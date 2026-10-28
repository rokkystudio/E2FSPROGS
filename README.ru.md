# E2FSPROGS — нативные инструменты ext2/ext3/ext4 для Windows

**[Русский](README.ru.md) | [English](README.en.md)**

Проект переносит открытые утилиты [e2fsprogs 1.47.3](https://github.com/tytso/e2fsprogs) на Windows x64 с помощью компилятора MinGW-w64. Готовые EXE не требуют установки MSYS2, Cygwin или их DLL.

## Утилиты

| Программа | Назначение |
| --- | --- |
| `debugfs.exe` | Просмотр и отладка ext2/ext3/ext4, чтение и извлечение файлов |
| `dumpe2fs.exe` | Сведения о суперблоке, группах и метаданных файловой системы |
| `e2fsck.exe` | Проверка файловой системы и исправление ошибок |
| `mke2fs.exe` | Создание файловой системы ext2/ext3/ext4 в образе |

**Текущая версия:** [v0.2.0-beta.2](https://github.com/rokkystudio/E2FSPROGS/releases/tag/v0.2.0-beta.2). Это экспериментальный бета-выпуск: при исправлении ошибок работайте только на копиях ценных данных. Запись в ext4 с `shared_blocks` средствами `debugfs` намеренно заблокирована до подтверждения её безопасности.

## Установка

Скачайте архив Windows x64 из [GitHub Releases](https://github.com/rokkystudio/E2FSPROGS/releases) и распакуйте его в отдельную папку. Никакие Unix-среды для запуска готовых программ не нужны.

## Примеры

```cmd
dumpe2fs.exe -h D:\images\sample.img
debugfs.exe -R "stat /example.txt" D:\images\sample.img
e2fsck.exe -fn D:\images\sample.img
```

Комбинация `-fn` выполняет проверку без автоматического исправления. Параметры записи и исправления используйте исключительно на подготовленных копиях образов.

## Структура репозитория

- `upstream/` — исходники оригинального e2fsprogs (Git-подмодуль).
- `patches/windows-port.patch` — изменения для нативной сборки Windows.
- `tests/` — интеграционные и регрессионные тесты.
- `tools/` — скрипты настройки сборки и запуска тестов.
- `docs/` — документация и отчёты о проверках.
- `build-clean/`, `build-local/`, `artifacts/` — локальные результаты, игнорируемые Git.

## Сборка на Windows

Нужны Windows x64, MinGW-w64 GCC, MSYS2 как **оболочка для сборки** и Python. Сначала получите исходники:

```cmd
git clone --recurse-submodules https://github.com/rokkystudio/E2FSPROGS.git
cd E2FSPROGS
git -C upstream apply ../patches/windows-port.patch
```

В среде MSYS2 с MinGW-w64:

```bash
export PATH=/mingw64/bin:/usr/bin:$PATH
mkdir build-clean
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

Команда `make` без выбора целей также собирает другие программы upstream, которые ещё не полностью адаптированы.

## Тесты и ограничения

На Windows прошли семь автоматических наборов тестов: создание и проверка ext4, чтение и извлечение бинарных данных, восстановление повреждений на одноразовых образах, разные размеры блоков, независимое чтение структур ext4 и отрицательные тесты. Команда на локальной машине разработки: `tools\run_beta_tests.cmd`; она ожидает собранные программы в `artifacts\beta-candidate\`.

Проверки не охватывают все функции и возможные повреждения ext4. Независимый Python-парсер поддерживает ограниченный набор структур и явно отвергает неизвестные случаи. Дополнительно: [матрица тестов](docs/TEST_MATRIX.ru.md), [Windows-only тесты](docs/WINDOWS_ONLY.ru.md).

## Лицензирование

На оригинальные исходники распространяются их лицензии GPL/LGPL и указанные в них авторские права. См. `upstream/NOTICE` и заголовки исходных файлов. При распространении бинарников требуется предоставить соответствующий исходный код и патч Windows.
