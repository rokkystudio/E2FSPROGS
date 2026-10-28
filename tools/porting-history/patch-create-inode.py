from pathlib import Path
f=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\misc\create_inode.c")
s=f.read_text()
needle='#include "config.h"'
assert needle in s
s=s.replace(needle,'''#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <errno.h>
#ifndef S_ISLNK
#define S_ISLNK(x) 0
#endif
/* Windows reparse points are not treated as ordinary files. */
static int win32_lstat_file(const char *path, struct stat *st);
#define lstat win32_lstat_file
#endif
#include "config.h"''',1)
needle='#include "create_inode_libarchive.h"'
assert needle in s
s=s.replace(needle,needle+'''
#ifdef _WIN32
static int win32_lstat_file(const char *path, struct stat *st)
{
    DWORD a = GetFileAttributesA(path);
    if (a == INVALID_FILE_ATTRIBUTES)
        return -1;
    if (a & FILE_ATTRIBUTE_REPARSE_POINT) {
        errno = EOPNOTSUPP;
        return -1;
    }
    return stat(path, st);
}
#endif
''',1)
f.write_text(s)
print("Windows host directory import refuses reparse points")
