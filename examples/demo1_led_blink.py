#!/usr/bin/env python3
"""
Demo 1: LED Blink - Basic Control Flow
Demonstrates: if/while loops, function calls, basic GPIO
"""

# Optional GUI integration (PC simulation)
import demo1_led_blink_gui as gui
"""
__C_CODE__
#ifdef TARGET_PC
    #include <time.h>
#endif
"""

# Hardware configuration
LED_PIN: int = 13

def delay_ms(ms: int) -> None:
    """Delay for specified milliseconds
    
    __C_CODE__
    #ifdef TARGET_PC
    // PC simulation: nanosleep
    struct timespec ts;
    ts.tv_sec = ms / 1000;
    ts.tv_nsec = (ms % 1000) * 1000000L;
    nanosleep(&ts, NULL);
    #else
    // STM32F4 precise delay using SysTick
    uint32_t start = HAL_GetTick();
    while ((HAL_GetTick() - start) < ms) {
        __NOP();  // No operation, just wait
    }
    #endif
    """
    # PC simulation: Python sleep
    import time
    time.sleep(ms / 1000.0)

def gpio_write(pin: int, value: bool) -> None:
    """Write digital value to GPIO pin
    
    __C_CODE__
    #ifdef TARGET_PC
    // PC simulation: print GPIO state
    printf("GPIO Pin %d: %s\n", pin, value ? "HIGH" : "LOW");
    #else
    // STM32F4 GPIO write (assumes GPIOA)
    if (value) {
        GPIOA->BSRR = (1 << pin);  // Set pin high
    } else {
        GPIOA->BSRR = (1 << (pin + 16));  // Set pin low
    }
    #endif
    """
    if pin == LED_PIN:
        gui.set_led(value)
    print(f"GPIO Pin {pin}: {'HIGH' if value else 'LOW'}")


def setup() -> None:
    """Initialize hardware"""
    # Configure LED pin as output
    print("Setting up LED on pin", LED_PIN)

def loop() -> None:
    gpio_write(LED_PIN, True)   # LED on
    delay_ms(500)
    gpio_write(LED_PIN, False)  # LED off
    delay_ms(1000)

def main() -> None:
    setup()
    while True:
        loop()
        gui.root.update_idletasks()  # 更新空闲任务
        gui.root.update()            # 处理事件
        gui.loop()

if __name__ == "__main__":
    main()
