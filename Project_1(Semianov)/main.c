#include <stdio.h>
#include <stdio.h>
#include <locale.h>
#include <stdlib.h>
#include <malloc.h>
#include <string.h>
int ret_int(char* s) {
	char* endptr;
	return strtol(s, &endptr, 10);
}
void git() {
	char* end;
	printf("enter the divisible\n");
	char* ch1[10000];
	fgets(ch1, 10000, stdin);
	int divisible = strtol(ch1, &end, 10);
	printf("enter the divisor\n");
	char* ch2[10000];
	fgets(ch2, 10000, stdin);
	int divisor = strtol(ch2, &end, 10);
	int prin = divisible % divisor;
	printf("the remainder of the division is %d\n", prin);
}
int main(void) {
	setlocale(LC_ALL, "");
	git();
	system("pause");
	return 0;

}