// Minimal GC runtime header for py2mcu
#ifndef GC_RUNTIME_H
#define GC_RUNTIME_H

#include <stdint.h>
#include <stdlib.h>

// Memory allocation wrappers
void* gc_malloc(size_t size);
void gc_free(void* ptr);

#endif // GC_RUNTIME_H
