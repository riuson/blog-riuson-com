{
  "title": "BB & Qt — Некоторые исправления",
  "date": "2014-07-18 14:30:00 +0500",
  "categories": [ "BeagleBone", "BB-View" ],
  "excerpt": "Перекраска синего пингвина и исправление некоторых конфликтов."
}

### Синий пингвин

Нужно поменять местами красный и синий цвета. Решение найдено [здесь](http://www.element14.com/community/message/108736/l/re-how-to-bb-view-on-latest-debian#108736).
Для этого открываем файл <i>/linux-dev/KERNEL/drivers/gpu/drm/drm_fb_helper.c</i>, ищем все инициализации смещения цветовых каналов и меняем местами red/blue.
```bash
--- ./drm_fb_helper.c.orig	2014-07-03 19:48:33.465438683 +0600
+++ ./drm_fb_helper.c	2014-07-18 18:52:09.336754771 +0600
@@ -603,5 +603,5 @@
 	case 8:
-		var->red.offset = 0;
-		var->green.offset = 0;
 		var->blue.offset = 0;
+		var->green.offset = 0;
+		var->red.offset = 0;
 		var->red.length = 8;
@@ -613,5 +613,5 @@
 	case 15:
-		var->red.offset = 10;
+		var->blue.offset = 10;
 		var->green.offset = 5;
-		var->blue.offset = 0;
+		var->red.offset = 0;
 		var->red.length = 5;
@@ -623,5 +623,5 @@
 	case 16:
-		var->red.offset = 11;
+		var->blue.offset = 11;
 		var->green.offset = 5;
-		var->blue.offset = 0;
+		var->red.offset = 0;
 		var->red.length = 5;
@@ -633,5 +633,5 @@
 	case 24:
-		var->red.offset = 16;
+		var->blue.offset = 16;
 		var->green.offset = 8;
-		var->blue.offset = 0;
+		var->red.offset = 0;
 		var->red.length = 8;
@@ -643,5 +643,5 @@
 	case 32:
-		var->red.offset = 16;
+		var->blue.offset = 16;
 		var->green.offset = 8;
-		var->blue.offset = 0;
+		var->red.offset = 0;
 		var->red.length = 8;
@@ -880,5 +880,5 @@
 	case 8:
-		info->var.red.offset = 0;
-		info->var.green.offset = 0;
 		info->var.blue.offset = 0;
+		info->var.green.offset = 0;
+		info->var.red.offset = 0;
 		info->var.red.length = 8; /* 8bit DAC */
@@ -890,5 +890,5 @@
 	case 15:
-		info->var.red.offset = 10;
+		info->var.blue.offset = 10;
 		info->var.green.offset = 5;
-		info->var.blue.offset = 0;
+		info->var.red.offset = 0;
 		info->var.red.length = 5;
@@ -900,5 +900,5 @@
 	case 16:
-		info->var.red.offset = 11;
+		info->var.blue.offset = 11;
 		info->var.green.offset = 5;
-		info->var.blue.offset = 0;
+		info->var.red.offset = 0;
 		info->var.red.length = 5;
@@ -909,5 +909,5 @@
 	case 24:
-		info->var.red.offset = 16;
+		info->var.blue.offset = 16;
 		info->var.green.offset = 8;
-		info->var.blue.offset = 0;
+		info->var.red.offset = 0;
 		info->var.red.length = 8;
@@ -919,5 +919,5 @@
 	case 32:
-		info->var.red.offset = 16;
+		info->var.blue.offset = 16;
 		info->var.green.offset = 8;
-		info->var.blue.offset = 0;
+		info->var.red.offset = 0;
 		info->var.red.length = 8;
```

Затем пересобираем ядро:
```bash
$ ./tools/rebuild.sh
```
Снова копируем файлы на карту памяти, загружаемся с неё и видим уже нормального Тукса.

### pin 44e10978 already requested by 4819c000.i2c
Полезная информация:
  * [BeagleBone Black Pin Mux Spreadsheet](http://www.embedded-things.com/bbb/beaglebone-black-pin-mux-spreadsheet)
  * [Building A Custom Cape](http://inspire.logicsupply.com/p/building-custom-cape.html)

При загрузке в логах можно увидеть конфликт назначения функции пина P9.20 (gpio0.12, смещение DT 0x178):
```bash
...
[    0.811465] pinctrl-single 44e10800.pinmux: pin 44e10978 already requested by 4819c000.i2c; cannot claim for gpio-leds-cape-lcd.12
[    0.823793] pinctrl-single 44e10800.pinmux: pin-94 (gpio-leds-cape-lcd.12) status -22
[    0.831988] pinctrl-single 44e10800.pinmux: could not request pin 94 on device pinctrl-single
...
```
Он используется как линия SDA в интерфейсе I2C2 на BeagleBone Black для поиска плат расширения. Каждая из них должна иметь I2C микросхему памяти с информацией о плате (см. BeagleBone Black SRM, пункт 8.2.2 - I2C Bus).

На плате BB-View место под миксрохему предусмотрено, но сама она отсутствует. А в DTS файле из Angstrom, да и в на плате BB-View, пин P9.20 обозначен как подключенный к светодиоду LED1. При попытке его инициализации как GPIO и возникает эта ошибка.

Удаляем из файла DTS упоминания о P9.20, а также некоторых других неиспользуемых здесь пинах.
```bash
--- ./BB-VIEW-LCD7-01-00A0.dts.orig	2014-07-18 18:18:59.172344896 +0600
+++ ./BB-VIEW-LCD7-01-00A0.dts	2014-07-18 18:20:11.771734973 +0600
@@ -38,21 +38,16 @@
 		"P8.29",	/* lcd: lcd_hsync */
 		"P8.28",	/* lcd: lcd_pclk */
 		"P8.30",	/* lcd: lcd_ac_bias_en */
-		"P9.27",	/* lcd: gpio3_19 */
 		"P9.12",	/* led: gpio1_28 */
 		"P9.14",	/* pwm: ehrpwm1a */
-		"P9.15",	/* keys: gpio1_16 */
-		"P9.23",	/* keys: gpio1_17 */
-		"P9.16",	/* keys: gpio1_19 */
-		"P9.21",	/* keys: gpio0_3 */
+		"P9.11",	/* keys: gpio0_30 USER3 */
+		"P9.23",	/* keys: gpio1_17 USER2 */
+		"P9.16",	/* keys: gpio1_19 USER0 */
+		"P9.24",	/* keys: gpio0_15 USER1 */
 		/* the hardware IP uses */
-		"gpio3_19",
-		"gpio1_28",
-		"gpio1_16",
+		"gpio1_28",     /* led: P9.12 */
 		"gpio1_17",
 		"gpio1_19",
-		"gpio0_3",
-		"gpio0_12",
 		"lcd",
 		"ehrpwm1a";
 
@@ -63,7 +58,6 @@
 			bb_view_lcd_cape_led_pins: pinmux_bb_view_lcd_cape_led_pins {
 				pinctrl-single,pins = <
 					0x078 0x2f      /* gpmc_be1n.gpio1_28, INPUT | PULLDIS | MODE7 */
-					0x178 0x2f	/* uart1_ctsn.gpio0_12,INPUT | PULLDIS | MODE7 */
 				>;
 			};
 
@@ -100,10 +94,10 @@
 
 			bb_view_lcd_cape_keys_pins: pinmux_bb_view_lcd_cape_keys_pins {
 				pinctrl-single,pins = <
-					0x4C 0x27	/* gpmc_a3.gpio1_19,   INPUT | MODE7 */
-					0x184 0x27	/* uart1_txd.gpio0_15, INPUT | MODE7 */
-					0x44 0x27	/* gpmc_a1.gpio1_17,   INPUT | MODE7 */
-					0x70 0x27	/* gpmc_wait0.gpio0_30,INPUT | MODE7 */
+					0x4C 0x27	/* gpmc_a3.gpio1_19    USER0, INPUT | MODE7 */
+					0x184 0x27	/* uart1_txd.gpio0_15  USER1, INPUT | MODE7 */
+					0x44 0x27	/* gpmc_a1.gpio1_17    USER2, INPUT | MODE7 */
+					0x70 0x27	/* gpmc_wait0.gpio0_30 USER3, INPUT | MODE7 */
 				>;
 			};
 
@@ -179,13 +173,6 @@
 					linux,default-trigger = "none";
 					default-state = "off";
 				};
-
-				bb_view_led1 {
-					label = "bb-view:led1";
-					gpios = <&gpio1 12 0>;
-					linux,default-trigger = "none";
-					default-state = "off";
-				};
 			};
 
 			bb_view_gpio_keys {
```
Обновляем ядро.

После загрузки можно увидеть следующие группы пинов:
```bash
debian@beaglebone:~$ sudo cat /sys/kernel/debug/pinctrl/44e10800.pinmux/pingroups
registered pin groups:
group: pinmux_userled_pins
pin 21 (44e10854)
pin 22 (44e10858)
pin 23 (44e1085c)
pin 24 (44e10860)

group: pinmux_rstctl_pins
pin 20 (44e10850)

group: pinmux_i2c0_pins
pin 98 (44e10988)
pin 99 (44e1098c)

group: pinmux_i2c2_pins
pin 94 (44e10978)
pin 95 (44e1097c)

group: pinmux_pwm_bl_pins
pin 18 (44e10848)

group: pinmux_mmc1_pins
pin 88 (44e10960)

group: pinmux_emmc2_pins
pin 32 (44e10880)
pin 33 (44e10884)
pin 0 (44e10800)
pin 1 (44e10804)
pin 2 (44e10808)
pin 3 (44e1080c)
pin 4 (44e10810)
pin 5 (44e10814)
pin 6 (44e10818)
pin 7 (44e1081c)

group: pinmux_userled_pins
pin 21 (44e10854)
pin 22 (44e10858)
pin 23 (44e1085c)
pin 24 (44e10860)

group: pinmux_bb_view_lcd_cape_led_pins
pin 30 (44e10878)

group: pinmux_bb_view_lcd_cape_pins
pin 40 (44e108a0)
pin 41 (44e108a4)
pin 42 (44e108a8)
pin 43 (44e108ac)
pin 44 (44e108b0)
pin 45 (44e108b4)
pin 46 (44e108b8)
pin 47 (44e108bc)
pin 48 (44e108c0)
pin 49 (44e108c4)
pin 50 (44e108c8)
pin 51 (44e108cc)
pin 52 (44e108d0)
pin 53 (44e108d4)
pin 54 (44e108d8)
pin 55 (44e108dc)
pin 56 (44e108e0)
pin 57 (44e108e4)
pin 58 (44e108e8)
pin 59 (44e108ec)

group: pinmux_bb_view_lcd_cape_keys_pins
pin 19 (44e1084c)
pin 97 (44e10984)
pin 17 (44e10844)
pin 28 (44e10870)
```