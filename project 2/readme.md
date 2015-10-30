#Requirement for project 2 : CPSC 456 

####This assignment does not involve implementation of self-propagating malware and therefore can be safely done on any any 32-bit Ubuntu system. However, this assignment shall be graded using 32-bit Ubuntu 12.04 system. It is in your best interest to test your submission on such system prior to submitting it.

If you choose to do this assignment on your own Ubuntu 12.04 system, you will need to install
g++ version 4.8. Please see the following link for the instructions for installing g++ version 4.8

```
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install gcc-4.8
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 50
```


#Overview

In class we learned about control hijacking attacks and binders of executable les. Implement-
ing these requires understanding of the techniques used for manipulating and combining binary
codes. These skills are important for developing vulnerability patches, executing and countering
control hijacking attacks, analyzing malware, and in many other facets of network security.
This assignment has two parts. In the rst part you will experiment with a primitive technique
which can be used for hiding malicious codes on Microsoft Windows systems. In the second part,
you are going to implement a program for combining multiple binary executables into a single
executable le which when ran executes all the constituent executables. This type of program
is called a binder.

#Part I
In order to complete this part you will need a Windows 7 VM which you can nd on your
security lab node.
 1. Boot your VM.
 2. Download the http://www.7-zip.org compression program.
 3. Launch the installer and follow the installation instructions.
 4. Download the worm.bat le from one of the earlier demos given in class. The le can be found on Titanium. Recall, the le illustrates a very simple Windows worm which can hang your system.
 5. Right-click on worm.bat, and from the menu choose 7-zip ! Add to worm.7z
 6. Find a .gif image
 7. Copy the .7z and .gif les to the same directory (if you have not already done so).
 8.  Hold the Shift key and right-click in the directory containing the two les.
 9.   From the drop-down right-click menu choose: Open command window here.
 10. In the terminal window that appears, enter the following command: copy /B <gif file name> + <7z file name> result. For example, copy /B mygifile.gif + myzipfile.7z result.
 11. The above command should have created a le called result in the same directory.
 12. Rename the result le to result.7z (i.e., append the 7z extension).
 13. Try opening the le using the 7-zip program. What happens? (Note: one way to open the le using the 7-zip program is to right-click on result.7z and choose 7-zip ! Open archive. What happens? Are you able to extract and run the worm.bat le inside the archive?
 14. Repeat the above steps, but this time rename the le to result.gif extension.
 15. Try opening the le. What happens?
 
 ### Question to answers
 * Explain what is happening. Do some research in order to nd out what the above copy command does. In your explanation be sure to explain the role of each argument in the above command. Also, be sure to explain how Windows handles les which leads to the above behavior. Include the answers to these questions in the README le you submit.
 - How can this technique be used for hiding malicious codes?
 + How robust is this technique in terms of avoiding detection by anti-virus tools? You may need to do some research.

###Part II
In this part of the assignment, you are going to implement an executable binder program. The program shall take names of multiple executable les as command line arguments and merge these executables into a single executable le called bound. Executing the bound binary shall execute all of the constituent executables. The binder program shall be invoked using python binder.py h PROG1 i h PROG2 i...h PROGN i command line where each PROGi is an executable program. For example, python binder.py /usr/bin/ls /usr/bin/pwd.

##The program architecture comprises two main components:
 1. A python script called binder.py: this script has the following logic: 
   + (a) Call the hexdump program on each executable le provided as command line argument in order to extract and convert the binary contents of each executable le into a sequence of C/C++-style, 1-byte hexadecimal values (i.e. each value comprising two hexadecimal digits prexed with 0x. For example, 0x1a). Before proceeding with this part, you should spend sometime experimenting with the hexdump utility on the terminal. Try the following sequence of commands: hexdump /usr/bin/ls. What is the output? What does this output: "hexdump", "-v", "-e", '"0x" 1/1 "%02X" ","', /usr/bin/ls. You will nd this command useful in this assignment. More information about hexdump utility can be found on <http://manpages.debian.org/cgi-bin/man.cgi?query=hexdump&sektion=1.>
   + (b) Generates a C++ header le called codearray.h. This le contains a C/C++-style array of pointers to unsigned characters codeArray. The pointer at index location i of the array points to the array of hexadecimal numbers representing executable instructions and data of each executable le previously extracted using the hexdump utility. For example, lets assume we have three programs. The programs have sizes of 5, 3, and 6 bytes respectively. <br>The codeArray should be dened as
```
  unsigned char* codeArray[3] = fnew char[5]f0x43, 0x91, 0xa1, 0xdb, 0xffg,
   new char[3]f0x12, 0xfe, 0xabg,
  new char[6]f0x56, 0x45, 0x8d, 0x37, 0x78, 0x30g g;
 ```
 In the same le, the script adds an array of integers programLenghts where each index location i contains the length of the ith row of codeArray. It also adds a C/C++- style macro or a constant NUM BINARIES specifying the number of programs to be bound. For example, assume we have three programs from the previous example. The script will add array programLenghts[3] = f5, 3, 6g; and macro #define NUM BINARIES.
Finally, the script invokes the g++ compiler program in order to compile the binderbackend.cpp le which includes the codearray.h as header le and executes the binary codes in the codeArray array dened therein. The g++ compilation line is<code> g++ binderbackend.cpp -o bound -std=gnu++11</code>.
 2. A C++ program called binderbackend.cpp which is a program implementing the logic for executing the codes of each executable in the array codeArray declared and initialized in codeArrays.h. This program, when executed, has the following 
ow of logic: for each row i in the codeArray:
   + (a) Generate a randomly named temporary le. This can be achieved using the tmpnam() function which will create a randomly named le in the /tmp directory. The syntax for calling tmpnam() is <code> char* fileName = tmpnam(NULL);</code>
   + (b) Give the le executable permissions; can be done using chmod(fileName, 0777);
   + (c) Write all columns of row i to the above-create le. This can be achieved using the fwrite() function; please see the fwrite.cpp sample le for details. Please note: doing this operation requires us knowing the number of elements in each row. This value we can nd in the programLenghts array at index location i.
   + (d) Issue a fork() system call which will spawn another process which is a clone of the process that has issued fork() system call. The new process is called a child process while the original process is called a parent process. Both processes will continue executing with the next line following the fork() system call. In the parent process, the fork() system call returns the process id of the child, while in the parent it returns 0.
   + (e) The child process shall invoke the execlp() system call in order to turn into process which runs an executable le we just created, while
   + (f) The parent process repeats the above steps on row i + 1 until all rows of the matrix have been processed. You can nd an example on how to use fork() and execlp() system calls in fork.cpp. Also, the following link gives a nice tutorial on the same.
   + (g) The parent process then waits for all children to nish. The skeleton les for binder.py and binderbackend.cpp have been provided. Please check out the TODO: comments.

###BONUS:
#Implement the same binder program on the Windows platform.
