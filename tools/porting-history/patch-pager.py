from pathlib import Path
f=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\lib\ss\pager.c")
t=f.read_text()
t=t.replace('#include "ss_internal.h"', '#include "ss_internal.h"\n#ifdef _WIN32\n#include <io.h>\n#endif')
t=t.replace('if ((getuid() != geteuid()) || (getgid() != getegid()))', 'if (\n#ifndef _WIN32\n    (getuid() != geteuid()) || (getgid() != getegid())\n#else\n    0\n#endif\n    )')
t=t.replace('#ifndef NO_FORK\nint ss_pager_create', '#if defined(_WIN32)\nint ss_pager_create(void) { return _dup(_fileno(stdout)); }\n#elif !defined(NO_FORK)\nint ss_pager_create')
t=t.replace('void ss_page_stdin(void)\n{','''#ifdef _WIN32
void ss_page_stdin(void)
{
    char buffer[4096];
    int n;
    while ((n = _read(0, buffer, sizeof(buffer))) > 0)
        if (_write(1, buffer, n) != n) break;
}
#else
void ss_page_stdin(void)
{''')
t += '\n#endif /* _WIN32 ss_page_stdin */\n'
f.write_text(t)
print('patched pager Win32 console fallback')
