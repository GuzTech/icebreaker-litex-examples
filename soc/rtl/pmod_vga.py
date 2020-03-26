# This file is Copyright (c) 2020 Oguz Meteer <info@guztech.nl>
# License: BSD

from migen import *

from litex.soc.interconnect.csr import *
from litex.soc.integration.doc import AutoDoc, ModuleDoc


class VGA(Module, AutoCSR, AutoDoc):
	"""VGA PMOD module

   	This module uses the Digilent PmodVGA board, generates an 800x600 @ 60Hz VGA signal,
   	and displays a single color which is determined by the CSR value.

   	Attributes:
    	red: The bits for the red color.
      	green: The bits for the green color.
      	blue: The bits for the blue color.
      	hsync: The horizontal sync signal.
      	vsync: The vertical sync signal.
      	color: The new color.
    """
	def __init__(self, red, green, blue, hsync, vsync):
		# Documentation
		self.intro = ModuleDoc("""VGA PMOD module.

		This module uses the Digilent PmodVGA board, generates an 800x600 @ 60Hz VGA signal,
		and displays a single color which is determined by the CSR value.
		""")

		# HDL Implementation
		self.csr = csr = CSRStorage(size=len(red) + len(green) + len(blue), fields=[
			CSRField(name="red", size=len(red), description="The value of the red color channel"),
			CSRField(name="green", size=len(green), description="The value of the green color channel"),
			CSRField(name="blue", size=len(blue), description="The value of the blue color channel"),
		])

		# General timing: 800x600 @ 60Hz (taken from http://tinyvga.com/vga-timing/800x600@60Hz).
		# This mode requires a pixel clock of 40 MHz.
		# The values below are the timings in pixel clocks.
		H_VISIBLE_AREA = 800
		H_FRONT_PORCH  = 40
		H_SYNC_PULSE   = 128
		H_BACK_PORCH   = 88
		H_TOTAL = H_VISIBLE_AREA + H_FRONT_PORCH + H_SYNC_PULSE + H_BACK_PORCH

		V_VISIBLE_AREA = 600
		V_FRONT_PORCH  = 1
		V_SYNC_PULSE   = 4
		V_BACK_PORCH   = 23
		V_TOTAL = V_VISIBLE_AREA + V_FRONT_PORCH + V_SYNC_PULSE + V_BACK_PORCH

		self.hcnt = Signal(log2_int(H_TOTAL, need_pow2=False))
		self.vcnt = Signal(log2_int(V_TOTAL, need_pow2=False))
      	
		# Horizontal counter
		self.sync.pix += If(self.hcnt == (H_TOTAL - 1),
							self.hcnt.eq(0)
						).Else(
							self.hcnt.eq(self.hcnt + 1)
						)

		# Vertical counter
		self.sync.pix += If((self.hcnt == (H_TOTAL - 1)) & (self.vcnt == (V_TOTAL - 1)),
							self.vcnt.eq(0)
						).Elif(self.hcnt == (H_TOTAL - 1),
							self.vcnt.eq(self.vcnt + 1)
						)

		# Horizontal sync
		self.sync.pix += If((self.hcnt >= (H_VISIBLE_AREA + H_FRONT_PORCH)) & (self.hcnt < (H_TOTAL - H_BACK_PORCH)),
							hsync.eq(1)
						).Else(
							hsync.eq(0)
						)

		# Vertical sync
		self.sync.pix += If((self.vcnt >= (V_VISIBLE_AREA + V_FRONT_PORCH)) & (self.vcnt < (V_TOTAL - V_BACK_PORCH)),
							vsync.eq(1)
						).Else(
							vsync.eq(0)
						)

		# Drawing a solid color when we are in the visible area
		self.draw = Signal()
		self.comb += self.draw.eq((self.hcnt < H_VISIBLE_AREA) & (self.vcnt < V_VISIBLE_AREA))

		# Clear red, green, and blue when we are NOT in the visible area.
		# This is necessary because some monitors use the RGB values outside
		# of the visible area as black level calibration. So it is necessary
		# in order for black to be actually displayed as black.
		self.sync.pix += If(self.draw,
							red.eq(csr.fields.red),
							green.eq(csr.fields.green),
							blue.eq(csr.fields.blue)
						).Else(
							red.eq(0),
							green.eq(0),
							blue.eq(0))