#!/usr/bin/env python3
"""
Demo 4: Memory Management Strategies
Demonstrates: stack allocation, arena allocation, reference counting
"""

from py2mcu.decorators import arena, static_alloc

# Stack allocation for fixed-size data
@static_alloc
def process_sensor_reading(value: int) -> int:
    """
    Process sensor reading using stack allocation
    Fast and deterministic, no heap allocation
    """
    # All variables allocated on stack
    filtered: int = value
    threshold: int = 100

    if filtered > threshold:
        filtered = threshold

    return filtered

# Arena allocation for temporary data
@arena
def process_batch(data: list, count: int) -> int:
    """
    Process batch of data using arena allocation
    Memory automatically freed when function returns
    """
    # Temporary buffers allocated in arena
    temp_buffer: list = [0] * count
    i: int = 0

    # Process data
    while i < count:
        temp_buffer[i] = data[i] * 2
        i = i + 1

    # Calculate sum
    total: int = 0
    i = 0
    while i < count:
        total = total + temp_buffer[i]
        i = i + 1

    # temp_buffer automatically freed here
    return total

def create_persistent_buffer(size: int) -> list:
    """
    Create persistent buffer using reference counting
    Buffer persists until all references are released
    """
    # Allocated on heap with reference count
    buffer: list = [0] * size
    return buffer  # Reference count = 1

def demo_stack_allocation() -> None:
    """Demonstrate stack allocation"""
    print("=== Stack Allocation Demo ===")

    # Fast stack-based processing
    readings: list = [50, 150, 75, 200, 25]
    i: int = 0

    while i < 5:
        result: int = process_sensor_reading(readings[i])
        print("Processed:", result)
        i = i + 1

def demo_arena_allocation() -> None:
    """Demonstrate arena allocation"""
    print("=== Arena Allocation Demo ===")

    # Temporary processing with arena
    data: list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result: int = process_batch(data, 10)
    print("Batch result:", result)

    # All temporary memory freed after process_batch returns

def demo_reference_counting() -> None:
    """Demonstrate reference counting"""
    print("=== Reference Counting Demo ===")

    # Create persistent buffer
    buffer1: list = create_persistent_buffer(100)  # refcount = 1
    buffer2: list = buffer1                         # refcount = 2

    # Use buffers
    buffer1[0] = 42
    print("Buffer value:", buffer2[0])

    # Release references
    buffer1 = None  # refcount = 1
    buffer2 = None  # refcount = 0, memory freed

def main() -> None:
    """Main program"""
    print("Memory Management Demo\n")

    demo_stack_allocation()
    print()

    demo_arena_allocation()
    print()

    demo_reference_counting()
    print()

    print("Demo complete")

if __name__ == "__main__":
    main()
