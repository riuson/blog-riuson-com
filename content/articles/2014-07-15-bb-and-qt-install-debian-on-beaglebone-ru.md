Title: BB & Qt — Установка Debian на BeagleBone
Tags: BeagleBone, Qt

Установка системы Debian 7.5 Wheezy на SD Card для загрузки BeageBone Black.
<!-- more -->

### Загрузка
Создаём каталог /home/user/beaglebone.

На [странице последних образов](http://beagleboard.org/latest-images) берём вариант Debian (BeagleBone, BeagleBone Black - 2GB SD), запускаемый без прошивки в eMMC. Скачиваем его в <i>/home/user/beaglebone/images</i>.
Получается что-то типа <i>/home/user/beaglebone/images/bone-debian-7.5-2014-05-14-2gb.img.xz</i> .

### Установка
Записываем образ на SD карту памяти, объёмом более 2 ГБ. В Ubuntu для этого есть встроенное средство - приложение Disks.

![disks]({static}/images/posts/2014/07/15/bb-and-qt-install-debian-on-beaglebone-1.png){ .img-fluid }


На SD карте должно появиться 2 раздела:
  * BEAGLE_BONE, объёмом около 100 МБ;
  * rootfs, объёмом около 1,7 ГБ.

На разделе rootfs остаются свободными около 88 МБ, чего явно будет недостаточно. Поэтому запускаем Gparted и меняем размер этого раздела так, чтобы он занимал всё остальное доступное место на карте памяти (поэтому и нужна карта объёмом более 2 ГБ).

![gparted]({static}/images/posts/2014/07/15/bb-and-qt-install-debian-on-beaglebone-2.png){ .img-fluid }

Устаналиваем карту памяти в BeagleBone. Зажимаем кнопку <i>boot</i> и подключаем USB кабелем к ПК. После чего:
  * Загружается Debian;
  * Подключается съёмный диск BEAGLE_BONE (первый раздел на карте);
  * Поверх USB создаётся новое проводное подключение с адресом 192.168.7.1, маской 255.255.255.252, широковещательным адресом 192.168.7.3;

### Связь
Теперь можно зайти по ssh. Логин debian, пароль temppwd.
```bash
$ ssh debian@192.168.7.2
Debian GNU/Linux 7

BeagleBoard.org BeagleBone Debian Image 2014-05-14

Support/FAQ: http://elinux.org/Beagleboard:BeagleBoneBlack_Debian
debian@192.168.7.2's password: temppwd
debian@beaglebone:~$
```

### Выход в интернет
[Настраиваем выход в интернет с BeagleBone через ПК по USB](http://robotic-controls.com/learn/beaglebone/beaglebone-internet-over-usb-only).

На BeagleBone:
```bash
debian@beaglebone:~$ sudo ifconfig usb0 192.168.7.2
debian@beaglebone:~$ sudo route add default gw 192.168.7.1
```
Возможно понадобится добавить строку <i>nameserver 8.8.8.8</i> в файл <i>/etc/resolv.conf</i> 

На ПК с Linux:
```bash
#eth0 интерфейс, смотрящий в интернет
#eth3 это подключение к BeagleBone по USB
$ sudo su
$ ifconfig eth3 192.168.7.1
$ iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE
$ iptables --append FORWARD --in-interface eth3 -j ACCEPT
$ echo 1 > /proc/sys/net/ipv4/ip_forward
```

Теперь можно установить какой-либо дополнительный софт. Например Midnight Commander:
```bash
debian@beaglebone:~$ sudo apt-get install mc
```

Или обновить систему:
```bash
debian@beaglebone:~$ sudo apt-get update
debian@beaglebone:~$ sudo apt-get upgrade
```

(BeagleBone Black можно приобрести на [eBay](http://cgi.ebay.com/ws/eBayISAPI.dll?ViewItem&item=261487540514))