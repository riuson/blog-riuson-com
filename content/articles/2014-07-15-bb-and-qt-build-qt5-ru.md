Title: BB & Qt — Сборка Qt 5
Date: 2014-07-15 22:02:00 +0500
Tags: Qt
Category: BeagleBone

Сборка Qt 5 для Debian и BeagleBone.

Данный материал основан на "Bare Metal Qt 5.2 on BeagleBone Black Ubuntu" [Part 1](http://armsdr.blogspot.ru/2014/01/bare-metal-qt-52-on-beaglebone-black.html?showComment=1405048695791#c8161014580628478124), [Part 2](http://armsdr.blogspot.ru/2014/01/bare-metal-qt-52-on-beaglebone-black_10.html).

**Внимание: для Qt 4.7, 4.8 процедура настройки другая.**
Её можно посмотреть, например, здесь: [Qt на BeagleBoard / BlueShark](http://we.easyelectronics.ru/rcdimon/qt-na-beagleboard---blueshark.html).

С [официального сайта](http://download.qt-project.org/) берём [qt-everywhere-opensource-src-5.2.1.tar.xz](http://download.qt-project.org/official_releases/qt/5.2/5.2.1/single/qt-everywhere-opensource-src-5.2.1.tar.xz).\
Распаковываем в /<i>home/user/Qt/qt-everywhere-opensource-src-5.2.1-armv7</i> .

Настраиваем mkspecs.
```bash
$ cd /home/user/Qt/qt-everywhere-opensource-src-5.2.1-armv7/qtbase/mkspecs/devices
$ cp -r linux-beagleboard-g++ linux-beaglebone-g++
$ nano linux-beaglebone-g++/qmake.conf
```

Меняем во флагах компилятора
```text
-mfloat-abi=softfp
```
на
```text
-mfloat-abi=hard
```

В конце файла, перед строкой load(qt_config), добавляем строки для Tslib:
```make
QMAKE_INCDIR += /usr/share/tslib-armv7/include
QMAKE_LIBDIR += /usr/share/tslib-armv7/lib
QMAKE_RPATHDIR += /usr/share/tslib-armv7/lib
```

И для ICU:
```make
QMAKE_INCDIR += /usr/share/icu-4c-53.1-armv7/include
QMAKE_LIBDIR += /usr/share/icu-4c-53.1-armv7/lib
QMAKE_RPATHDIR += /usr/share/icu-4c-53.1-armv7/lib
```

Далее:
```bash
$ cd /home/user/Qt/qt-everywhere-opensource-src-5.2.1-armv7/qtbase/mkspecs
$ cp -r linux-arm-gnueabi-g++ linux-arm-gnueabihf-g++
$ nano linux-arm-gnueabihf-g++/qmake.conf
```

Меняем путь к компилятору:
```make
# modifications to g++.conf
QMAKE_CC         = arm-linux-gnueabi-gcc
QMAKE_CXX        = arm-linux-gnueabi-g++
QMAKE_LINK       = arm-linux-gnueabi-g++
QMAKE_LINK_SHLIB = arm-linux-gnueabi-g++
```
на
```make
# modifications to g++.conf
CROSS_TOOL       = /home/user/beaglebone/gcc-linaro-arm-linux-gnueabi-4.8-2014.03_linux/bin/arm-linux-gnueabihf
QMAKE_CC         = $$CROSS_TOOL-gcc
QMAKE_CXX        = $$CROSS_TOOL-g++
QMAKE_LINK       = $$CROSS_TOOL-g++
QMAKE_LINK_SHLIB = $$CROSS_TOOL-g++
```
[Конфигурация](http://qt-project.org/doc/qt-5/configure-options.html) Qt 5.

Создаём скрипт конфигурации:
```bash
$ cd /home/user/Qt/qt-everywhere-opensource-src-5.2.1-armv7
$ touch ./start-conf.sh
$ chmod +x ./start-conf.sh
$ nano ./start-conf.sh
```
Пишем в нём:
```bash
./configure -prefix /usr/share/qt-5.2.1-armv7 -v -release -opensource -confirm-license -no-largefile -no-accessibility -nomake examples -nomake tests -qt-sql-sqlite -plugin-sql-sqlite -qt-zlib -no-gif -qt-libpng -qt-libjpeg -no-nis -no-eglfs -qpa linuxfb -no-cups -tslib -icu -xplatform linux-arm-gnueabihf-g++ -device linux-beaglebone-g++ -device-option CROSS_COMPILE=/home/user/beaglebone/gcc-linaro-arm-linux-gnueabi-4.8-2014.03_linux/bin/arm-linux-gnueabihf- -qt-pcre
```

Сохраняем (Ctrl+O, Enter) и выходим (Ctrl+X).
Дополнительные опции можно посмотреть по команде:
```bash
$ ./configure --help
```

Запускаем конфигурацию, собираем и устанавливаем:
```bash
$ ./start-conf.sh
$ make
$ sudo make install
```

Копируем каталог <i>/usr/share/qt-5.2.1-armv7</i> на BeagleBone.