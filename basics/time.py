import time
current_time = time.time()
print("Current time in seconds since the epoch:", current_time)
epoch_time = 1613004173.957986
local_time = time.ctime(epoch_time)
print("Local time for the given epoch time:", local_time)