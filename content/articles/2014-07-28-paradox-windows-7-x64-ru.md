Title: Paradox & Windows 7 x64
Tags: Windows 7
Summary: Костыли для установки этого анахронизма на Windows 7 x64.

Настройка BDE на Windows 7 x64

Идём на сайт Inno Setup.
http://www.jrsoftware.org/iskb.php?bde

Скачиваем файлы minireg.exe и bdeinst.cab.
Распаковываем bdeinst.dll из bdeinst.cab (7zip, например), устанавливаем:
```bat
$ minireg.exe bdeinst.dll
```

![bde-install]({static}/images/posts/2014/07/28/paradox-windows-7-x64-1.png){ .img-fluid }

Запускаем `C:\Program Files (x86)\Common Files\Borland Shared\BDE\BDEADMIN.EXE` из под админа.
На вкладке Configuration в дереве находим **Configuration** -> **Drivers** -> **Native** -> **Paradox**.
Путь **NET DIR** меняем на любой каталог, к которому есть полный доступ у пользователя, который будет запускать программу с БД.

![bde-admin]({static}/images/posts/2014/07/28/paradox-windows-7-x64-2.png){ .img-fluid }

Если используемая программа не может сама создать алиас к БД, на вкладке Databases добавляем алиас вручную.