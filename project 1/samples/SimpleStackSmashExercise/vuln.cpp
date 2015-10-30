#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/**
 * If this function gets called, we succeed!
 */
void test()
{

	fprintf(stderr, "You did it!");
}

/* Just a pointer to store the address of test */ 
void* addr = (void*)test;

void func()
{

	
	/* Just a buffer of 3 bytes */
	char buff[] = "AAA";
	
	/**
 	 * Copy the value of the addr (the pointer to
 	 * the test() function) into the memory starting
 	 * at the offset address of buff + 24. I did this
 	 * on a 64-bit system. Here, all addresses and hence
 	 * pointers are 8 bytes (i.e. 64 bits) in size. 
 	 *
 	 * Why 24?  Our buffer is 4 bytes (3 A's +
 	 * a NULL terminator). By using "disassemble"
 	 * command in GDB, I found that although this function
 	 * does not have any other local variables, overall,
 	 * for variables, 16 bytes are allocated on the stack.  The
 	 * last byte of buff is the 16th byte of
 	 * this memory. The next element on the stack
 	 * is the old ebp register value. It's 8 bytes
 	 * long. Finally, the next element is the return
 	 * value. This is what we want. Hence, we should
 	 * write into offset 16 (highest address of the
 	 * local variable memory) + 8 (skip the old ebp) = 
 	 * 24.
 	 */  
	strncpy(buff+24, (char*)&addr, 8); 
	
	
}

int main()
{
	/* Tell us the address of test() so we know */	
	fprintf(stderr, "The address of test() is: %p\n", (void*)test); 		
	
	func();	
	
	return 0;
}
