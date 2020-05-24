{
  "title": "Debian на BB + BB-View, мануал от element14",
  "date": "2015-05-20 00:00:00 +0500",
  "categories": [ "BB-View", "BeagleBone" ]
}

* [BeagleBone Black & BB-View Demo](http://www.element14.com/community/community/designcenter/single-board-computers/next-gen_beaglebone/blog)<br>
Отсюда берём Debian patch files, по указанной там ссылке: [element14: BB View LCD Cape Software Download Centre[1]](http://www.element14.com/community/docs/DOC-67958/l/element14-bb-view-lcd-cape-software-download-centre1?ICID=beagleboneblack-bbview-software). Файл называется [Debian Image (Patched for BB-View)](http://downloads.element14.com/downloads/bb-view/BB%20VIEW%20Debian%20Image.zip?COM=BeagleBoneBlack).
<!-- more -->

* [Beaglebone Black with the BBView and the new Beaglebone Debian image](http://www.element14.com/community/community/designcenter/single-board-computers/next-gen_beaglebone/blog/2015/05/20/beaglebone-black-with-the-bbview-and-the-new-beaglebone-debian-image)<br>
По инструкциям здесь записываем Debian на SD карту. Затем распаковываем на карту, в папку /home/debian/bbview, содержимое указанного выше архива Debian image, дабы потом вытаскивать эти файлы сразу с SD, без монтирования внешней USB флэшки.

<span class="text-success"><b>Работает.</b></span>
