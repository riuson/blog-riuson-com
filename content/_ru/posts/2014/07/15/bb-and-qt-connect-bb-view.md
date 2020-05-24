{
  "title": "BB & Qt — подключение дисплея BB-View",
  "date": "2014-07-15 21:38:00 +0500",
  "categories": [ "BeagleBone", "Qt", "BB-View" ]
}

К сожалению, придётся перекомпилировать ядро. Видео будет работать сразу (за исключением порядка цветов), а вот подключение сенсорной панели не совпадает со стандартным 4-проводным интерфейсом TI.
<!-- more -->

Первоисточник:
"How-to BB-View on latest Debian"<br>
http://www.element14.com/community/thread/31051/l/how-to-bb-view-on-latest-debian
{: .p-3 .mb-2 .bg-info .text-white }

Создаём каталог <i>/home/user/beaglebone/kernel</i> и заходим в него:
```bash
$ mkdir /home/user/beaglebone/kernel
$ cd /home/user/beaglebone/kernel
```

Если на ПК **git** ещё не установлен, устанавливаем:
```bash
$ sudo apt-get install git
```

Клонируем проект **linux-dev** автора Robert Nelson. Готовьтесь к большой загрузке (~100 МБ для кросс-компилятора и ~700 МБ для исходников ядра).
```bash
$ git clone https://github.com/RobertCNelson/linux-dev.git
```

Заходим в новый каталог <i>linux-dev</i> и выбираем ветку/тег, соответствующую версии Debian.
```bash
$ cd linux-dev
$ git checkout 3.8.13-bone53 -b tmp
```

Теперь нам нужно собрать базовый образ, чтобы каталог драйверов плат расширения заполнился. Сценарий подскажет вам, если понадобится что-то сделать или доустановить.
```bash
$ ./build_kernel.sh
```
Процесс будет длиться час или около того. Наберитесь терпения...

**По состоянию на 2014-07-15:**
Скачиваем в каталог <i>/home/user/beaglebone/kernel</i> архив <i>BB-View Angstrom Source Code</i>.
Взять его можно здесь: [Expansion Board for BeagleBone family with 7 inch LCD](http://www.element14.com/community/docs/DOC-55844?ICID=beagleboneblack-bbview-learn) - [Downloads](http://www.element14.com/community/docs/DOC-55844?ICID=beagleboneblack-bbview-learn#cdownloads).

Вытаскиваем оттуда два файла:
```bash
$ unzip angstrom-source.zip
$ bzip2 -cd bb-black-kernel-3.8.13-bb-view.tar.bz2 | tar -xvf -
$ cp kernel/kernel/drivers/input/touchscreen/ti_am335x_tsc.c ../linux-dev/KERNEL/drivers/input/touchscreen/
$ cp kernel/kernel/firmware/capes/BB-VIEW-LCD7-01-00A0.dts ../linux-dev/KERNEL/firmware/capes/
```

**По состоянию на 2014-09-02:**
Скачиваем в каталог <i>/home/user/beaglebone/kernel</i> архив <i>Debian Source Code Patched for BB View</i>.
Взять его можно здесь: <a href="http://www.element14.com/community/docs/DOC-67958?ICID=beagleboneblack-bbview-software">element14: BB View LCD Cape Software Download Centre[1]</a>.

Вытаскиваем оттуда три файла:
```bash
$ unzip BB\ VIEW\ Debian\ Source\ Code.zip
$ cd BB\ VIEW\ Debian\ Source\ Code/
$ bzip2 -cd bb-black-kernel-3.8.13-bb-view.tar.bz2 | tar -xvf -
$ cp kernel/kernel/drivers/input/touchscreen/ti_am335x_tsc.c ../linux-dev/KERNEL/drivers/input/touchscreen/
$ cp kernel/kernel/include/linux/mfd/ti_am335x_tscadc.h ../linux-dev/KERNEL/include/linux/mfd/
$ cp kernel/kernel/firmware/capes/BB-VIEW-LCD7-01-00A0.dts ../linux-dev/KERNEL/firmware/capes/
```




Теперь надо включить добавленное в сборку. Открываем файл:
```bash
$ nano /home/user/beaglebone/kernel/linux-dev/KERNEL/firmware/Makefile
```

Добавляем следующую строку где-то около 192-ой (CTRL-C показывает текущую позицию курсора):
```bash
BB-VIEW-LCD7-01-00A0.dtbo \
```
Не забываем про закрывающий слеш, это важно. Теперь сохраняем и выходим, нажимая CTRL-O, Enter, CTRL-X.
Переходим обратно в корневой каталог <i>linux-dev</i>:
```bash
$ cd /home/user/beaglebone/kernel/linux-dev
```
Теперь запускаем пересборку ядра, это уже не должно занять много времени:
```bash
$ ./tools/rebuild.sh
```
В итоге получаем каталог <i>/home/user/beaglebone/kernel/linux-dev/deploy</i> .
Из него размещаем файлы на SD карте:
  * <i>deploy/config-3.8.13-bone53</i> копируем в <i>BEAGLE_BONE/config-3.8.13-bone53</i>
  * <i>deploy/3.8.13-bone53.zImage</i> копируем в <i>BEAGLE_BONE/zImage</i>
  * <i>deploy/3.8.13-bone53-dtbs.tar.gz</i> распаковываем в <i>BEAGLE_BONE/dtbs</i>
  * <i>deploy/3.8.13-bone53-firmware.tar.gz</i> распаковываем в <i>rootfs/lib/firmware/</i>
  * <i>deploy/3.8.13-bone53-modules.tar.gz</i> распаковываем в <i>rootfs/</i>

Также, надо включить поддержку этого дисплея.
Открываем файл <i>BEAGLE_BONE/uEnv.txt</i>. Где-то после строки #Disable HDMI добавляем параметры загрузки, в которых отключаем поддержку HDMI и включаем BB-View:
```bash
optargs=capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN capemgr.enable_partno=BB-VIEW-LCD7-01
```

Подключаем карту памяти к плате и загружаемся. Проверяем, что HDMI выключен (должна отсутствовать буква ...-L в списке), а BB-View включен:
```bash
debian@beaglebone:~$ cat /sys/devices/bone_capemgr.9/slots
 0: 54:PF--- 
 1: 55:PF--- 
 2: 56:PF--- 
 3: 57:PF--- 
 4: ff:P-O-L Bone-LT-eMMC-2G,00A0,Texas Instrument,BB-BONE-EMMC-2G
 5: ff:P-O-- Bone-Black-HDMI,00A0,Texas Instrument,BB-BONELT-HDMI
 6: ff:P-O-- Bone-Black-HDMIN,00A0,Texas Instrument,BB-BONELT-HDMIN
 7: ff:P-O-L Override Board Name,00A0,Override Manuf,BB-VIEW-LCD7-01
debian@beaglebone:~$ 
```
Если всё нормально... в ходе загрузки наблюдаем синего пингвина :)
Как исправить - в продолжении.

Приобрести BB-View можно на [eBay](http://www.ebay.com/itm/BB-VIEW-70-Embest-7-Inch-Lcd-Display-Cape-For-Beaglebone-/141212194989?pt=UK_BOI_Electrical_Components_Supplies_ET&hash=item20e0e718ad).