use icebesoc_pac::VGA;

pub struct PMOD_VGA {
    registers: VGA,
}

#[allow(dead_code)]
impl PMOD_VGA {
    pub fn new(registers: VGA) -> Self {
        Self { registers }
    }

    pub fn set(&mut self, value: u32) {
        unsafe {
            self.registers.csr.write(|w| w.bits(value));
        }
    }

    pub fn get(&self) -> u32 {
        self.registers.csr.read().bits()
    }

    pub fn off(&mut self) {
        unsafe {
            self.registers.csr.write(|w| w.bits(0));
        }
    }

    pub fn on(&mut self) {
        unsafe {
            self.registers.csr.write(|w| w.bits(3));
        }
    }

    pub fn toggle(&mut self) {
        self.toggle_mask(0xFFFF_FFFF);
    }

    pub fn toggle_mask(&mut self, mask: u32) {
        let val: u32 = self.registers.csr.read().bits() ^ mask;
        unsafe {
            self.registers.csr.write(|w| w.bits(val));
        }
    }
}