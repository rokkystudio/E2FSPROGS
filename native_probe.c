#include <windows.h>
#include <stdio.h>
int main(void) {
  printf("Native Windows build, compiler: MinGW-w64, process: %lu\n", (unsigned long)GetCurrentProcessId());
  return 0;
}
