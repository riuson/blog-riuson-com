{
  "title": "Статическая сборка Qt на Windows с MinGW",
  "date": "2017-07-19 19:00:00 +0500",
  "categories": [ "Qt" ],
  "excerpt": "Сборка статического комплекта Qt для получения приложения без зависимостей от других библиотек Qt."
}

Оригинал: [Building a static Qt for Windows using MinGW](https://wiki.qt.io/Building_a_static_Qt_for_Windows_using_MinGW)

Загрузить и установить Qt. Не забыть выбрать набор MinGW:

![Установка](assets/images/posts/2017/07/19/qt-static-build-on-windows-with-mingw-1.png){ .img-fluid }

Запомнить каталог, куда установился MinGW. Например, **D:\Qt\Tools\mingw530_32\bin\**

Загрузить скрипт для PowerShell [windows-build-qt-static.ps1](https://sourceforge.net/p/qtlmovie/code/ci/v1.2.16/tree/build/windows-build-qt-static.ps1?format=raw).
Сохранить, например в **D:\Qt\**

Выбрать версию Qt в [Qt Downloads](http://download.qt.io/official_releases/qt/) и запомнить ссылку на неё **{Версия}/{Версия}/single/qt-everywhere-opensource-src-{Версия}.zip**. Например, http://download.qt.io/official_releases/qt/5.9/5.9.1/single/qt-everywhere-opensource-src-5.9.1.zip

Создать файл **windows-build-run.bat** со следующим содержимым:
```
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\Qt\windows-build-qt-static.ps1' -QtSrcUrl 'http://download.qt.io/official_releases/qt/5.9/5.9.1/single/qt-everywhere-opensource-src-5.9.1.zip' -QtStaticDir 'D:\Qt\Static591' -MingwDir 'D:\Qt\Tools\mingw530_32' -QtVersion '5.9.1-Static'
```
где
  * -QtSrcUrl - ссылка на архив с исходниками;
  * -QtStaticDir - каталог для установки новой статической сборки Qt;
  * -MingwDir - путь к набору MinGW.

<div class="alert alert-warning" role="alert">
Строка QtVersion не должна содержать пробелов!<br>
Иначе при сборке будет получена ошибка типа
<code><br>
ERROR: Invalid command line parameter 'Static'.<br>
mingw32-make: *** No targets specified and no makefile found.  Stop.<br>
mingw32-make: *** No rule to make target 'install'.
</code>
</div>

Запустить **cmd.exe**, перейти в каталог со скриптами, **D:\\Qt**, запустить **windows-build-run.bat**

Если выдаётся ошибка на тему **SQLite**, надо открыть файл **windows-build-qt-static.ps1** в редакторе и заменить **-qt-sql-sqlite** на **-sql-sqlite**.

Ждём несколько часов.............

Добавляем собранный Qt в Qt Creator: **Инструменты** → **Параметры** → **Сборка и запуск** → **Профили Qt** → **Добавить...**. Указать путь к файлу **qmake.exe**.

![Версии Qt](assets/images/posts/2017/07/19/qt-static-build-on-windows-with-mingw-2.png){ .img-fluid }

Добавляем новый комплект: **Инструменты** → **Параметры** → **Сборка и запуск** → **Комплекты** → **Добавить...**. Выбрать компилятор C/C++ = MinGW 5.3.0, отладчик = GNU gdb из MinGW 5.3.0 и свежесобранный профиль Qt.

![Комплекты](assets/images/posts/2017/07/19/qt-static-build-on-windows-with-mingw-3.png){ .img-fluid }

Выбрать комплект для проект:

![выбор комплекта](assets/images/posts/2017/07/19/qt-static-build-on-windows-with-mingw-4.png){ .img-fluid }

После сборки получится изрядно потолстевший исполняемый файл.
