import gc

# Optional: Run garbage collection first to free up unused objects
gc.collect()

# Get free and allocated RAM in bytes
free_ram = gc.mem_free()
used_ram = gc.mem_alloc()

print(f"Free RAM: {free_ram} bytes")
print(f"Used RAM: {used_ram} bytes")