{
  "title": "BB & Qt — Тестовое приложение",
  "date": "2014-07-16 12:05:00 +0500",
  "categories": [ "BeagleBone", "Qt" ],
  "excerpt": "Создание тестового приложения в Qt Creator с использованием ранее собранного Qt 5.2.1 для ARMv7."
}

### Консольное

В Qt Creator создаём консольное приложение bb-test-console.
При выборе комплекта выбираем Desktop Qt 5.2.1 GCC и ARMv7 Qt 5.2.1 GCC ARM.

В проекте будет всего 2 файла, bb-test-console.pro и main.cpp.
bb-test-console.pro:

```
#-------------------------------------------------
#
# Project created by QtCreator 2014-07-15T20:59:08
#
#-------------------------------------------------

QT       += core
QT       -= gui

TARGET = bb-test-console
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app

SOURCES += main.cpp
```


main.cpp приводим к следующему виду:
```cpp
#include <QCoreApplication>
#include <iostream>

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    std::cout << "Hello, World!" << std::endl;

    return 0; // a.exec();
}
```

Вибираем сборку под ARM:

![kit-selection]({{ '/assets/images/posts/2014/07/16/bb-and-qt-test-application-1.png' | relative_url }}){:class="img-fluid"}

Собираем и копируем на BeagleBone.

