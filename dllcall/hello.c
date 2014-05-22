/*
 * =====================================================================================
 *
 *       Filename:  hello.c
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  2014年05月22日 11时37分08秒
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *        Company:  
 *
 * =====================================================================================
 */
#include <stdio.h>
extern "C"  {

	int  hello_void(void){
		printf("I am in hello void\n");
		return 5;
	}
}
