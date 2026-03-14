#!/usr/bin/env python3
"""
Demo 7: Multiple Module Calls
Demonstrates: multiple Python modules calling each other
"""

"""
__C_CODE__
extern int32_t add_numbers(int32_t a, int32_t b);
extern int32_t multiply_numbers(int32_t a, int32_t b);
extern int32_t* calculate_stats(void);
"""

from demo7_helper import (
    add_numbers,
    multiply_numbers,
    calculate_stats,
)

def main() -> None:
    """Main program that uses functions from helper module"""
    print("=== Demo 7: Module Function Calls ===")
    print()

    a: int = 10
    b: int = 5
    
    sum_result: int = add_numbers(a, b)
    print(f"add_numbers({a}, {b}) = {sum_result}")
    
    product_result: int = multiply_numbers(a, b)
    print(f"multiply_numbers({a}, {b}) = {product_result}")
    
    stats: list = calculate_stats()
    print(f"calculate_stats([1,2,3,4,5])")
    print(f"  Sum: {stats[0]}, Avg: {stats[1]}, Max: {stats[2]}")
    
    print()
    print("Demo completed!")

if __name__ == "__main__":
    main()
