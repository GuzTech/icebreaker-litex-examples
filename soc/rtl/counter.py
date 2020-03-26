# This file is Copyright (c) 2020 Oguz Meteer <info@guztech.nl>
# License: BSD

from migen import *

from litex.soc.interconnect.csr import *
from litex.soc.integration.doc import AutoDoc, ModuleDoc


class Counter(Module, AutoCSR, AutoDoc):
    """Counter module

    This module creates a counter, and the CSR determines the how fast it counts.

    Attributes:
        cntr_size: The number of bits used for the CSR.
        cntr_out: The output of the counter.
    """
    def __init__(self, cntr_size, cntr_out):
        # Documentation
        self.intro = ModuleDoc("""Counter module.

        The CSR value determines the speed of the counter.
        """)

        # HDL Implementation
        self._out = CSRStorage(cntr_size)

        self.counter = Signal(30)

        self.sync.vga += self.counter.eq(self.counter + self._out.storage)
        self.comb += cntr_out.eq(self.counter[len(self.counter) - len(cntr_out):])
