# E2FSPROGS v0.2.0-beta.2 — Windows x64

## Русский

Нативные Windows x64 утилиты **debugfs**, **dumpe2fs**, **e2fsck**, **mke2fs** на базе e2fsprogs 1.47.3. Для запуска не требуются MSYS2/Cygwin DLL.

Проверено: **7/7 автоматических тестовых наборов на Windows**, создание ext4, чтение, запись файлов и восстановление повреждений на одноразовых образах, матрица блоков 1024/2048/4096 байт, файлы до 4 МиБ, независимый Python-парсер и отрицательные тесты. Проверена статическая линковка сторонних библиотек.

**Ограничения:** работа с `shared_blocks` в режиме записи не поддерживается; `debugfs` отказывает в опасной записи. Исправление файловой системы и работа с большими образами проверены не для всех вариантов ext4. Используйте копии данных.

## English

Native Windows x64 **debugfs**, **dumpe2fs**, **e2fsck** and **mke2fs** from e2fsprogs 1.47.3. No MSYS2/Cygwin runtime DLLs are required.

Validation: **7/7 Windows-only automated test suites**, disposable ext4 creation, file read/write, corruption recovery, 1024/2048/4096-byte block sizes, files up to 4 MiB, independent Python ext4 reader and negative tests. Third-party libraries are statically linked.

**Limitations:** write operations on `shared_blocks` filesystems are unsupported and rejected by `debugfs`. Not all ext4 feature combinations, repair operations or large filesystem sizes have been independently validated. Work on copies of valuable data.

Source: https://github.com/rokkystudio/E2FSPROGS. Upstream GPL/LGPL notices and the Windows port patch are provided.
