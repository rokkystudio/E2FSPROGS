# E2FSPROGS v0.2.0-beta.1 — Windows x64 (beta preview)

## Русский
- Нативные `debugfs.exe`, `dumpe2fs.exe`, `e2fsck.exe` и `mke2fs.exe`; MinGW-w64, импорт только системных DLL Windows.
- **7 из 7 наборов Windows-only тестов PASS:** форматирование, проверка и восстановление одноразовых ext4, бинарные файлы до 4 МиБ, независимый Python-парсер, отрицательные тесты, отказ от записи `shared_blocks`.
- Подтверждена успешная загрузка REDMAGIC с отдельным Magisk-модулем и исчезновение звука затвора в Telegram.
- **Ограничение:** Magisk-патч — не прямая прошивка ext4. Запись и ремонт реальных Android `shared_blocks` и AVB/dm-verity **не сертифицированы**. Не используйте для прошивки важных разделов.
- Чистая выборочная сборка четырёх целевых программ прошла на Windows; полная сборка дополнительных upstream-программ не завершена.

## English
- Native Windows `debugfs.exe`, `dumpe2fs.exe`, `e2fsck.exe`, `mke2fs.exe`, using MinGW-w64 with Windows-only runtime imports.
- **7/7 Windows-only suites PASS:** disposable ext4 formatting, repair and checks, binary files up to 4 MiB, independent Python verifier, negative tests, and `shared_blocks` write refusal.
- REDMAGIC successfully rebooted with a separate Magisk overlay; the user confirmed Telegram's shutter sound is gone.
- **Scope:** systemless Magisk overlay success does **not** prove direct firmware flashing safety. Android `shared_blocks` mutation and AVB/dm-verity remain unqualified.
- Four selected programs build in the independent Windows build tree; other upstream programs are not fully ported.

Sources: https://github.com/rokkystudio/E2FSPROGS — clone with `--recurse-submodules`, apply `patches/windows-port.patch`. Upstream GPL/LGPL license notices apply.
