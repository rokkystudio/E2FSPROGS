# E2FSPROGS — нативные ext2/ext3/ext4-утилиты для Windows

[Русский](README.ru.md) | [English](README.en.md)

Порт [e2fsprogs 1.47.3](https://github.com/tytso/e2fsprogs) под Windows x64 на MinGW-w64. Исполняемые файлы используют только системные DLL Windows, не требуют среды MSYS2/Cygwin для запуска.

## Возможности

| Утилита | Назначение | Проверенный статус |
| --- | --- | --- |
| `debugfs.exe` | Просмотр и извлечение файлов ext2/3/4; изменение тестовых образов | Пройдено чтение и бинарное извлечение |
| `dumpe2fs.exe` | Суперблок и метаданные ext4 | Проверено |
| `e2fsck.exe` | Проверка и исправление файловой системы | Проверено на одноразовых тестовых образах |
| `mke2fs.exe` | Форматирование нового ext4-образа | Проверено на ограниченной матрице; ещё не в опубликованной альфе |

**Статус:** кандидат в бета-версию, а не выпуск для критичных данных. Запись на Android-разделы и прошивка **не разрешены** тестами. Для ext4 с `shared_blocks` необходимы дополнительные гарантии.

## Установка

Опубликованный архив [v0.1.0-alpha.1](https://github.com/rokkystudio/E2FSPROGS/releases/tag/v0.1.0-alpha.1) содержит предыдущие три утилиты. Свежая четырёхкомпонентная сборка пока существует только как локальный кандидат на ASHOT, в каталоге `artifacts/beta-candidate/`. Не смешивайте бинарники разных версий.

## Использование (без записи)

```bat
dumpe2fs.exe -h C:\images\test.img
debugfs.exe -R "stat /path/to/file" C:\images\test.img
e2fsck.exe -fn C:\images\test.img
```

`-fn` отключает исправление. Перед любой работой с важными данными сделайте отдельную копию и зафиксируйте SHA-256. **Никогда не выполняйте `e2fsck -y` или `debugfs -w` на единственном экземпляре образа.**

## Структура репозитория

- `upstream/` — Git-подмодуль оригинального e2fsprogs;
- `patches/windows-port.patch` — наши переносы и исправления;
- `tools/configure_win32_makefiles.py` — настройки линковки с Windows-библиотеками;
- `tests/` — одноразовые интеграционные и регрессионные тесты;
- `docs/` — подробная документация и контрольные списки;
- `build-clean/`, `build-local/`, `artifacts/` — локальные, исключённые из Git результаты сборок.

## Сборка и тестирование

```bat
git clone --recurse-submodules https://github.com/rokkystudio/E2FSPROGS.git
cd E2FSPROGS
git -C upstream apply ..\patches\windows-port.patch
```

Для сборки требуется MSYS2 **как среда сборки**, MinGW-w64 GCC и Python. После настройки из MSYS2:

```bash
mkdir -p build-clean
cd build-clean
../upstream/configure --build=x86_64-w64-mingw32 --host=x86_64-w64-mingw32 --disable-nls --disable-uuidd --disable-tls --disable-tdb --disable-mmp CC=/mingw64/bin/gcc
python ../tools/configure_win32_makefiles.py .
make -C lib/ext2fs -j4
make -C lib/blkid -j4
make -C lib/support -j4
make -C debugfs -j4
make -C misc mke2fs dumpe2fs -j4
make -C e2fsck -j4
```

Пока гарантирована только целевая сборка указанных утилит: общий `make -j4` дополнительно собирает `tune2fs`, для которого портирование не завершено.

На компьютере ASHOT прогон тестов: `tools\run_beta_tests.cmd`. Скрипт проверяет именно EXE из `artifacts\beta-candidate`; его тестовые образы автоматически удаляются.

## Проверки и ограничения

Тесты прошли на ext4-образах 16–256 МиБ, с блоками 1024/2048/4096 байт, на бинарных файлах до 4 МиБ; также проверены обнаружение повреждений и восстановление счетчика ссылок inode и суперблока. Это не покрывает все размеры, функции ext4 или Android.

Для прошивки REDMAGIC обязательны проверка `shared_blocks`, анализ AVB/dm-verity, подтверждённые резервные копии и практически проверенный план восстановления. См. [критерии беты и прошивки](docs/BETA_CHECKLIST.ru.md) и [результаты тестов](docs/TEST_MATRIX.ru.md).

## Лицензии

Сохраняются исходные лицензии GPL/LGPL и уведомления о правах e2fsprogs — в частности `upstream/NOTICE` и заголовки исходных файлов. При распространении бинарников должен быть доступен соответствующий исходный код вместе с Windows-патчем.

## Windows-only qualification / Квалификация Windows-only

[Проверки без Linux](docs/WINDOWS_ONLY.ru.md). MSYS2 используется только во время сборки.
