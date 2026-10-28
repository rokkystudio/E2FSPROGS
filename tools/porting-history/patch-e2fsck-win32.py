from pathlib import Path
p=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\e2fsck\unix.c")
s=p.read_text().replace('unix_io_manager','default_io_manager')
start=s.index('static int is_on_batt(void)\n{')
end=s.index('\n}',start)+2
func=s[start:end]
s=s[:start]+'''static int is_on_batt(void)
{
#ifdef _WIN32
    return 0; /* No Linux /proc power supply information in Windows. */
#else'''+func[len('static int is_on_batt(void)\n{'): -1]+'''
#endif
}'''+s[end:]
s=s.replace('#ifdef HAVE_SIGNAL_H\n\tstruct sigaction\tsa;', '#if defined(HAVE_SIGNAL_H) && !defined(_WIN32)\n\tstruct sigaction\tsa;')
s=s.replace('#ifdef HAVE_SIGNAL_H\n\t/*\n\t * Set up signal action', '#if defined(HAVE_SIGNAL_H) && !defined(_WIN32)\n\t/*\n\t * Set up signal action')
p.write_text(s)
print('Windows battery and signal guard adjustments completed')
