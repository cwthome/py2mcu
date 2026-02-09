"""py2mcu demo6: C #define with @#define annotations

This demo shows how to use @#define comments to generate C preprocessor
definitions. This is useful for:
- Hardware configuration constants
- Buffer sizes and limits
- Feature flags and compile-time options
- Register addresses and bit masks

The @#define annotation converts Python constants to C #define directives,
allowing compile-time optimization while keeping Python code testable.
"""

# =================================================================================
# Hardware Configuration
# =================================================================================

LED_PIN = 13  # @#define uint8_t
BUTTON_PIN = 2  # @#define uint8_t
ADC_CHANNEL = 0  # @#define uint8_t

# GPIO Port Base Addresses (STM32F4)
GPIOA_BASE = 0x40020000  # @#define uint32_t
GPIOB_BASE = 0x40020400  # @#define uint32_t
GPIOC_BASE = 0x40020800  # @#define uint32_t

# =================================================================================
# Buffer Sizes and Limits
# ================================================================================

MAX_SAMPLES = 100  # @#define
BUFFER_SIZE = 1024  # @#define
UART_BUFFER_SIZE = 256  # @#define

# Expression with operators
TIMEOUT_MS = 1000 * 60  # @#define
BAUD_RATE = 115200  # @#define

# =================================================================================
# Feature Flags
# =================================================================================

DEBUG_ENABLED = True  # @#define
USE_DMA = False  # @#define
ENABLE_LOGGING = True  # @#define

# =================================================================================
# String Constants
# ===============================================================================

DEVICE_NAME = "py2mcu"  # @#define
FIRMWARE_VERSION = "1.0.0"  # @#define

# =================================================================================
# Functions Using Defines
# ===============================================================================

def init_gpio():
    """Initialize GPIO using defines
    
    __C_CODE__
    // Enable GPIOA clock
    RCC->AHB1ENR |= (1 << 0);
    
    // Configure LED pin as output
    volatile uint32_t* moder = (uint32_t*)(GPIOA_BASE + 0x00);
    *moder &= ~(3 << (LED_PIN * 2));
    *moder |= (1 << (LED_PIN * 2));
    
    // Configure BUTTON pin as input
    *moder &= ~(3 << (BUTTON_PIN * 2));
    """
    print(f"Initializing GPIO: LED={LED_PIN}, BUTTON={BUTTON_PIN}")

def blink_led():
    """Blink LED using defines
    
    __C_CODE__
    volatile uint32_t* bsrr = (uint32_t*)(GPIOA_BASE + 0x18);
    
    // Turn LED on
    *bsrr = (1 << LED_PIN);
    HAL_Delay(500);
    
    // Turn LED off
    *bsrr = (1 << (LED_PIN + 16));
    HAL_Delay(500);
    """
    print(f"Blinking LED on pin {LED_PIN}")

def read_adc_samples() -> int:
    """Read multiple ADC samples into buffer
    
    __C_CODE__
    int32_t buffer[MAX_SAMPLES];
    int count = 0;
    
    while (count < MAX_SAMPLES) {
        buffer[count] = HAL_ADC_GetValue(&hadc1);
        count++;
    }
    
    // Calculate average
    int32_t sum = 0;
    for (int i = 0; i < MAX_SAMPLES; i++) {
        sum += buffer[i];
    }
    
    return sum / MAX_SAMPLES;
    """
    # PC simulation
    import random
    return sum([random.randint(0, 1023) for _ in range(100)]) // 100

def main() -> None:
    """Main program"""
    print("Defines Demo")
    print(f"Device: {DEVICE_NAME}")
    print(f"Firmware: {FIRMWARE_VERSION}")
    print(f"Buffer size: {BUFFER_SIZE}")
    print(f"Timeout: {TIMEOUT_MS} ms")
    
    init_gpio()
    
    while True:
        blink_led()
        avg_value: int = read_adc_samples()
        print(f"ADG Average: {avg_value}")

if __name__ == "__main__":
    main()
