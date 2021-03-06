Title: Hard-coded пути в QtCore.dll
Tags: Qt
Summary: Hard-coded путь qt_prfxpath в библиотеке QtCore под Windows.

После обновления Qt 5.5.0 до Qt 5.5.1 оказалось, что приложение перестало работать.
Выдаваемые ошибки:

<blockquote class="blockquote">
This application failed to start because it could not find or load the Qt platform plugin "windows".
Available platform plugins are: minimal, offscreen, windows windows.
Reinstalling the application may fix the problem.
</blockquote>

и

<blockquote class="blockquote">
Microsoft Visual C++ Runtime Library
Runtime Error!
This application has requested the Runtime to terminate it in an unusual way.
Please contact the application's support team for more information.
</blockquote>

![QtCore Failure 1]({static}/images/posts/2016/01/09/qtcore-hard-coded-paths-1.png){ .img-fluid }

![QtCore Failure 2]({static}/images/posts/2016/01/09/qtcore-hard-coded-paths-2.png){ .img-fluid }

Поиск недостающих зависимостей в dependency walker ничего не дал. Нужные пакеты MS VC++ Redistibutable установлены..

Скачал прежнюю версию Qt, 5.5.0, но случайно установил её не в *D:\Qt*, а в *C:\Qt* (по умолчанию). Копирование библиотек из этой установки в каталог к приложению привёл его в рабочее состояние.

По объёму и версии библиотеки оказались идентичные. В сравнении содержимого обнаружилось отличие:

![QtCore Compare]({static}/images/posts/2016/01/09/qtcore-hard-coded-paths-3.png){ .img-fluid }

Библиотека QtCore5.dll содержит в себе строку пути **qt_prfxpath** к месту установки библиотеки Qt на компьютере разработчика.

В багтрекере обнаружился следующий тикет: [QtQTBUG-31760 Local path information is baked into Qt5Core.dll causing very hard to reproduce crashes](https://bugreports.qt.io/browse/QTBUG-31760)

В качестве решения предлагают задействовать [qt.conf](http://doc.qt.io/qt-5/qt-conf.html) для переопределения путей.