Проверить наличие требуемых библиотек можно командой ldd -v на устройстве:
```bash
debian@beaglebone:~/usr-share$ ldd -v bb-test-console 
	libQt5Core.so.5 => /usr/share/qt-5.2.1-armv7/lib/libQt5Core.so.5 (0xb6bed000)
	librt.so.1 => /lib/arm-linux-gnueabihf/librt.so.1 (0xb6bcf000)
	libdl.so.2 => /lib/arm-linux-gnueabihf/libdl.so.2 (0xb6bc4000)
	libpthread.so.0 => /lib/arm-linux-gnueabihf/libpthread.so.0 (0xb6ba9000)
	libstdc++.so.6 => /usr/lib/arm-linux-gnueabihf/libstdc++.so.6 (0xb6afe000)
	libm.so.6 => /lib/arm-linux-gnueabihf/libm.so.6 (0xb6a92000)
	libgcc_s.so.1 => /lib/arm-linux-gnueabihf/libgcc_s.so.1 (0xb6a6e000)
	libc.so.6 => /lib/arm-linux-gnueabihf/libc.so.6 (0xb6989000)
	libicui18n.so.53 => /usr/share/icu-4c-53.1-armv7/lib/libicui18n.so.53 (0xb6820000)
	libicuuc.so.53 => /usr/share/icu-4c-53.1-armv7/lib/libicuuc.so.53 (0xb6722000)
	/lib/ld-linux-armhf.so.3 (0xb6f62000)
	libicudata.so.53 => /usr/share/icu-4c-53.1-armv7/lib/libicudata.so.53 (0xb5291000)

	Version information:
	./bb-test-console:
		libc.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libc.so.6
		libstdc++.so.6 (CXXABI_1.3) => /usr/lib/arm-linux-gnueabihf/libstdc++.so.6
		libstdc++.so.6 (GLIBCXX_3.4) => /usr/lib/arm-linux-gnueabihf/libstdc++.so.6
		libstdc++.so.6 (CXXABI_ARM_1.3.3) => /usr/lib/arm-linux-gnueabihf/libstdc++.so.6
	/usr/share/qt-5.2.1-armv7/lib/libQt5Core.so.5:
		ld-linux-armhf.so.3 (GLIBC_2.4) => /lib/ld-linux-armhf.so.3
		librt.so.1 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/librt.so.1
		libdl.so.2 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libdl.so.2
		libm.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libm.so.6
		libgcc_s.so.1 (GCC_3.0) => /lib/arm-linux-gnueabihf/libgcc_s.so.1
		libgcc_s.so.1 (GCC_3.4) => /lib/arm-linux-gnueabihf/libgcc_s.so.1
		libgcc_s.so.1 (GCC_3.5) => /lib/arm-linux-gnueabihf/libgcc_s.so.1
		libstdc++.so.6 (CXXABI_1.3) => /usr/lib/arm-linux-gnueabihf/libstdc++.so.6
		libstdc++.so.6 (CXXABI_ARM_1.3.3) => /usr/lib/arm-linux-gnueabihf/libstdc++.so.6
		libstdc++.so.6 (GLIBCXX_3.4) => /usr/lib/arm-linux-gnueabihf/libstdc++.so.6
		libpthread.so.0 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libpthread.so.0
		libc.so.6 (GLIBC_2.7) => /lib/arm-linux-gnueabihf/libc.so.6
		libc.so.6 (GLIBC_2.9) => /lib/arm-linux-gnueabihf/libc.so.6
		libc.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libc.so.6
	/lib/arm-linux-gnueabihf/librt.so.1:
		libpthread.so.0 (GLIBC_PRIVATE) => /lib/arm-linux-gnueabihf/libpthread.so.0
		libpthread.so.0 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libpthread.so.0
		libc.so.6 (GLIBC_PRIVATE) => /lib/arm-linux-gnueabihf/libc.so.6
		libc.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libc.so.6
	/lib/arm-linux-gnueabihf/libdl.so.2:
		ld-linux-armhf.so.3 (GLIBC_PRIVATE) => /lib/ld-linux-armhf.so.3
		libc.so.6 (GLIBC_PRIVATE) => /lib/arm-linux-gnueabihf/libc.so.6
		libc.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libc.so.6
	/lib/arm-linux-gnueabihf/libpthread.so.0:
		ld-linux-armhf.so.3 (GLIBC_2.4) => /lib/ld-linux-armhf.so.3
		ld-linux-armhf.so.3 (GLIBC_PRIVATE) => /lib/ld-linux-armhf.so.3
		libc.so.6 (GLIBC_PRIVATE) => /lib/arm-linux-gnueabihf/libc.so.6
		libc.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libc.so.6
	/usr/lib/arm-linux-gnueabihf/libstdc++.so.6:
		ld-linux-armhf.so.3 (GLIBC_2.4) => /lib/ld-linux-armhf.so.3
		libgcc_s.so.1 (GCC_3.3) => /lib/arm-linux-gnueabihf/libgcc_s.so.1
		libgcc_s.so.1 (GCC_3.5) => /lib/arm-linux-gnueabihf/libgcc_s.so.1
		libgcc_s.so.1 (GCC_3.0) => /lib/arm-linux-gnueabihf/libgcc_s.so.1
		libm.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libm.so.6
		libc.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libc.so.6
	/lib/arm-linux-gnueabihf/libm.so.6:
		ld-linux-armhf.so.3 (GLIBC_PRIVATE) => /lib/ld-linux-armhf.so.3
		libc.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libc.so.6
	/lib/arm-linux-gnueabihf/libgcc_s.so.1:
		libc.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libc.so.6
	/lib/arm-linux-gnueabihf/libc.so.6:
		ld-linux-armhf.so.3 (GLIBC_2.4) => /lib/ld-linux-armhf.so.3
		ld-linux-armhf.so.3 (GLIBC_PRIVATE) => /lib/ld-linux-armhf.so.3
	/usr/share/icu-4c-53.1-armv7/lib/libicui18n.so.53:
		libstdc++.so.6 (GLIBCXX_3.4) => /usr/lib/arm-linux-gnueabihf/libstdc++.so.6
		libstdc++.so.6 (CXXABI_1.3) => /usr/lib/arm-linux-gnueabihf/libstdc++.so.6
		libc.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libc.so.6
		libgcc_s.so.1 (GCC_3.5) => /lib/arm-linux-gnueabihf/libgcc_s.so.1
		libm.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libm.so.6
	/usr/share/icu-4c-53.1-armv7/lib/libicuuc.so.53:
		libstdc++.so.6 (GLIBCXX_3.4) => /usr/lib/arm-linux-gnueabihf/libstdc++.so.6
		libstdc++.so.6 (CXXABI_1.3) => /usr/lib/arm-linux-gnueabihf/libstdc++.so.6
		libdl.so.2 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libdl.so.2
		libm.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libm.so.6
		libgcc_s.so.1 (GCC_3.5) => /lib/arm-linux-gnueabihf/libgcc_s.so.1
		libc.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libc.so.6
		libpthread.so.0 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libpthread.so.0
	/usr/share/icu-4c-53.1-armv7/lib/libicudata.so.53:
		libc.so.6 (GLIBC_2.4) => /lib/arm-linux-gnueabihf/libc.so.6
debian@beaglebone:~/usr-share$
```

Запускаем:
```bash
debian@beaglebone:~/usr-share$ ./bb-test-console 
Hello, World!
debian@beaglebone:~/usr-share$ 
```

### GUI
В Qt Creator создаём приложение QT Widgets bb-test-widgets.
При выборе комплекта выбираем Desktop Qt 5.2.1 GCC и ARMv7 Qt 5.2.1 GCC ARM.

