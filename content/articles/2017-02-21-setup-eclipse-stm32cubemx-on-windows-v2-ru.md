Title: Установка и настройка Eclipse, STM32CubeMX под Windows (v2).
Tags: STM32

Здесь описываю настройку среды разработки для микроконтроллеров STM32, с использованием Eclipse, STM32CubeMX, GNU ARM Embedded, GNU ARM Eclipse Plugins.<br>
На примере микроконтроллера STM32F103RET6.

[<i class="fab fa-youtube"></i> Видео: Настройка Eclipse и STM32CubeMX под Windows (v2)](https://youtu.be/i5VUF1wYTQU)
<!-- more -->

В связи с некоторыми изменениями между рассмотренной ранее и текущей версией CubeMX, переделал инструкцию.{ .bg-info .text-white }

Если у Вас это не работает или найдёте ошибку, пишите в комментариях.{ .bg-warning .text-dark }

На видео приведён весь процесс установки и настройки. Операционная система Windows 10 Home.


# Загрузка

Список ПО, которое понадобится:

  * [Eclipse IDE for C/C++ Developers](http://www.eclipse.org/downloads/)
  * [Java Virtual Machine](https://www.java.com/en/download/)
  * [GCC ARM Embedded](https://launchpad.net/gcc-arm-embedded) Windows Installer
  * [How to install the Windows Build Tools?](http://gnuarmeclipse.github.io/windows-build-tools/  install/)
  * [The GNU ARM Eclipse plug-ins](http://gnuarmeclipse.github.io/)
    * [How to install the GNU ARM Eclipse plug-ins?](http://gnuarmeclipse.github.io/plugins/install/)   (скачивается из самого Eclipse)
  * [STM32CubeMX STM32Cube initialization code generator](http://www.st.com/en/development-tools/  stm32cubemx.html?icmp=stm32cubemx_pron_prcube_feb2014&sc=stm32cube-pr)
    * [STM32CubeMX Eclipse plug in for STM32 configuration and initialization C code generation](http://  www.st.com/content/st_com/en/products/development-tools/software-development-tools/  stm32-software-development-tools/stm32-configurators-and-code-generators/stsw-stm32095.html)
    * [STM32CubeF1](http://www.st.com/content/st_com/en/products/embedded-software/  mcus-embedded-software/stm32-embedded-software/stm32cube-embedded-software/stm32cubef1.html)
  * [Jlink - Software and documentation pack for Windows](https://www.segger.com/jlink-software.html)

# Установка

## Eclipse IDE for C/C++ Developers
Скачиваем установщик Eclipse и устанавливаем Eclipse IDE for C/C++ Developers.

## Java Virtual Machine
Если установщик Eclipse не найдёт Java SE Runtime Environment подходящей версии, он предложит его скачать.
Скачиваем и устанавливаем.

## Windows Build Tools
Установка описана в [руководстве](http://gnuarmeclipse.github.io/windows-build-tools/install/). Ничего необычного.

## GCC ARM Embedded
При завершения установки снимаем галочки с Launch _gccvar.bat_ и _Add path to enviroment variable_. Чтобы можно было установить несколько компиляторов.

## GNU ARM Eclipse plug-ins
Установка описана в [руководстве](http://gnuarmeclipse.github.io/plugins/install/).
В меню Eclipse выбираем _Help_ -> _Install New Software..._. Добавляем сайт

* name: GNU ARM Eclipse Plug-ins
* URL: http://gnuarmeclipse.sourceforge.net/updates

И устанавливаем всё.

Если вылетела ошибка **Handshake_failure**, читаем статью [GNU ARM Eclipse plug-ins: Received fatal alert: handshake_failure](http://gnuarmeclipse.github.io/blog/2017/01/29/plugins-install-issue).
Вкратце: повысили настройки безопасности у репозитория плагинов Eclipse, а в некоторых версиях JRE библиотеки содержат экспортные ограничения на функции шифрования. Вот их надо заменить на полные.

## STM32CubeMX Eclipse plug in
Запускаем Eclipse. Через меню _Help_ -> _Install New Software..._ устанавливаем плагин из архива _STSW-STM32095.zip_.
Перезапускаем Eclipse.

## STM32CubeF1
Запускаем Eclipse. Открываем STM32CubeMX через меню _Window_ -> _Show View_ -> _Other..._. Там в дереве, в ветке Other, будет STM32CubeMX.
В меню STM32CubeMX выбираем _Help_ -> _Install New Libraries_, открывается окно установки пакетов под серии микроконтролллеров.

Далее можно скачать пакет из сети, выбрав галочку и нажав _Install Now_.
Либо установить из скачанного вручную архива, нажав кнопку _From Local..._ и выбрав скачанный ранее архив _STM32CubeF1.ZIP_.


## J-Link
Всё как обычно.

# Настройка

## Создание проекта в Eclipse
В мастере создания нового проекта выбираем _C/C++_ -> _C Project_.
Далее указываем имя проекта и тип _Hello World ARM C++ Project_, Toolchain _Cross ARM GCC_.
Далее меняем каталог исходников Source с _src_ на _Src_. В Linker semi-hosting options стираем всё и пишем 
```
--specs=nosys.specs
```

Пробуем собрать проект.

## Создание проекта в STM32CubeMX
### Генерация кода
Запускаем STM32CubeMX, создаём новый проект.
В списке микроконтроллеров выбираем нужный (здесь STM32F103RET6 для примера).
Настраиваем как нужно.
Запускаем генерацию кода из меню. Указываем имя проекта как было в Eclipse выше. Указываем Project Location на каталог workspace, где лежит тот проект. Меняем Toolchain/IDE на SW4STM32. Снимаем галочку Generate Under Root.
Запускаем.
Исходные коды проекта будут созданысгенерированы поверх уже существующего проекта.
Закрываем STM32CubeMX.

Обновляем дерево проекта в Eclipse. Появляются новые каталоги, _Driver_ и _Inc_. Сгенерированный Src совпал с уже сушествующим.
Новые каталоги исключены из сборки, поэтому включаем их через свойства в контекстном меню.
При необходимости, меняем в свойствах проект кодировку исходников на UTF-8.

Создаём в каталоге _Src_ файл _startup.asm_. Прописывываем в нём путь к стартовому файлу на ассемблере:
```
.include "../Drivers/CMSIS/Device/ST/STM32F1xx/Source/Templates/gcc/startup_stm32f103xe.s"
```
Это позволит оставить файлы _*.s_ на месте (они не попадают под сборку ассемблером), но в то же время включить нужный в сборку через файл _*.asm_.

### Перенос настроек
Далее, надо перенести настройки проекта из сгенерированного в существующий.

Открываем проект в Eclipse. Заходим в свойства проекта - C/C++ General - Path and Symbols. Добавляем там легко опознаваемые строки-маркеры в разделы Includes и Symbols.

Далее открываем XML файл сгенерированного проекта в _./SW4STM32/<project name>/.cproject_.
Делаем его текст более читаемым через любое средство форматирования XML, позволяющее разнести атрибуты по строкам. Например, xmlbeautifier.

#### Define
Ищем в XML файле макросы, в ноде, подобной следующей:

```xml
<tool
    id="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.147826764"
    name="MCU GCC Compiler"
    superClass="fr.ac6.managedbuild.tool.gnu.cross.c.compiler">
    <option
        id="gnu.c.compiler.option.preprocessor.def.symbols.1801753735"
        name="Defined symbols (-D)"
        superClass="gnu.c.compiler.option.preprocessor.def.symbols"
        useByScannerDiscovery="false"
        valueType="definedSymbols">
        <listOptionValue
            builtIn="false"
            value="__weak=__attribute__((weak))" />
        ...
```

Ищем во втором файле ноды XML с соответствующими маркерами и заменяем их.
Список примерно следующий:
```c
__weak="__attribute__((weak))"
__packed="__attribute__((__packed__))"
USE_HAL_DRIVER
STM32F103RE
ARM_MATH_CM3
```
Последнего в XML файле нет, но без него библиотеки не соберутся.<br>
Кавычек у \__weak и \__packed тоже нет. Их надо добавить в виде ` " ` :
```c
__weak="__attribute__((weak))"
```

#### Include
Ищем в XML файле пути для Include, в ноде, подобной следующей:
```xml
<tool
    id="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.147826764"
    name="MCU GCC Compiler"
    superClass="fr.ac6.managedbuild.tool.gnu.cross.c.compiler">
    <option
        id="gnu.c.compiler.option.include.paths.976375416"
        name="Include paths (-I)"
        superClass="gnu.c.compiler.option.include.paths"
        useByScannerDiscovery="false"
        valueType="includePath">
        <listOptionValue
            builtIn="false"
            value="..\..\..\Inc" />
        ...
```
Открываем рядом файл проекта Eclipse CDT. Ищем ранее добавленные маркеры. Копируем соответствующие ноды XML из первого файла во второй. Попутно заменяя относительные пути:
```
../../../Inc
../../../Drivers/STM32F0xx_HAL_Driver/Inc
```
на
```
${ProjDirPath}/Inc
${ProjDirPath}/Drivers/STM32F0xx_HAL_Driver/Inc
```

#### ARM family
Открываем свойства проекта в Eclipse, идём в _C/C++ Build_ -> _Settings_ -> _Tool Settings_ -> _Target Processor_ -> _ARM family_, выбираем _cortex-m3_, соответственно микроконтроллеру.

#### Linker script
Копируем скрипт линкера из _./SW4STM32/<project name>/STM32F103RETx\_FLASH.ld_ в _Scripts/STM32F103RETx\_FLASH.ld_.<br>
Открываем свойства проекта в Eclipse, идём в _C/C++ Build_ -> _Settings_ -> _Tool Settings_ -> _Cross ARM C Linker_ -> _General_. Добавляем в список _Scripts files (-T)_ путь к файлу скрипта.

# Сборка.
Собираем проект.
Для ускорения сборки можно включить параллельную работу в свойствах проекта _C/C++ Build_ -> _Behavior_ -> _Enable parallel build_.

# Отладка
## Проверка связи с отладчиком и микроконтроллером через J-Flash.
Запускаем J-Flash. Создаём новый проект. В свойствах проекта выбираем свой отладчик, _Target Interface_, _CPU_ -> _Device_. Выполняем подключение _Target_ -> _Connect_. Если в логах появилась запись 
```text
- Connected successfully
```
, то всё OK. Если нет, разбираемся с драйверами и подключением.
Для дополнительной проверки можно считать память программ микроконтроллера через меню _Target_ -> _Read back_ -> _Entire chip_. Должно отобразиться содержимое памяти. Если нет - опять же разбираемся с поключением.
## Настройка Eclipse
Открываем меню _Debug_ -> _Debug Configurations..._.
Создаём новое подключение под _GDB Segger J-Link Debugging_.
На вкладке _Debugger_ прописываем _Device name_ (ссылка на список поддерживаемых устройств там есть справа), например _STM32F103RE_. Выбираем подключение _Connection_ и интерфейс _Interface_, если требуется. 
На вкладке _Common_ ставим галочку на _Debug_ в списке _Display in favorites menu_ для упрощения перехода в режим отладки.
Далее окно настроек можно закрыть и запустить отладку через меню _Debug_.
Бинарник должен прошиться в память программ и начаться отладка, с остановкой в начале функции _main_.

# Обновление проекта
Данная структура проекта позволяет обновить проект черех генератор кода STM32CubeMX без особых усилий, при соблюдении рекомендаций к написанию пользовательского кода в предназначенных для того участках.
Запускаем STM32CubeMX. Загружаем проект STM32CubeMX (файл *.ioc, сохранённый в каталоге проекта при генерации кода).
Меняем необходимые настройки, отключаем или подключаем модули.
Потом запускаем генерацию кода и файла описания.
Файлы перезаписываются поверх существующего проекта, сохраняя упомянутые выше участки пользовательского кода.


**На этом пока всё.**
