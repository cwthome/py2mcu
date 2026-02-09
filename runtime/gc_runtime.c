// Minimal GC runtime implementation for py2mcu
#include "gc_runtime.h"
#include <stdlib.h>

void* gc_malloc(size_t size) {
    return malloc(size);
}

void gc_free(void* ptr) {
    free(ptr);
}
