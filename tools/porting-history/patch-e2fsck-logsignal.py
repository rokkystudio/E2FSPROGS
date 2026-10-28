from pathlib import Path
r=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\e2fsck")
p=r/"logfile.c";s=p.read_text()
s=s.replace('tm = (*flags & FLAG_UTC) ? gmtime_r(&ctx->now, &tm_struct) :\n\t\t\tlocaltime_r(&ctx->now, &tm_struct);','''#ifdef _WIN32
        if (*flags & FLAG_UTC) {
            tm = (gmtime_s(&tm_struct, &ctx->now) == 0) ? &tm_struct : NULL;
        } else {
            tm = (localtime_s(&tm_struct, &ctx->now) == 0) ? &tm_struct : NULL;
        }
#else
        tm = (*flags & FLAG_UTC) ? gmtime_r(&ctx->now, &tm_struct) :
            localtime_r(&ctx->now, &tm_struct);
#endif''')
s=s.replace('gethostname(buf, sizeof(buf));','''#ifdef _WIN32
        cp = getenv("COMPUTERNAME");
        snprintf(buf, sizeof(buf), "%s", cp ? cp : "windows");
#else
        gethostname(buf, sizeof(buf));
#endif''')
s=s.replace('static FILE *save_output(const char *s0, const char *s1, const char *s2)\n{','''static FILE *save_output(const char *s0, const char *s1, const char *s2)
{
#ifdef _WIN32
    /* Windows: no forked daemon. Log immediately to an accessible file. */
    FILE *f = NULL;
    if (s0 && *s0) f = fopen(s0, "w");
    if (!f && s1 && *s1) f = fopen(s1, "w");
    if (!f && s2 && *s2) f = fopen(s2, "w");
    return f;
#else''',1)
start=s.index('static FILE *save_output(')
end=s.index('\n#ifndef TEST_PROGRAM',start)
s=s[:end].rstrip()+'\n#endif /* _WIN32 */\n}\n'+s[end:] if False else s
# Insert #endif ahead of actual closing brace by indexing
start=s.index('static FILE *save_output('); end=s.index('\n#ifndef TEST_PROGRAM',start)
segment=s[start:end]; pos=segment.rfind('\n}')
assert pos!=-1;segment=segment[:pos]+'\n#endif /* _WIN32 */'+segment[pos:];s=s[:start]+segment+s[end:]
p.write_text(s)
p=r/"sigcatcher.c";s=p.read_text()
s='''#ifdef _WIN32
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
static void win32_crash_signal_handler(int signum) {
    fprintf(stderr, "e2fsck: fatal signal %d\\n", signum);
    exit(8);
}
void sigcatcher_setup(void) {
    signal(SIGSEGV, win32_crash_signal_handler);
    signal(SIGILL, win32_crash_signal_handler);
    signal(SIGFPE, win32_crash_signal_handler);
    signal(SIGABRT, win32_crash_signal_handler);
}
#else
'''+s+'\n#endif /* _WIN32 */\n';p.write_text(s)
print('log output direct on Win32, time/hostname API adjusted, Win32 C-signal crash handlers')
