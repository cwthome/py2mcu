#include "gc_runtime.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// Global arena
static uint8_t arena_buffer[GC_ARENA_SIZE];
gc_arena_t global_arena;

// Statistics
static gc_stats_t stats = {0};

// ============ Arena Implementation ============
void gc_arena_init(gc_arena_t* arena, void* buffer, size_t size) {
    arena->memory = (uint8_t*)buffer;
    arena->size = size;
    arena->offset = 0;
}

void* gc_arena_alloc(gc_arena_t* arena, size_t size) {
    // 8-byte alignment
    size = (size + 7) & ~7;

    if (arena->offset + size > arena->size) {
        return NULL;
    }

    void* ptr = arena->memory + arena->offset;
    arena->offset += size;

    stats.total_allocated += size;
    stats.current_used += size;
    if (stats.current_used > stats.peak_used) {
        stats.peak_used = stats.current_used;
    }

    return ptr;
}

void gc_arena_reset(gc_arena_t* arena) {
    stats.current_used -= arena->offset;
    arena->offset = 0;
}

size_t gc_arena_checkpoint(gc_arena_t* arena) {
    return arena->offset;
}

void gc_arena_restore(gc_arena_t* arena, size_t checkpoint) {
    if (checkpoint <= arena->offset) {
        stats.current_used -= (arena->offset - checkpoint);
        arena->offset = checkpoint;
    }
}

// ============ Reference Counting ============
#if GC_USE_REFCOUNT
void* gc_alloc(size_t size) {
    gc_object_t* obj = malloc(sizeof(gc_object_t) + size);
    if (obj == NULL) return NULL;

    obj->refcount = 1;
    obj->size = size;

    stats.alloc_count++;
    stats.total_allocated += size;
    stats.current_used += size;
    if (stats.current_used > stats.peak_used) {
        stats.peak_used = stats.current_used;
    }

    return obj->data;
}

void* gc_retain(void* ptr) {
    if (ptr == NULL) return NULL;

    gc_object_t* obj = (gc_object_t*)((uint8_t*)ptr - offsetof(gc_object_t, data));
    obj->refcount++;
    return ptr;
}

void gc_release(void* ptr) {
    if (ptr == NULL) return;

    gc_object_t* obj = (gc_object_t*)((uint8_t*)ptr - offsetof(gc_object_t, data));

    if (--obj->refcount == 0) {
        stats.free_count++;
        stats.current_used -= obj->size;
        free(obj);
    }
}

uint32_t gc_refcount(void* ptr) {
    if (ptr == NULL) return 0;
    gc_object_t* obj = (gc_object_t*)((uint8_t*)ptr - offsetof(gc_object_t, data));
    return obj->refcount;
}
#endif

// ============ Statistics ============
void gc_get_stats(gc_stats_t* out) {
    memcpy(out, &stats, sizeof(gc_stats_t));
}

void gc_print_stats(void) {
    printf("=== GC Statistics ===\n");
    printf("Total allocated: %zu bytes\n", stats.total_allocated);
    printf("Current used: %zu bytes\n", stats.current_used);
    printf("Peak used: %zu bytes\n", stats.peak_used);
    printf("Alloc count: %u\n", stats.alloc_count);
    printf("Free count: %u\n", stats.free_count);
    printf("Leaked objects: %u\n", stats.alloc_count - stats.free_count);
}

// Initialize on startup
__attribute__((constructor))
void gc_init(void) {
    gc_arena_init(&global_arena, arena_buffer, GC_ARENA_SIZE);
}
