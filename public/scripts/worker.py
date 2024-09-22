from pyscript import RUNNING_IN_WORKER, display, sync

display("Hello World", target="output", append=True)

# will log into devtools console
print(RUNNING_IN_WORKER)  # True
print("sleeping")
sync.sleep(1)
print("awake")