Title: Qt Deploy on Windows
Tags: Qt
Summary: How to collect DLLs, what are required to run Qt application with dinamic linking.

## How to deploy dynamically linked application with DLLs.

Source article: [Qt for Windows - Deployment](http://doc.qt.io/qt-5/windows-deployment.html)

Create simple Windows Batch file *.bat with commands:

```bat
; Add path to MinGW tools to %PATH% environment variable.
SET PATH=%PATH%;c:\Qt\Tools\mingw530_32\bin\

; Set output path for application and DLLs
set destination=d:\projects\my-project\output\

; Path to directory with executable file of application
set source=d:\projects\my-project\build-my-project-Desktop_Qt_5_9_0_MinGW_32bit-Release\release\windows\output\

; Copy executable file
xcopy %source%my-project.exe %destination% /y

; Copy other necessary resources ...
xcopy .\sources\resources\readme.md %destination% /y

; Run windeployqt
c:\Qt\5.9\mingw53_32\bin\windeployqt --release --force --compiler-runtime %destination%my-project.exe
```
Run batch file.
