---
title:  "BB & Qt — Tslib"
date:   2014-07-15 21:54:00 +0500
categories:
  - BeagleBone
  - Qt
---
Сборка Tslib для Qt.
<!-- more -->

### Сборка

Клонируем репозиторий [tslib](https://github.com/kergoth/tslib):
```bash
$ cd /home/user/beaglebone/
$ mkdir tslib
$ cd tslib
$ git clone https://github.com/kergoth/tslib.git .
```

Устанавливаем дополнительные пакеты для создания файлов конфигурации:
```bash
$ cd /home/user/beaglebone/tslib/
$ sudo apt-get install autoconf automake gettext libtool
$ ./autogen.sh
```

Создаём скрипт сборки:
```bash
$ cd /home/user/beaglebone/tslib/
$ touch build.sh
$ chmod +x build.sh
$ nano build.sh
```

С текстом:
```bash
export CC=/home/user/beaglebone/gcc-linaro-arm-linux-gnueabi-4.8-2014.03_linux/bin/arm-linux-gnueabihf-gcc
export CXX=/home/user/beaglebone/gcc-linaro-arm-linux-gnueabi-4.8-2014.03_linux/bin/arm-linux-gnueabihf-g++
export CONFIG_SITE=arm-linux.autogen
./configure --build=i386-linux --host=arm-linux --target=arm --disable-inputapi --prefix=/usr/share/tslib-armv7
make
```

Собираем и устанавливаем:
```bash
$ ./build.sh
$ sudo make install
```

Получаем каталог <i>/usr/share/tslib-armv7</i>, копируем на BeagleBone.

### Настройка и калибровка
В <i>/dev/input/</i> требуется определить, какой из event'ов относится к touchscreen.
Можно запустить, например, дамп и понажимать на панель:
```bash
debian@beaglebone:~$ sudo cat /dev/input/event1 | hexdump
```
Либо запросить инфу о каждом event'е, пока не найдётся tsc:
```bash
debian@beaglebone:~$ sudo udevadm info -n input/event1 -q path

/devices/ocp.3/44e0d000.tscadc/tsc/input/input1/event1
```

Теперь надо создать симлинк к этому event'у и разрешить доступ к нему.
Создаём в каталоге <i>/etc/udev/rules.d</i> файл <i>80-touchscreen.rules</i> с одной строкой:
```bash
KERNEL=="event1", SUBSYSTEM=="input", SUBSYSTEMS=="input", ATTRS{name}=="ti-tsc", SYMLINK+="input/touchscreen", MODE="0644"
```
и перезагружаемся. Должен появиться <i>/dev/input/touchscreen</i> с правами на чтение для всех.
<a href="http://rus-linux.net/lib.php?name=/MyLDP/sys-conf/udev.html">Инструкция по udev</a>. В Debian udevinfo заменяется на udevadm info.

Создаём в Debian скрипт калибровки:
```bash
debian@beaglebone:~$ mkdir /home/debian/test
debian@beaglebone:~$ cd /home/debian/test
debian@beaglebone:~/test$ nano ./calibr.sh
```
С текстом:
```bash
#!/bin/sh
export TSLIB_TSDEVICE=/dev/input/touchscreen
export TSLIB_CONFFILE=/etc/ts.conf
export TSLIB_CALIBFILE=/etc/pointercal2

/usr/share/tslib-armv7/bin/ts_calibrate
#/usr/share/tslib-armv7/bin/ts_test
```
Закрываем редактор. Запускаем скрипт калибровки:
```bash
debian@beaglebone:~/test$ chmod +x ./calibr.sh
debian@beaglebone:~/test$ sudo ./calibr.sh
```
В результате будет создан файл <i>/etc/pointercal2</i> с данными калибровки.
После калибровки, если в скрипте заменить ts_calibrate на ts_test, можно проверить работу touchscreen.