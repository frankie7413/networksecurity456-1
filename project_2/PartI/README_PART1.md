Brandon Huebert	brandon_huebert@csu.fullerton.edu
Kourun Sok	kourun@csu.fullerton.edu
Denice Ron Valbuena	Denice_valbuena@csu.fullerton.edu
Francisco Rivas frankie7413@csu.fullerton.edu
CPSC 456
assignment 2

CPSC 456 Part I
Questions:
1. Try opening the file using the 7-zip program. What happens? (Note: one way to open the file using the 7-zip program is to right-click on result.7z and
  choose 7-zip ? Open archive. What happens? Are you able to extract and run the worm.bat file inside the archive?

When opening the file using 7-zip, one is able to see the worm.bat program intact and is able to extract it and run it.

2. Repeat the above steps, but this time rename the file to result.gif extension. Try opening the file. What happens?

When opening the result.gif file i was able to view the .gif in internet explorer with nothing else happening. The worm.bat did not execute. Furthermore,
the file size of the original and altered gif remain the same 520 KB on disk.

3. Explain what is happening. Do some research in order to find out what the above copy command does. In your explanation be sure to explain the role of each
argument in the above command. Also, be sure to explain how Windows handles files which leads to the above behavior. Include the answers to these questions
in the README file you submit.

Overall what the copy command does is copy one or more files that are known as source files and store them into a destination file. The argument of /B
indicates binary mode which makes the output into a binary file. Furthermore, the way windows handles the above behavior is by having the copied files stored in
the same format they were originally; therefore, the copied files can be used as they were before in their original format for example as a gif or 7zip file.

4. How can this technique be used for hiding malicious codes?
This technique can be used to hide malicious code in a file. By merging malicious code with a normal file, Attackers can uploaded a compromised file to
a file sharing network with the hidden malicious code. The users using the file sharing network would not be unaware of the tampering of the files
so it will appear as a legit program or movie or file or etc. However,from part 1 of the assignment, the worm does run when clicking on the gif image just remains
hidden in the image.

5. How robust is this technique in terms of avoiding detection by anti-virus tools? You may need to do some research.
This technique is not robust enough to evade detection by anti-virus since the copy command simply merges the files bytes to each other; therefore, an antivirus will
be able to pick up on the malicious bytes of the file with its virus signature and let the user know that the file contains malicious code.

Sources:
http://www.coolhackingtrick.com/2013/03/learn-to-hide-files-behind-images.html
https://superuser.com/questions/453245/what-exactly-happens-when-you-use-the-copy-b-command
https://stackoverflow.com/questions/1396443/how-do-antivirus-programs-detect-viruses
