Title: Утечка пользовательских данных при спользовании DfuSE Demo от STMicroelectronics 
Date: 2020-10-10 22:47:00 +0500
Tags: STM32
Summary: Будьте осторожны при публикации прошивок в формате DFU, созданных в DfuSe Demo v3.0.6

Для обновления встроенного ПО микроконтроллеров фирма STMicroelectronics реализовала встроенный загрузчик. На некоторых МК он позволяет использовать в том числе и интерфейс USB.

Документация и демонстрационное ПО верхнего уровня представлены в пакете [STSW-STM32080](https://www.st.com/en/development-tools/stsw-stm32080.html).

> STSW-STM32080 package contains all binaries and source code for DfuSe USB device firmware upgrade (DFU) software, including the demonstration, debugging GUIs and protocol layers.  
>
> It includes the DFU driver compatible with the latest Microsoft®OS.  
> DfuSe utility can be used to interact with the STM32 system memory bootloader or any In-Application Programming (IAP) firmware, running from the user Flash, thus allowing internal memories programming through USB.  
> All source files for Microsoft®Visual Studio 2012 are provided as well, to allow the customization of the default GUI interface.

Внимание, это именно **пример** ПО, а не готовые утилиты. Если вы используете их лишь как **пример** работы с загрузчиком, то проблемы для вас нет.
{: .bg-warning}

На данный момент статус продукта **ACTIVE**, версия **3.0.6**.

Создание файлов DFU демонстрируется программой под названием **DFU File Manager**.

Выбор режима работы.

![Выбор режима работы]({static}/images/posts/2020/10/10/dfu-file-manager-1.png){ .img-fluid }

Указываем короткое имя. Но можно и оставить как есть.

![Указываем имя]({static}/images/posts/2020/10/10/dfu-file-manager-2.png){ .img-fluid }

Добавляем бинарник.

![Добавлеяем бинарник]({static}/images/posts/2020/10/10/dfu-file-manager-4.png){ .img-fluid }

Сохраняем в файл DFU.

![Сохраняем в файл]({static}/images/posts/2020/10/10/dfu-file-manager-5.png){ .img-fluid }

Вроде всё работает.

Теперь открываем получившийся файл в просморщике и видим, что участок структуры, выделенный под имя образа (`char szTargetName[255]`), заполнен мусором.

Мусор этот разнообразен. Что было в тот момент в памяти, то и сохранилось.

![Мусор-1]({static}/images/posts/2020/10/10/dfu-file-manager-result-1.png){ .img-fluid }

![Мусор-2]({static}/images/posts/2020/10/10/dfu-file-manager-result-2.png){ .img-fluid }

В ST по этому поводу сказали: программа поставляется AS IS и с исходным кодом, мы её не поддерживаем.
