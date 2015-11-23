from subprocess import call
from subprocess import Popen, PIPE


# Run the ls command
#hexdump -v -e '"0x" 1/1 "%02X" ","' /bin/ls
execPath = "/bin/ls"
process = Popen(["hexdump", "-v", "-e", '"0x" 1/1 "%02X" ","', execPath], stdout=PIPE)

# Grab the stdout and the stderr streams
(output, err) = process.communicate()
print("before output")
print(output)
print("after output")

# Wait for the process to finish and get the exit code
exit_code = process.wait()

# If the process exited with a code of 0, then it ended normally.
# Otherwise, it terminated abnormally
if exit_code == 0:
	retVal = output	

