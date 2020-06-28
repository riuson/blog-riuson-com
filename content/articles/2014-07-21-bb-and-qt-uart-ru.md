Title: BB & Qt — UART
Tags: BeagleBone
Summary: Подключение UART интерфейса.

### Настройка пинов

В комплекте с исходниками ядра можно найти файлы BB-UART1-00A0.dts, BB-UART2-00A0.dts, BB-UART4-00A0.dts, BB-UART4-RTSCTS-00A0.dts, BB-UART5-00A0.dts.
Перечень задействованных в них пинов:
  * BB-UART1-00A0.dts
    * P9.24 - кнопка User1 на BB-View
    * P9.26
  * BB-UART2-00A0.dts
    * P9.21
    * P9.22
  * BB-UART4-00A0.dts
    * P9.13
    * P9.11 - кнопка User3 на BB-View
  * BB-UART5-00A0.dts
    * P8.37 - LCD Data
    * P8.38 - LCD Data

Отсюда видно, что можно задействовать UART2.
На BeagleBone открываем файл настроек окружения:
```bash
debian@beaglebone:~$ sudo nano /boot/uboot/uEnv.txt
```

Меняем ранее добавленную строку параметров на
```bash
optargs=capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN capemgr.enable_partno=BB-VIEW-LCD7-01,BB-UART2
```
Перезагружаемся.

Теперь пины подключены к UART:
```bash
sudo cat /sys/kernel/debug/pinctrl/44e10800.pinmux/pingroups
...
group: pinmux_bb_uart2_pins
pin 84 (44e10950)
pin 85 (44e10954)
...
```
В списке устройств должно появиться /dev/ttyO2.

### Проверка обмена

Подключаем к ПК через адаптер RS-232 - UART 3.3V. На ПК можно воспользоваться любым терминалом для работы с RS-232. Настраиваем на скорость 115200, 8 бит, проверки чётности нет, 1 стоп бит.

#### Проверка передачи на ПК

На BeagleBone:
```bash
debian@beaglebone:~$ sudo stty -F /dev/ttyO2 speed 115200 cs8 -cstopb -parenb
115200
debian@beaglebone:~$ echo 'Hello, World!' > /dev/ttyO2
```
На ПК должна быть принята эта строка.

#### Проверка передачи на BeagleBone
Включаем приём на плате:
```bash
debian@beaglebone:~$ cat /dev/ttyO2
```

Отправляем строку текста с ПК, заканчивающуюся /r или /n. Строка должна отобразиться в консоли BeagleBone.