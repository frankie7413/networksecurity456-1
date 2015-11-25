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
		char* fileName = tmpnam(NULL);	
		
		//TODO: Open the file and write the bytes of the first program to the file.
		//These bytes are found in codeArray[progCount]
		//Open and write the file 

		FILE* fp = fopen(fileName, "wb");
	
		/* Make sure the file was opened */
		if(!fp)
		{
			perror("fopen");
			exit(-1);
		}
		
		/* The arguments are as follows:
	 	 * @arg1 - the array containing the elements we would like to write to the file.
	 	 * @arg2 - the size of a single element.
	 	 * @arg3 - the number of elements to write to the file
	 	 * @arg4 - the file to which to write the bytes
	 	 * The function returns the number of bytes written to the file or -1 on error
	 	 */

	 	fwrite(codeArray, sizeof(codeArray[progCount]), sizeof(codeArray), fp);
	 	 /*
		if(fwrite(codeArray, sizeof(codeArray[progCount]), sizeof(codeArray), fp) < 0)
		{
			perror("fwrite");
			exit(-1);
		}
		*/
		/* Close the file */
		fclose(fp);

		//TODO: Make the file executable: this can be done using chmod(fileName, 0777)
		chmod(fileName, 0777);
		
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
