#include <string>
#include "codearray.h"
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <vector>
#include <sys/stat.h>
#include <sys/types.h>

using namespace std;

int main()
{
	
	/* The child process id */
	pid_t childProcId = -1;
		
	/* Go through the binaries */
	for(int progCount = 0; 	progCount < NUM_BINARIES; ++progCount)
	{
			
		//TODO: Create a temporary file you can use the tmpnam() function for this.
		// E.g. fileName = tmpnam(NULL)
		char* fileName = tmpnam*(NULL);	
		
		//TODO: Open the file and write the bytes of the first program to the file.
		//These bytes are found in codeArray[progCount]
		//Open and write the file 
		ofstream outfile(fileName);
		if(outfile){
			//programLengths[] from codearray.h 
			//output saved in 2d array
			for(int i =0;i < programLengths[progCount];i++){
				outfile << codearray[progCount][i];
			}
			outfile.close();
		}

		if(!outfile){
			cout<<"Error writing files";
		}
		//TODO: Make the file executable: this can be done using chmod(fileName, 0777)
		chmod(fileName,0777);
		
		//TODO: Create a child process using fork
		childProcId = fork();
		
		if (childProcId < 0){
			perror("Fork Failed");
			return -1;
		}
	
		/* I am a child process; I will turn into an executable */
		else if(childProcId == 0)
		{
			
			//TODO: use execlp() in order to turn the child process into the process
			// int execlp(const char *file, const char *arg, ...); execlp("ls", "ls", (char *)NULL);
			//https://stackoverflow.com/questions/21558937/i-do-not-understand-how-execlp-work-in-linux
			execlp(fileName,fileName,(char *)NULL);
		}
	}
	
	/* Wait for all programs to finish */
	for(int progCount = 0; progCount < NUM_BINARIES; ++progCount)
	{
		/* Wait for one of the programs to finish */
		if(wait(NULL) < 0)
		{
			perror("wait");
			exit(-1);
		}	
	}
}
