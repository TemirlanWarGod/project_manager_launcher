#include <stdio.h>
#include <locale.h>
#include <stdlib.h>
#include <malloc.h>
#include <string.h>
int ret_int(char *s) {
	char* endptr;
	return strtol(s, &endptr, 10);
}
void git() {
	printf("enter the terms(Write 'end' when you're done)\n");
	char* vvod[10000];
	fgets(vvod, 10000, stdin);
	int prin = 0;
	for (; strcmp(vvod, "end\n") != 0; fgets(vvod, 10000, stdin)) {
		prin += ret_int(vvod);
	}
	printf(the amount is equal to "%d", prin);
}
int main(void) {
	setlocale(LC_ALL, "");
	git();
	return 0;
}
