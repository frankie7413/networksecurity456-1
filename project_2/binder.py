import os
import sys
from subprocess import call
import os
from subprocess import Popen, PIPE

#running the file 
#python binder.py /bin/ls /bin/pwd
# The file name
FILE_NAME = "codearray.h";

###########################################################
# Returns the hexidecimal dump of a particular binary file
# @execPath - the executable path
# @return - returns the hexidecimal string representing
# the bytes of the program. The string has format:
# byte1,byte2,byte3....byten,
# For example, 0x19,0x12,0x45,0xda,
##########################################################
def getHexDump(execPath):

	# The return value
	retVal = None

	# TODO:
	# 1. Use popen() in order to run hexdump and grab the hexadecimal bytes of the program.
	#Popen(["hexdump", "-v", "-e", '"0x" 1/1 "%02X" ","', "/bin/ls"], stdout=PIPE)
	process = Popen(["hexdump", "-v", "-e", '"0x" 1/1 "%02X" ","',execPath], stdout=PIPE)

	# 2. If hexdump ran successfully, return the string retrieved. Otherwise, return None.
	# The command for hexdump to return the list of bytes in the program in C++ byte format
	# the command is hexdump -v -e '"0x" 1/1 "%02X" ","' progName
	(output, err) = process.communicate()

	#wait for the process to finish and get the exit code
	exit_code = process.wait()

	#if the process exited with a code of 0, then it ended normally.
	#otherwise, it terminated abnormally.
	print retVal
	if exit_code == 0:
		retVal = output
	return retVal


###################################################################
# Generates the header file containing an array of executable codes
# @param execList - the list of executables
# @param fileName - the header file to which to write data
###################################################################

def generateHeaderFile(execList, fileName):

    # The header file
    headerFile = None

    # The program array
    progNames = sys.argv

    # Open the header file
    headerFile = open(fileName, "w")

    # The program index
    progCount = 0

    # The lengths of programs
    progLens = []

    # Write the array name
    headerFile.write("#include <string>\n\nusing namespace std;\n\nunsigned char* codeArray[] = {");

    # Go through the program names
    for progName in execList:
    
        # Count the program
        progCount += 1
    
        print("Generating a hexdump of", progName,)    
        # Generate the hex code
        hexCode = getHexDump(progName)
    
        print("Done!")
    
        
        # Failed to get hex dump for the program
        if not hexCode:
            print("Invalid path for program " + progName)
            
            # Close the file
            headerFile.close()
        
            # Remove the file
            os.remove(FILE_NAME)
        
            # Exit abnormally
            exit(1)
    
        # Remove the last comma
        if len(hexCode) > 0:
            hexCode = hexCode.decode("utf-8").rstrip(",")
    
        # Get the program length
        programLength = len(hexCode.split(","))
        
        # Save the program length
        progLens.append(str(programLength))
        
        # Write the code surrounded by quotes
        headerFile.write("new unsigned char[" + str(programLength) + "]{" + hexCode + "}");
            
        # This is the last element -- insert the closing "}"
        if progCount == len(execList):
            headerFile.write("};")
    
        # This is not the last element
        else:
            # Add the ","
            headerFile.write(",");
    

    # The array to contain program lengths
    headerFile.write("\n\nunsigned programLengths[] = {")

    # The number of programs
    numProgs = 0

    for progLen in progLens:
    
        # Increment the program
        numProgs+=1
    
        headerFile.write(str(progLen))
    
        # If this is the last element add "}"
        if numProgs == len(progLens):
            headerFile.write("};")
        # Otherwise, add a ","
        else:
            headerFile.write(",")
    


    # Write the number of programs
    headerFile.write("\n\n#define NUM_BINARIES " +  str(len(execList)))
    
    headerFile.close()

############################################################
# Compiles the combined binaries
# @param binderCppFileName - the name of the C++ binder file
# @param execName - the executable file name
############################################################
def compileFile(binderCppFileName, execName):

	print("Compiling...")

	# Run the process
	# TODO: run the g++ compiler in order to compile backbinder.cpp
	# If the compilation succeeds, print "Compilation succeeded"
	# If compilation failed, then print "Compilation failed"
	# Do not forget to add -std=gnu++11 flag to your compilation line
	process = Popen(["g++", binderCppFileName, "-o", execName, "-std=gnu++11"], stdout = PIPE)
	(output, err) = process.communicate()

	#wait for the process to finish and get the exit code
	exit_code = process.wait()

	#if the process exited with a code of 0, then it ended normally.
	#otherwise, it terminated abnormally.
	if exit_code == 0:
		val = output
		return val
	pass

generateHeaderFile(sys.argv[1:], FILE_NAME)
compileFile("binderbackend.cpp", "bound")

print("Done Compiling")
