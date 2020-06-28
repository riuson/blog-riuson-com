Title: Как собрать необходимые DLL для приложения на Qt
Tags: Qt
Summary: Как собрать DLL, необходимые для работы Qt приложения с динамической линковкой.

## Как собрать динамические библиотеки, требуемые для приложения на Qt.

Исходная статья: [Qt for Windows - Deployment](http://doc.qt.io/qt-5/windows-deployment.html)

Создать простой батник *.bat со следующими командами:

```
; Добавить путь к набору MinGW в переменную окружения %PATH%.
SET PATH=%PATH%;c:\Qt\Tools\mingw530_32\bin\

; Установить путь, куда будет помещено приложение и требуемые им библиотеки
set destination=d:\projects\my-project\output\

; Путь к каталогу со скомпилированным исполняемым файлом приложения
set source=d:\projects\my-project\build-my-project-Desktop_Qt_5_9_0_MinGW_32bit-Release\release\windows\output\

; Копируем исполняемый файл
xcopy %source%my-project.exe %destination% /y

; Копируем остальные необходимые ресурсы ...
xcopy .\sources\resources\readme.md %destination% /y

; Копируем библиотеки с помощью windeployqt
c:\Qt\5.9\mingw53_32\bin\windeployqt --release --force --compiler-runtime %destination%my-project.exe
```
Запустить батник.
