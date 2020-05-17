---
title:  "Ubuntu и Asus E35M1-M, проблема с сетью"
date:   2016-02-02 00:00:00 +0500
categories:
  - Ubuntu
---
Плата [Asus E35M1-M](https://www.asus.com/ru/Motherboards/E35M1M/) формата Micro-ATX с распаянным процессором AMD APU E-350 Dual-Core.

Проблема: ухудшение пинга со временем (с 1 мс до 10 **секунд** и далее), падение скорости, потери пакетов, отваливание сети.
<!-- more -->

Впервые столкнулся после покупки платы году так в 2012. Каким-то образом решил проблему и забыл.
Смутно припоминаю, что установил драйвера для сетевой карты из исходников.
После переустановки системы проблема всплыла снова.

# r8168

На плате встроенная поддержка сети реализуется с помощью **Realtek® 8111E , 1 x Gigabit LAN Controller(s)**.
```bash
$ lspci -v

03:00.0 Ethernet controller: Realtek Semiconductor Co., Ltd. RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller (rev 06)
	Subsystem: ASUSTeK Computer Inc. P8P67 and other motherboards
	Flags: bus master, fast devsel, latency 0, IRQ 24
	I/O ports at e000 [size=256]
	Memory at d0004000 (64-bit, prefetchable) [size=4K]
	Memory at d0000000 (64-bit, prefetchable) [size=16K]
	Capabilities: <access denied>
	Kernel driver in use: r8169
```


Раньше надо было собирать драйвер для 8111/8168 из исходников.
Сейчас в репозитории есть пакет [r8168-dkms](http://packages.ubuntu.com/wily/r8168-dkms).
После его установки контроллер работает уже с иным драйвером:
```bash
$ lspci -v

03:00.0 Ethernet controller: Realtek Semiconductor Co., Ltd. RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller (rev 06)
	Subsystem: ASUSTeK Computer Inc. P8P67 and other motherboards
	Flags: bus master, fast devsel, latency 0, IRQ 24
	I/O ports at e000 [size=256]
	Memory at d0004000 (64-bit, prefetchable) [size=4K]
	Memory at d0000000 (64-bit, prefetchable) [size=16K]
	Capabilities: <access denied>
	Kernel driver in use: r8168
```
Откатить на прежний драйвер можно удалением этого пакета через --purge.

[Bug #141343: r8169 driver does not work with Realtek "PCI-E" 8111B integrated network controller](https://bugs.launchpad.net/ubuntu/+source/linux/+bug/141343)<br/>
[The pain of an Realtek (RTL8111/RTL8168) ethernet card](https://unixblogger.wordpress.com/2011/10/18/the-pain-of-an-realtek-rtl8111rtl8168-ethernet-card/)</br>
[Realtek ethernet drivers: r8169 vs r8168](https://nelsonslog.wordpress.com/2012/01/22/realtek-ethernet-drivers-r8169-vs-r8168/)

Однако, говорят, что именно эта проблема с r8168 была закрыта. И действительно, установка этого драйвера в данном случае не помогла. Если в прошлый раз отваливалась локальная сеть, за этой сетевой картой, то теперь сеть провайдера за дискретной сетевой на базе 8139.

# ASM1083

Простеньким скриптом было обнаружено время возникновения ошибки. Между двумя этими записями:
```bash

======== 2016-02-01T02:06:34+0500 ========
64 bytes from cache.google.com (xx.xx.xx.xx): icmp_seq=1 ttl=62 time=0.998 ms
          RX packets:500253 errors:211 dropped:2370 overruns:122 frame:0
          TX packets:411349 errors:0 dropped:0 overruns:0 carrier:0
          RX bytes:393385246 (393.3 MB)  TX bytes:127926222 (127.9 MB)

======== 2016-02-01T02:07:34+0500 ========
64 bytes from cache.google.com (xx.xx.xx.xx): icmp_seq=1 ttl=62 time=99.7 ms
          RX packets:500265 errors:211 dropped:2370 overruns:122 frame:0
          TX packets:411361 errors:0 dropped:0 overruns:0 carrier:0
          RX bytes:393386290 (393.3 MB)  TX bytes:127927258 (127.9 MB)
```

В kern.log обнаружилось соответствие:
```bash
Feb  1 02:06:55 ubuntu kernel: [82015.771329] irq 18: nobody cared (try booting with the "irqpoll" option)
Feb  1 02:06:55 ubuntu kernel: [82015.771426] CPU: 0 PID: 0 Comm: swapper/0 Tainted: G           OE   4.2.0-25-generic #30-Ubuntu
Feb  1 02:06:55 ubuntu kernel: [82015.771430] Hardware name: System manufacturer System Product Name/E35M1-M, BIOS 1401 12/21/2011
Feb  1 02:06:55 ubuntu kernel: [82015.771435]  0000000000000000 e37fa07b054cf793 ffff88013ec03e28 ffffffff817e94c9
Feb  1 02:06:55 ubuntu kernel: [82015.771442]  0000000000000000 ffff880035cdf0bc ffff88013ec03e58 ffffffff810d6b65
Feb  1 02:06:55 ubuntu kernel: [82015.771447]  ffffffff81cbd600 ffff880035cdf000 0000000000000000 0000000000000012
Feb  1 02:06:55 ubuntu kernel: [82015.771452] Call Trace:
Feb  1 02:06:55 ubuntu kernel: [82015.771456]  <IRQ>  [<ffffffff817e94c9>] dump_stack+0x45/0x57
Feb  1 02:06:55 ubuntu kernel: [82015.771474]  [<ffffffff810d6b65>] __report_bad_irq+0x35/0xd0
Feb  1 02:06:55 ubuntu kernel: [82015.771479]  [<ffffffff810d6f0d>] note_interrupt+0x24d/0x290
Feb  1 02:06:55 ubuntu kernel: [82015.771484]  [<ffffffff810d432c>] handle_irq_event_percpu+0x11c/0x180
Feb  1 02:06:55 ubuntu kernel: [82015.771489]  [<ffffffff810d43d9>] handle_irq_event+0x49/0x70
Feb  1 02:06:55 ubuntu kernel: [82015.771494]  [<ffffffff810d742a>] handle_fasteoi_irq+0x9a/0x150
Feb  1 02:06:55 ubuntu kernel: [82015.771499]  [<ffffffff810172b5>] handle_irq+0x25/0x40
Feb  1 02:06:55 ubuntu kernel: [82015.771504]  [<ffffffff817f2eaf>] do_IRQ+0x4f/0xe0
Feb  1 02:06:55 ubuntu kernel: [82015.771508]  [<ffffffff817f0e2b>] common_interrupt+0x6b/0x6b
Feb  1 02:06:55 ubuntu kernel: [82015.771510]  <EOI>  [<ffffffff81060526>] ? native_safe_halt+0x6/0x10
Feb  1 02:06:55 ubuntu kernel: [82015.771522]  [<ffffffff81488261>] arch_safe_halt+0x9/0xd
Feb  1 02:06:55 ubuntu kernel: [82015.771526]  [<ffffffff814889b7>] acpi_safe_halt+0x22/0x2b
Feb  1 02:06:55 ubuntu kernel: [82015.771530]  [<ffffffff814889e0>] acpi_idle_do_entry+0x20/0x30
Feb  1 02:06:55 ubuntu kernel: [82015.771534]  [<ffffffff81488eb0>] acpi_idle_enter+0x1e8/0x21e
Feb  1 02:06:55 ubuntu kernel: [82015.771540]  [<ffffffff81687074>] cpuidle_enter_state+0xf4/0x270
Feb  1 02:06:55 ubuntu kernel: [82015.771544]  [<ffffffff81687227>] cpuidle_enter+0x17/0x20
Feb  1 02:06:55 ubuntu kernel: [82015.771548]  [<ffffffff810bd4f2>] call_cpuidle+0x32/0x60
Feb  1 02:06:55 ubuntu kernel: [82015.771552]  [<ffffffff81687203>] ? cpuidle_select+0x13/0x20
Feb  1 02:06:55 ubuntu kernel: [82015.771556]  [<ffffffff810bd788>] cpu_startup_entry+0x268/0x320
Feb  1 02:06:55 ubuntu kernel: [82015.771562]  [<ffffffff817dda2c>] rest_init+0x7c/0x80
Feb  1 02:06:55 ubuntu kernel: [82015.771568]  [<ffffffff81d50025>] start_kernel+0x48b/0x4ac
Feb  1 02:06:55 ubuntu kernel: [82015.771573]  [<ffffffff81d4f120>] ? early_idt_handler_array+0x120/0x120
Feb  1 02:06:55 ubuntu kernel: [82015.771577]  [<ffffffff81d4f339>] x86_64_start_reservations+0x2a/0x2c
Feb  1 02:06:55 ubuntu kernel: [82015.771581]  [<ffffffff81d4f485>] x86_64_start_kernel+0x14a/0x16d
Feb  1 02:06:55 ubuntu kernel: [82015.771584] handlers:
Feb  1 02:06:55 ubuntu kernel: [82015.771613] [<ffffffff815db9c0>] usb_hcd_irq
Feb  1 02:06:55 ubuntu kernel: [82015.771663] [<ffffffff815db9c0>] usb_hcd_irq
Feb  1 02:06:55 ubuntu kernel: [82015.771712] [<ffffffff815db9c0>] usb_hcd_irq
Feb  1 02:06:55 ubuntu kernel: [82015.771761] [<ffffffff815db9c0>] usb_hcd_irq
Feb  1 02:06:55 ubuntu kernel: [82015.771815] [<ffffffffc01361c0>] rtl8139_interrupt [8139too]
Feb  1 02:06:55 ubuntu kernel: [82015.771878] Disabling IRQ #18
```

Поиск по **irq "nobody cared"** прояснил, что проблема, вероятно, кроется в чипе ASM1083, используемом на данной материнской плате и на других от Asus:
[Bug 38632 - IRQ Nobody Cared on Sandybridge Additional Ethernet Card](https://bugzilla.kernel.org/show_bug.cgi?id=38632)
> [ASMedia ASM1083](http://www.asmedia.com.tw/eng/e_show_products.php?item=114)<br/>
 Engaged in High Speed I/O solution development, Asmedia Technology is committed to enlarging product portfolio with introducing PCI Express Bridge Products. **The ASM1083, x1 PCI Express to 32-bit PCI Bridge**, enables users to connect legacy parallel bus devices to the advanced serial PCI Express interface.  The ASM1083 is a PCI Express-to-PCI forward bridge, fully compliant with PCI-SIG PCI Express-to-PCI Bridge Specification1.0.
- Support PCI bus 33 MHz
- Support 3 PCI Masters
- SSC Support
- CLKRUN Support
- PME Support

Из-за некой ошибки в этом чипе, при работе с устройствами за ним (на шине PCI, которую он обеспечивает), иногда происходит сбой и всё накрывается медным тазом.
Предлагаемые решения:
 - Не подключать ничего к шине PCI, т.е. не работать с устройствами через этот мост;
 - Настроить прерывания устройств на несовпадающие номера (иногда помогает);
 - Добавить **irqpoll** в опции загрузки ядра (иногда помогает);
 - Не покупать платы с чипами от ASMedia.

Драйвера для Windows, якобы, используют именно метод irqpoll. Это хоть и делает работу более стабильной, но отрицательно сказывается на производительности.