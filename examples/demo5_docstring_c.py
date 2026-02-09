"""
Demo 5: Docstring Embedded C Code
==================================

Demonstrates using __C_CODE__ marker in docstrings to embed C code
that gets compiled to MCU while keeping Python executable for PC testing.

Features:
- Direct register access for GPIO
- Fast ADC reading
- Critical timing sections
- Python fallback for PC testing
"""

def gpio_set_high(pin: int) -> None:
    """__C_CODE__
    GPIOA->BSRR = (1 << pin);
    """
    # Python fallback for PC testing
    print(f"GPIO Pin {pin}: HIGH")


def gpio_set_low(pin: int) -> None:
    """__C_CODE__
    GPIOA->BSRR = (1 << (pin + 16));
    """
    # Python fallback for PC testing
    print(f"GPIO Pin {pin}: LOW")


def gpio_toggle(pin: int) -> None:
    """__C_CODE__
    GPIOA->ODR ^= (1 << pin);
    """
    # Python fallback for PC testing
    print(f"GPIO Pin {pin}: TOGGLE")


def adc_read_channel(channel: int) -> int:
    """__C_CODE__
    ADC1->SQR3 = channel;
    ADC1->CR2 |= ADC_CR2_SWSTART;
    while(!(ADC1->SR & ADC_SR_EOC));
    return ADC1->DR;
    """
    # Python fallback for PC testing
    import random
    value = random.randint(0, 4095)
    print(f"ADC Channel {channel}: {value}")
    return value


def delay_microseconds(us: int) -> None:
    """__C_CODE__
    volatile uint32_t count = us * (SystemCoreClock / 1000000);
    while(count--);
    """
    # Python fallback for PC testing
    import time
    time.sleep(us / 1000000.0)
    print(f"Delay: {us} us")


def critical_timing_loop() -> None:
    """__C_CODE__
    // Critical timing: toggle pin every 10 cycles
    for(int i = 0; i < 1000; i++) {
        GPIOA->ODR ^= (1 << 5);
        __asm volatile("nop");
        __asm volatile("nop");
        __asm volatile("nop");
        __asm volatile("nop");
        __asm volatile("nop");
        GPIOA->ODR ^= (1 << 5);
        __asm volatile("nop");
        __asm volatile("nop");
        __asm volatile("nop");
        __asm volatile("nop");
    }
    """
    # Python fallback for PC testing
    print("Critical timing loop executed (1000 iterations)")
    for i in range(1000):
        pass  # Simulate timing loop


def read_multiple_channels() -> int:
    """__C_CODE__
    uint32_t sum = 0;
    for(int ch = 0; ch < 4; ch++) {
        ADC1->SQR3 = ch;
        ADC1->CR2 |= ADC_CR2_SWSTART;
        while(!(ADC1->SR & ADC_SR_EOC));
        sum += ADC1->DR;
    }
    return sum / 4;
    """
    # Python fallback for PC testing
    import random
    values = [random.randint(0, 4095) for _ in range(4)]
    avg = sum(values) // 4
    print(f"Multi-channel ADC average: {avg} (channels: {values})")
    return avg


def main() -> None:
    """Main demo function"""
    print("=== Demo 5: Docstring Embedded C Code ===\n")
    
    print("1. GPIO Control:")
    gpio_set_high(5)
    delay_microseconds(1000)
    gpio_set_low(5)
    delay_microseconds(1000)
    gpio_toggle(5)
    print()
    
    print("2. ADC Reading:")
    value: int = adc_read_channel(0)
    print(f"   Single channel value: {value}")
    print()
    
    print("3. Multi-channel ADC:")
    avg: int = read_multiple_channels()
    print(f"   Average value: {avg}")
    print()
    
    print("4. Critical Timing:")
    critical_timing_loop()
    print()
    
    print("Demo completed!")


if __name__ == "__main__":
    main()