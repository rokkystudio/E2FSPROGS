from pathlib import Path
r=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\e2fsck")
p=r/"ehandler.c";s=p.read_text().replace('#include <termios.h>','#ifndef _WIN32\n#include <termios.h>\n#endif').replace('#include <sys/resource.h>','#ifdef HAVE_SYS_RESOURCE_H\n#include <sys/resource.h>\n#endif');p.write_text(s)
p=r/"util.c";s=p.read_text().replace('#include "config.h"','#include "config.h"\n#ifdef _WIN32\n#define WIN32_LEAN_AND_MEAN\n#include <windows.h>\nstatic void *win32_heap_position(void) { PROCESS_MEMORY_COUNTERS dummy; (void)dummy; return NULL; }\n#endif',1)
s=s.replace('PROCESS_MEMORY_COUNTERS dummy; (void)dummy; ','')
s=s.replace('track->brk_start = sbrk(0);','#ifdef _WIN32\n\ttrack->brk_start = NULL;\n#else\n\ttrack->brk_start = sbrk(0);\n#endif')
s=s.replace('kbytes(((char *)sbrk(0)) - ((char *)track->brk_start))', '''#ifdef _WIN32
        (unsigned long long)0
#else
        kbytes(((char *)sbrk(0)) - ((char *)track->brk_start))
#endif''')
p.write_text(s)
print("Windows console/header and resource accounting guarded")
