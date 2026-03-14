#!/usr/bin/env python3
"""
Demo 7 Helper: Utility functions for module call demo
"""

def add_numbers(a: int, b: int) -> int:
    """Add two numbers
    
    __C_CODE__
    return a + b;
    """
    return a + b


def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers
    
    __C_CODE__
    return a * b;
    """
    return a * b


def calculate_stats() -> list:
    """Calculate sum, average, and max of fixed data
    
    __C_CODE__
    int32_t data[5] = {1, 2, 3, 4, 5};
    int32_t sum = 0;
    int32_t max_val = data[0];
    for (int i = 0; i < 5; i++) {
        sum += data[i];
        if (data[i] > max_val) max_val = data[i];
    }
    int32_t avg = sum / 5;
    int32_t* result = (int32_t*)gc_malloc(sizeof(int32_t) * 3);
    result[0] = sum;
    result[1] = avg;
    result[2] = max_val;
    return result;
    """
    data: list = [1, 2, 3, 4, 5]
    total: int = 0
    max_val: int = data[0]
    i: int = 0
    
    while i < 5:
        total = total + data[i]
        if data[i] > max_val:
            max_val = data[i]
        i = i + 1
    
    avg: int = total // 5
    
    result: list = [total, avg, max_val]
    return result
