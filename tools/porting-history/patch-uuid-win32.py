from pathlib import Path
f=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\lib\uuid\gen_uuid.c")
s=f.read_text()
s=s.replace('#include "uuidP.h"', '#ifdef _WIN32\n#define WIN32_LEAN_AND_MEAN\n#include <windows.h>\n#include <bcrypt.h>\n#endif\n#include "uuidP.h"')
s=s.replace('^ getuid() ^ tv.tv_sec', '^ tv.tv_sec')
needle='static void get_random_bytes(void *buf, int nbytes)\n{'
replacement='''static void get_random_bytes(void *buf, int nbytes)
{
#ifdef _WIN32
    if (nbytes <= 0) return;
    if (BCryptGenRandom(NULL, (PUCHAR)buf, (ULONG)nbytes, BCRYPT_USE_SYSTEM_PREFERRED_RNG) != 0)
        abort();
    return;
#else'''
assert needle in s
s=s.replace(needle,replacement,1)
mark='\n\treturn;\n}\n\n/*\n * Get the ethernet'
assert mark in s
s=s.replace(mark,'\n\treturn;\n#endif /* _WIN32 */\n}\n\n/*\n * Get the ethernet',1)
f.write_text(s)
print('Windows secure RNG patch applied with WIN32_LEAN_AND_MEAN')
