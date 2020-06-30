Title: BB & Qt — Установка Qt Creator
Date: 2014-07-15 01:00:00 +0500
Tags: Qt
Category: BeagleBone

Подготовка Qt Creator для сборки проектов под BeagleBone.

### Установка
Для установки Qt Creator берём [Qt Online Installer](http://qt-project.org/downloads). С его помощью загружаем Tools и Qt 5.2.1 gcc 32/64 bit.

![qt-maintenance-tool]({static}/images/posts/2014/07/15/bb-and-qt-setup-qt-creator-1.png){ .img-fluid }


Далее запускаем свежеустановленный Qt Creator.

### Добавление устройства
Открываем меню Иструменты -> Параметры -> Устройства.
Добавляем новое "Обычное Linux-устройство", называем его "BeagleBone Black - Debian".
Хост 192.168.7.2, авторизация по паролю, логин debian, пароль temppwd.

![device]({static}/images/posts/2014/07/15/bb-and-qt-setup-qt-creator-2.png){ .img-fluid }

### Добавление комплекта
Открываем меню Иструменты -> Параметры -> Сборка и запуск.

На вкладке Отладчики добавляем новый отладчик Linaro GDB ARM Python, указывая путь к ранее собранному Linaro GDB:
<i>/home/user/beaglebone/gdb-linaro-7.6-2013.05/bin/arm-elf-linux-gnueabihf-gdb</i>

![gdb]({static}/images/posts/2014/07/15/bb-and-qt-setup-qt-creator-3.png){ .img-fluid }

На вкладке Компиляторы добавляем новый кросс-компилятор Linaro GCC ARMv7, указывая путь к копилятору:
<i>/home/user/beaglebone/gcc-linaro-arm-linux-gnueabi-4.8-2014.03_linux/arm-linux-gnueabihf/bin/g++</i>

![compiler]({static}/images/posts/2014/07/15/bb-and-qt-setup-qt-creator-4.png){ .img-fluid }

На вкладке Профили Qt добавляем новый профиль Qt 5.2.1 (armv7), указывая путь к qmake, из собранного ранее Qt 5.2.1 для ARMv7:
<i>/usr/share/qt-5.2.1-armv7/bin/qmake</i>

![profile]({static}/images/posts/2014/07/15/bb-and-qt-setup-qt-creator-5.png){ .img-fluid }

На вкладке комплекты добавляем новый комплект ARMv7 Qt 5.2.1 GCC ARM, указывая созданные выше компилятор Linaro GCC ARMv7, профиль Qt и устройство:

![kit]({static}/images/posts/2014/07/15/bb-and-qt-setup-qt-creator-6.png){ .img-fluid }

Подтверждаем и закрываем.