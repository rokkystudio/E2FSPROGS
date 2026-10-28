from pathlib import Path
f=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\lib\ss\help.c")
s=f.read_text()
start=s.index('    switch (child = fork()) {')
end=s.index('\n}',start)
replacement='''#ifdef _WIN32
    /* Native Win32: display the help file directly; no Unix fork/pager. */
    {
        char page_buf[8192];
        int bytes_read;
        while ((bytes_read = read(fd, page_buf, sizeof(page_buf))) > 0) {
            size_t sent = 0;
            while (sent < (size_t)bytes_read) {
                int n = fwrite(page_buf + sent, 1, (size_t)bytes_read - sent, stdout);
                if (n <= 0) break;
                sent += (size_t)n;
            }
        }
        close(fd);
    }
#else
'''+s[start:end]+'''
#endif'''
s=s[:start]+replacement+s[end:]
f.write_text(s)
print("patched",f)
