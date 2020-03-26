#![no_std]
#![no_main]

extern crate panic_halt;

use icebesoc_pac;
use riscv_rt::entry;

mod timer;
mod vga;
mod print;

use timer::Timer;
use vga::PMOD_VGA;

const SYSTEM_CLOCK_FREQUENCY: u32 = 20_000_000;

// This is the entry point for the application.
// It is not allowed to return.
#[entry]
fn main() -> ! {
    let peripherals = icebesoc_pac::Peripherals::take().unwrap();

    print::print_hardware::set_hardware(peripherals.UART);
    let mut timer = Timer::new(peripherals.TIMER0);

    let mut vga = PMOD_VGA::new(peripherals.VGA);
    let mut color = 0;

    loop {
        unsafe {
            vga.set(color);
        }

        color = color + 1;
        usleep(&mut timer, 16666);
    }
}

fn usleep(timer: &mut Timer, us: u32) {
    timer.disable();

    timer.reload(0);
    timer.load(SYSTEM_CLOCK_FREQUENCY / 1_000_000 * us);

    timer.enable();

    // Wait until the time has elapsed
    while timer.value() > 0 {}    
}

fn msleep(timer: &mut Timer, ms: u32) {
    timer.disable();

    timer.reload(0);
    timer.load(SYSTEM_CLOCK_FREQUENCY / 1_000 * ms);

    timer.enable();

    // Wait until the time has elapsed
    while timer.value() > 0 {}
}
