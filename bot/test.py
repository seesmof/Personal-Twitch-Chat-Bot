import time

start_time = time.time()
running = True

# Loop until the stopwatch is stopped
while running:
    # Update the stopwatch display
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.1f} seconds", end="\r")

    # Check for the stop event
    # Replace this with your own event
    if elapsed_time > 5:
        running = False
        stop_time = time.time()

# Calculate the elapsed time and print it
elapsed_time = stop_time - start_time
print(f"\n\nElapsed time: {elapsed_time:.1f} seconds")