На окне размещаем QLabel для вывода текста, и QButton для выхода из приложения.
Исходники приведены ниже.

bb-test-widgets.pro:
```
#-------------------------------------------------
#
# Project created by QtCreator 2014-07-15T21:42:00
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = bb-test-widgets
TEMPLATE = app

SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui
```
mainwindow.h:
```cpp
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

class QTimer;

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    Ui::MainWindow *ui;
    QTimer *mTimer;

private slots:
    void timerTick();
    void on_pushButtonClose_clicked();
};

#endif // MAINWINDOW_H
```

main.cpp:
```cpp
#include "mainwindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    w.setWindowState(Qt::WindowMaximized);

    return a.exec();
}
```

mainwindow.cpp:
```cpp
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QTimer>
#include <QDateTime>
#include <QScreen>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    this->mTimer = new QTimer(this);
    connect(this->mTimer, SIGNAL(timeout()), this, SLOT(timerTick()));
    this->mTimer->start(1000);

    QScreen *screen = QGuiApplication::screens().at(0);
    this->setGeometry(screen->geometry());
}

MainWindow::~MainWindow()
{
    this->mTimer->stop();
    delete this->mTimer;
    delete ui;
}

void MainWindow::timerTick()
{
    QDateTime time = QDateTime::currentDateTime();
    QScreen *screen = QGuiApplication::screens().at(0);
    QRect screenSize = screen->geometry();
    this->ui->label->setText(
                QString("%1\n%2 x %3").
                    arg(time.toString()).
                    arg(screenSize.width()).
                    arg(screenSize.height())
                );
}

void MainWindow::on_pushButtonClose_clicked()
{
    this->close();
}
```

mainwindow.ui:
```xml
<code>
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>90</width>
    <height>142</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralWidget">
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <widget class="QLabel" name="label">
      <property name="text">
       <string>TextLabel</string>
      </property>
      <property name="alignment">
       <set>Qt::AlignCenter</set>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QPushButton" name="pushButtonClose">
      <property name="text">
       <string>Закрыть</string>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menuBar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>90</width>
     <height>29</height>
    </rect>
   </property>
  </widget>
  <widget class="QToolBar" name="mainToolBar">
   <attribute name="toolBarArea">
    <enum>TopToolBarArea</enum>
   </attribute>
   <attribute name="toolBarBreak">
    <bool>false</bool>
   </attribute>
  </widget>
  <widget class="QStatusBar" name="statusBar"/>
 </widget>
 <layoutdefault spacing="6" margin="11"/>
 <resources/>
 <connections/>
</ui>
</code>
```

Здесь размер окна подгоняется под размер экрана. Каждую секунду выводится текущее время и размер экрана.
При нажатии на кнопку происходит выход из приложения.

Для запуска создаём скрипт:
```bash
debian@beaglebone:~$ cd usr-share/
debian@beaglebone:~/usr-share$ touch run.sh
debian@beaglebone:~/usr-share$ chmod +x run.sh 
debian@beaglebone:~/usr-share$ nano run.sh 
```

В нём пишем:
```bash
#!/bin/sh
export QWS_KEYBOARD=usb

export TSLIB_TSDEVICE=/dev/input/touchscreen
export TSLIB_CALIBFILE=/etc/pointercal2
export TSLIB_CONFFILE=/etc/ts.conf

#export TSLIB_PLUGINDIR=/usr/share/tslib-armv7/lib/ts
#export TSLIB_FBDEVICE=/dev/fb0
export TSLIB_CONSOLEDEVICE=none

export QT_QPA_PLATFORM=linuxfb:size=800x480:mmSize=153x91

./bb-test-widgets -platform linuxfb -plugin tslib
```

Запускаем:
```bash
debian@beaglebone:~/usr-share$ ./run.sh 
```

Если выполнять запуск по SSH, то консоль устройства не отключится. На экране поверх приложения будет мигать курсор. Также, приложение можно остановить комбинацией Ctrl+C.
При запуске с самого устройства консоль отключится, курсор исчезнет, и прервать выполнение приложения будет возможно нажатием кнопки "Закрыть" в окне (сенсорная панель уже должна быть правильно настроена), либо перезагрузкой.

### Запуск из Qt Creator
При настроенном устройстве и комплекте Qt, в параметрах Qt Creator, можно выполнять запуск (для отладки нужна поддержка python в gdb) приложения из самого Qt Creator.
Для этого надо в файл проекта добавить пару строк:
```
...
TARGET = bb-test-console
target.files = bb-test-console
target.path = /home/debian/usr-share
...
```