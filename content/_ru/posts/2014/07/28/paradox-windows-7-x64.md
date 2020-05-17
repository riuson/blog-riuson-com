---
title:  "Paradox & Windows 7 x64"
date:   2014-07-28 00:00:00 +0500
categories:
  - "Windows 7"
excerpt: Костыли для установки этого анахронизма на Windows 7 x64.
---
Настройка BDE на Windows 7 x64

Идём на сайт Inno Setup.
http://www.jrsoftware.org/iskb.php?bde

Скачиваем файлы minireg.exe и bdeinst.cab.
Распаковываем bdeinst.dll из bdeinst.cab (7zip, например), устанавливаем:
```bash
$ minireg.exe bdeinst.dll
```

![bde-install]({{ '/assets/images/posts/2014/07/28/paradox-windows-7-x64-1.png' | relative_url }}){:class="img-fluid"}

Запускаем `C:\Program Files (x86)\Common Files\Borland Shared\BDE\BDEADMIN.EXE` из под админа.
На вкладке Configuration в дереве находим **Configuration** -> **Drivers** -> **Native** -> **Paradox**.
Путь **NET DIR** меняем на любой каталог, к которому есть полный доступ у пользователя, который будет запускать программу с БД.

![bde-admin]({{ '/assets/images/posts/2014/07/28/paradox-windows-7-x64-2.png' | relative_url }}){:class="img-fluid"}

Если используемая программа не может сама создать алиас к БД, на вкладке Databases добавляем алиас вручную.