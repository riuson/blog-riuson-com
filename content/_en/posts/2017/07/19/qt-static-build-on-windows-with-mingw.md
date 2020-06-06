{
  "title": "Qt Static Build on Windows with MinGW",
  "date": "2017-07-19 19:00:00 +0500",
  "categories": [ "Qt" ],
  "excerpt": "How to build Qt Static on Windows with MinGW to get Qt application without depencies from Qt dynamic link libraries."
}

Source: [Building a static Qt for Windows using MinGW](https://wiki.qt.io/Building_a_static_Qt_for_Windows_using_MinGW)

Download Qt and install it. Also select toolchain MinGW:

![Install](assets/images/posts/2017/07/19/qt-static-build-on-windows-with-mingw-1.png){ .img-fluid }

Remember directory, where MinGW was installed. For example **D:\Qt\Tools\mingw530_32\bin\**

Download script [windows-build-qt-static.ps1](https://sourceforge.net/p/qtlmovie/code/ci/v1.2.16/tree/build/windows-build-qt-static.ps1?format=raw).
Save it to directory **D:\Qt\**

Select Qt version from [Qt Downloads](http://download.qt.io/official_releases/qt/) and remember url for **{VERSION}/{VERSION}/single/qt-everywhere-opensource-src-{VERSION}.zip**. For example http://download.qt.io/official_releases/qt/5.9/5.9.1/single/qt-everywhere-opensource-src-5.9.1.zip

Create file **windows-build-run.bat** with content:
```bat
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\Qt\windows-build-qt-static.ps1' -QtSrcUrl 'http://download.qt.io/official_releases/qt/5.9/5.9.1/single/qt-everywhere-opensource-src-5.9.1.zip' -QtStaticDir 'D:\Qt\Static591' -MingwDir 'D:\Qt\Tools\mingw530_32' -QtVersion '5.9.1-Static'
```
where
  * -QtSrcUrl - Url to source codes archive;
  * -QtStaticDir - Directory where the static version are installed.
  * -MingwDir - Path to MinGW toolchain.

<div class="alert alert-warning" role="alert">
QtVersion string must contains no spaces!<br>
Or you can meet error like
<code><br>
ERROR: Invalid command line parameter 'Static'.<br>
mingw32-make: *** No targets specified and no makefile found.  Stop.<br>
mingw32-make: *** No rule to make target 'install'.
</code>
</div>

Run **cmd.exe**, change directory to **D:\\Qt**, start file **windows-build-run.bat**

If you see error about **SQLite**, open file **windows-build-qt-static.ps1** in editor and replace **-qt-sql-sqlite** with **-sql-sqlite**.

Wait some hours.............

Add compiled Qt to Qt Creator: **Tools** → **Options** → **Build & Run** → **Qt Versions** → **Add...**. Browse to **qmake.exe**.

![Qt Versions](assets/images/posts/2017/07/19/qt-static-build-on-windows-with-mingw-2.png){ .img-fluid }

Add new kit: **Tools** → **Options** → **Build & Run** → **Kit** → **Add...**. Select compiler C/C++ = MinGW 5.3.0, debugger = GNU gdb from MinGW 5.3.0 and just compiled Qt Version.

![Kits](assets/images/posts/2017/07/19/qt-static-build-on-windows-with-mingw-3.png){ .img-fluid }

Select kit for project:

![Kit's selection](assets/images/posts/2017/07/19/qt-static-build-on-windows-with-mingw-4.png){ .img-fluid }

After build we could see a large executable file.
