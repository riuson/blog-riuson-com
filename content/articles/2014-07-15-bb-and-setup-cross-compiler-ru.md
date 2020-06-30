Title: BB & Qt — Кросс-компилятор
Date: 2014-07-15 21:50:00 +0500
Tags: Qt
Category: BeagleBone

Установка кросс-компилятора.

Операционная система на компьютере - [Ubuntu 14.04 LTS x64](http://releases.ubuntu.com/14.04/).
На BeagleBone Black - Debian 7.5 Wheezy.

### 32-битные библиотеки
Начиная с Ubuntu 13.10 выпилен пакет ia32-libs. Поэтому команда 
```bash
$ sudo apt-get install ia32-libs
```
уже не пройдёт.

Устанавливаем библиотеки как объяснено [здесь](http://www.linuxrussia.com/2014/02/32-libs-ubuntu.html) и [здесь](http://gnuarmeclipse.livius.net/blog/toolchain-install/).
```bash
$ sudo dpkg --add-architecture i386
$ sudo apt-get update 

$ sudo apt-get install libc6:i386 libstdc++6:i386
$ sudo apt-get install lib32z1 lib32ncurses5 lib32bz2-1.0
```

### Компилятор

В качестве кросс-компилятора берём [Linaro GCC](https://launchpad.net/gcc-linaro/).
У компилятора из репозитория Ubuntu версия libc выше используемой в Debian, программа на устройстве не запустится.

Скачиваем и распаковываем бинарники компилятора в какой-нибудь каталог, например:
<i>/home/user/beaglebone/gcc-linaro-arm-linux-gnueabi-4.8-2014.03_linux</i>

### Отладчик

Для Qt Creator понадобится gdb с поддержкой python.

Скачиваем исходники [Linaro GDB](https://launchpad.net/gdb-linaro/+download).
Распаковываем в <i>/home/user/beaglebone/gdb-linaro-7.6-2013.05-sources</i>
Собираем:
```bash
$ cd /home/user/beaglebone/gdb-linaro-7.6-2013.05-sources
~/beaglebone/gdb-linaro-7.6-2013.05-sources$ ./configure --target=arm-elf-linux-gnueabihf --prefix=/home/user/beaglebone/gdb-linaro-7.6-2013.05
~/beaglebone/gdb-linaro-7.6-2013.05-sources$ make -j 2
~/beaglebone/gdb-linaro-7.6-2013.05-sources$ make install
```
GDB будет установлен в каталог <i>/home/user/beaglebone/gdb-linaro-7.6-2013.05</i>. Поддержа python должна включиться автоматически.
