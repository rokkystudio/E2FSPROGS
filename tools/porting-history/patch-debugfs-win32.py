from pathlib import Path
r=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\debugfs")
f=r/"debugfs.c";t=f.read_text()
t=t.replace('unix_io_manager','default_io_manager')
t=t.replace('st.st_rdev = makedev(major, minor);', '''#ifdef _WIN32
    com_err(argv[0], 0, "mknod is not supported in native Win32 build");
    return;
#else
    st.st_rdev = makedev(major, minor);
#endif''')
f.write_text(t)
f=r/"util.c";t=f.read_text().replace('signal(SIGPIPE, SIG_IGN);','#ifndef _WIN32\n\tsignal(SIGPIPE, SIG_IGN);\n#endif')
f.write_text(t)
print('debugfs now uses default Windows I/O and console pager; Win32 mknod explicitly unsupported')
