use icebesoc_pac::COUNTER;

pub struct Counter {
    registers: COUNTER,
}

#[allow(dead_code)]
impl Counter {
    pub fn new(registers: COUNTER) -> Self {
        Self { registers }
    }

    pub fn set(&mut self, value: u32) {
        unsafe {
            self.registers.out.write(|w| w.bits(value));
        }
    }

    pub fn get(&self) -> u32 {
        self.registers.out.read().bits()
    }

    pub fn off(&mut self) {
        unsafe {
            self.registers.out.write(|w| w.bits(0));
        }
    }

    pub fn on(&mut self) {
        unsafe {
            self.registers.out.write(|w| w.bits(3));
        }
    }

    pub fn toggle(&mut self) {
        self.toggle_mask(0xFFFF_FFFF);
    }

    pub fn toggle_mask(&mut self, mask: u32) {
        let val: u32 = self.registers.out.read().bits() ^ mask;
        unsafe {
            self.registers.out.write(|w| w.bits(val));
        }
    }
}