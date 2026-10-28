# Device validation / Проверка на устройстве — 2026-10-28

## RU

**Результат: PASS для обратимого патча Magisk.** На REDMAGIC NX709S-UN (Android 13, слот `_b`) установлен системный модуль `redmagic_camera_silence`. После перезагрузки `sys.boot_completed=1`; два пути `camera_click.ogg` указывают на бесшумный Vorbis-файл. Пользователь подтвердил: **звук затвора камеры в Telegram пропал**, устройство работает.

Это **не** испытание прямой прошивки файловых систем `system_b` или `product_b`. Физические разделы `super`, `vbmeta`, `system`, `product` не записывались. Результат Magisk-модуля не подтверждает безопасность команд `fastboot flash` или починки образов с `shared_blocks`. Оригинальные образы сохранены отдельно. Откат: удалить модуль `REDMAGIC Camera Silence` в Magisk и перезагрузить устройство.

## EN

**Result: PASS for the reversible Magisk patch.** On REDMAGIC NX709S-UN (Android 13, slot `_b`), a systemless `redmagic_camera_silence` module was installed. After reboot `sys.boot_completed=1`; both `camera_click.ogg` paths resolve to the silent Vorbis audio file. The user confirmed that **Telegram's camera shutter sound is gone** and the device is working.

This is **not** a direct `system_b`/`product_b` firmware-flashing test. No physical `super`, `vbmeta`, `system`, or `product` partitions were written. A successful Magisk overlay does not validate `fastboot flash`, repairing images with `shared_blocks`, or OTA behavior. To revert: remove the module in Magisk and reboot.
