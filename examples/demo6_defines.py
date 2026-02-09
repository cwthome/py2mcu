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

# ==============================================================================
# Hardware Configuration
# ==============================================================================

LED_PIN = 13  # @#define uint8_t
BUTTON_PIN = 2  # @#define uint8_t
ADC_CHANNEL = 0  # @#define uint8_t

# GPIO Port Base Addresses (STM32F4)
GPIOA_BASE = 0x40020000  # @#define uint32_t
GPIOB_BASE = 0x40020400  # @#define uint32_t
GPIOC_BASE = 0x40020800  # @#define uint32_t

# ==============================================================================
# Buffer Sizes and Limits
# ==============================================================================

MAX_SAMPLES = 100  # @#define
BUFFER_SIZE = 1024  # @#define
UART_BUFFER_SIZE = 256  # @#define

# Expression with operators
TIMEOUT_MS = 1000 * 60  # @#define
BAUD_RATE = 115200  # @#define

# ==============================================================================
# Feature Flags
# ==============================================================================

DEBUG_ENABLED = True  # @#define
USE_DMA = False  # @#define
ENABLE_LOGGING = True  # @#define

# ==============================================================================
# String Constants
# ==============================================================================

DEVICE_NAME = "STM32F4"  # @#define
FIRMWARE_VERSION = "1.0.0"  # @#define

# ==============================================================================
# Functions Using Defines
# ==============================================================================

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
    int32_t sum = 0;
    
    // Read samples
    for (int i = 0; i < MAX_SAMPLES; i++) {
        HAL_ADC_Start(&hadc1);
        HAL_ADC_PollForConversion(&hadc1, 100);
        buffer[i] = HAL_ADC_GetValue(&hadc1);
        sum += buffer[i];
    }
    
    // Return average
    return sum / MAX_SAMPLES;
    """
    # Python implementation for testing
    samples = [0] * MAX_SAMPLES
    for i in range(MAX_SAMPLES):
        samples[i] = i * 10  # Simulated ADC reading
    
    return sum(samples) // MAX_SAMPLES

def send_debug_message(message: str) -> None:
    """Send debug message if enabled
    
    __C_CODE__
    #if DEBUG_ENABLED
    char buffer[UART_BUFFER_SIZE];
    snprintf(buffer, UART_BUFFER_SIZE, "[%s] %s\n", DEVICE_NAME, message);
    HAL_UART_Transmit(&huart2, (uint8_t*)buffer, strlen(buffer), TIMEOUT_MS);
    #endif
    """
    if DEBUG_ENABLED:
        print(f"[{DEVICE_NAME}] {message}")

def configure_uart():
    """Configure UART with defines
    
    __C_CODE__
    huart2.Instance = USART2;
    huart2.Init.BaudRate = BAUD_RATE;
    huart2.Init.WordLength = UART_WORDLENGTH_8B;
    huart2.Init.StopBits = UART_STOPBITS_1;
    huart2.Init.Parity = UART_PARITY_NONE;
    huart2.Init.Mode = UART_MODE_TX_RX;
    HAL_UART_Init(&huart2);
    """
    print(f"Configuring UART: baud={BAUD_RATE}, buffer={UART_BUFFER_SIZE}")

def main():
    """Main demo function"""
    print("=== py2mcu Demo 6: @#define Annotations ===\n")
    
    print("Hardware Configuration:")
    print(f"  LED_PIN: {LED_PIN}")
    print(f"  BUTTON_PIN: {BUTTON_PIN}")
    print(f"  ADC_CHANNEL: {ADC_CHANNEL}")
    print()
    
    print("Buffer Sizes:")
    print(f"  MAX_SAMPLES: {MAX_SAMPLES}")
    print(f"  BUFFER_SIZE: {BUFFER_SIZE}")
    print(f"  UART_BUFFER_SIZE: {UART_BUFFER_SIZE}")
    print()
    
    print("Feature Flags:")
    print(f"  DEBUG_ENABLED: {DEBUG_ENABLED}")
    print(f"  USE_DMA: {USE_DMA}")
    print(f"  ENABLE_LOGGING: {ENABLE_LOGGING}")
    print()
    
    print("Device Info:")
    print(f"  DEVICE_NAME: {DEVICE_NAME}")
    print(f"  FIRMWARE_VERSION: {FIRMWARE_VERSION}")
    print()
    
    # Run demo functions
    init_gpio()
    blink_led()
    
    avg = read_adc_samples()
    print(f"Average ADC reading: {avg}")
    
    send_debug_message("System initialized")
    configure_uart()
    
    print("\n✓ Demo completed successfully!")

if __name__ == "__main__":
    main()
