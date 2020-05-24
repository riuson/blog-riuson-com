{
  "title": "Установка и настройка Eclipse, STM32CubeMX под Windows",
  "date": "2016-01-25 00:00:00 +0500",
  "categories": [ "STM32" ]
}

Здесь описываю настройку среды разработки для микроконтроллеров STM32, с использованием Eclipse, STM32CubeMX, GNU ARM Embedded, GNU ARM Eclipse Plugins.
На примере микроконтроллера STM32F030F4P6.

[<i class="fab fa-youtube"></i> Видео: Настройка Eclipse и STM32CubeMX под Windows](https://youtu.be/Q68PBMGceqs)
<!-- more -->

На видео приведён весь процесс установки и настройки. Операционная система Windows 10, взята с сайта Microsoft: [Download virtual machines](https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/windows/). Образы выложены там для тестирования софта под различными браузерами.

Описываемая последовательность не обязана работать на Вашем ПК, т.к. правильность настроек может зависеть от текущего окружения операционной системы. Если у Вас это не работает или найдёте ошибку, пишите в комментариях.
{: .text-warning }

# Загрузка

Список ПО, которое понадобится:

  * [Java Virtual Machine](https://www.java.com/en/download/)
  * [Eclipse IDE for C/C++ Developers](http://www.eclipse.org/downloads/)
  * [STM32CubeMX STM32Cube initialization code generator](http://www.st.com/web/catalog/tools/FM147/CL1794/SC961/SS1743/PF259242?icmp=stm32cubemx_pron_prcube_feb2014&sc=stm32cube-pr)
    * [STM32CubeMX Eclipse plug in for STM32 configuration and initialization C code generation](http://www.st.com/web/en/catalog/tools/PF257931)
    * [STM32CubeF0](http://www.st.com/web/en/catalog/tools/PF260612)
  * [GCC ARM Embedded](https://launchpad.net/gcc-arm-embedded) Windows Installer
  * [The GNU ARM Eclipse plug-ins](http://gnuarmeclipse.github.io/)
    * [How to install the GNU ARM Eclipse plug-ins?](http://gnuarmeclipse.github.io/plugins/install/) (скачивается из самого Eclipse)
    * [How to install the Windows Build Tools?](http://gnuarmeclipse.github.io/windows-build-tools/install/)
  * [Jlink - Software and documentation pack for Windows](https://www.segger.com/jlink-software.html)

# Установка

## Java Virtual Machine
Далее, далее, ... тут всё понятно.

## Eclipse IDE for C/C++ Developers
Распаковываем архив с IDE куда-нибудь.

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

## STM32CubeMX Eclipse plug in
Запускаем Eclipse. Через меню _Help_ -> _Install New Software..._ устанавливаем плагин из архива _STSW-STM32095.zip_.
Перезапускаем Eclipse.

## STM32CubeF0
Запускаем Eclipse. Открываем STM32CubeMX через меню _Window_ -> _Show View_ -> _Other..._. Там в дереве, в ветке Other, будет STM32CubeMX.
В меню STM32CubeMX выбираем _Help_ -> _Install New Libraries_, открывается окно установки пакетов под серии микроконтролллеров. Нажимаем кнопку _From Local..._ и выбираем скачанный ранее архив _STM32CubeF0.ZIP_.


## Jlink
Всё как обычно.

# Настройка

## Создание проекта в Eclipse
В мастере создания нового проекта выбираем _C/C++_ -> _C Project_.
Далее указываем имя проекта и тип _Hello World ARM C Project_, Toolchain _Cross ARM GCC_.
Далее меняем каталог исходников Source с _src_ на _Src_. В Linker semi-hosting options стираем всё и пишем 
```
--specs=nosys.specs
```

Пробуем собрать проект.

## Создание проекта в STM32CubeMX
### Генерация кода
Запускаем STM32CubeMX, создаём новый проект.
В списке микроконтроллеров выбираем нужный (здесь STM32F030F4P6 для примера).
Настраиваем как нужно.
Запускаем генерацию кода из меню. Указываем имя проекта как было в Eclipse выше. Указываем Project Location на каталог workspace, где лежит тот проект. Меняем Toolchain/IDE на SW4STM32.
Запускаем.
Исходные коды проекта будут созданысгенерированы поверх уже существующего проекта.
Закрываем STM32CubeMX.

Обновляем дерево проекта в Eclipse. Появляются новые каталоги, _Driver_ и _Inc_. Сгенерированный Src совпал с уже сушествующим.
Новые каталоги исключены из сборки, поэтому включаем их через свойства в контекстном меню.
При необходимости, меняем в свойствах проект кодировку исходников на UTF-8.

Создаём в каталоге _Src_ файл _startup.asm_. Прописывываем в нём путь к стартовому файлу на ассемблере:
```
.include "../Drivers/CMSIS/Device/ST/STM32F0xx/Source/Templates/gcc/startup_stm32f030x6.s"
```
Это позволит оставить файлы _*.s_ на месте (они не попадают под сборку ассемблером), но в то же время включить нужный в сборку через файл _*.asm_.

Ищем файл _../Drivers/STM32F0xx\_HAL\_Driver/Src/stm32f0xx\_hal\_msp\_template.c_ и исключаем его из сборки, через свойства файла.

### Перенос настроек
Далее, надо перенести настройки проекта из сгенерированного в существующий.
Открываем XML файл сгенерированного проекта в _./SW4STM32/<project name> Configuration/.cproject_.
Делаем его текст более читаемым через любое средство форматирования XML, позволяющее разнести атрибуты по строкам.

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
```
Открываем свойства проекта в Eclipse, идём в _C/C++ Build_ -> _Settings_ -> _Tool Settings_ -> _Cross ARM C Compiler_ -> _Includes_. Добавляем найденные каталоги из XML файла в список _Include paths (-I)_.
Заменяем относительные пути:
```
../../../Inc
../../../Drivers/STM32F0xx_HAL_Driver/Inc
```
на
```
${ProjDirPath}/Inc
${ProjDirPath}/Drivers/STM32F0xx_HAL_Driver/Inc
```

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
```

Открываем свойства проекта в Eclipse, идём в _C/C++ Build_ -> _Settings_ -> _Tool Settings_ -> _Cross ARM C Compiler_ -> _Preprocessor_. Добавляем найденные макросы из XML файла в список _Defined symbols (-D)_.
Список примерно следующий:
```
__weak="__attribute__((weak))"
__packed="__attribute__((__packed__))"
USE_HAL_DRIVER
STM32F030x6
ARM_MATH_CM0
```
Последнего в XML файле нет, но без него библиотеки не соберутся.

#### ARM family
Открываем свойства проекта в Eclipse, идём в _C/C++ Build_ -> _Settings_ -> _Tool Settings_ -> _Target Processor_ -> _ARM family_, выбираем _cortex-m0_, соответственно микроконтроллеру.

#### Linker script
Открываем свойства проекта в Eclipse, идём в _C/C++ Build_ -> _Settings_ -> _Tool Settings_ -> _Cross ARM C Linker_ -> _General_. Добавляем в список _Scripts files (-T)_ путь к файлу скрипта, созданного при генерации проекта в STM32CubeMX. Например, _./SW4STM32/<project name> Configuration/STM32F030F4Px\_FLASH.ld_.
Ниже, в Miscellaneous, ставим галочку на _Use newlib-nano (--specs=nano.specs)_.

# Сборка.
Собираем проект.
Для ускорения сборки можно включить параллельную работу в свойствах проекта _C/C++ Build_ -> _Behavior_ -> _Enable parallel build_.

# Отладка
## Проверка связи с отладчиком и микроконтроллером через J-Flash.
Запускаем J-Flash. Создаём новый проект. В свойствах проекта выбираем свой отладчик, _Target Interface_, _CPU_ -> _Device_. Выполняем подключение _Target_ -> _Connect_. Если в логах появилась запись 
```
- Connected successfully
```
, то всё OK. Если нет, разбираемся с драйверами и подключением.
Для дополнительной проверки можно считать память программ микроконтроллера через меню _Target_ -> _Read back_ -> _Entire chip_. Должно отобразиться содержимое памяти. Если нет - опять же разбираемся с поключением.
## Настройка Eclipse
Открываем меню _Debug_ -> _Debug Configurations..._.
Создаём новое подключение под _GDB Segger J-Link Debugging_.
На вкладке _Debugger_ прописываем _Device name_ (ссылка на список поддерживаемых устройств там есть справа), например _STM32F030F4_. Выбираем подключение _Connection_ и интерфейс _Interface_, если требуется. 
На вкладке _Common_ ставим галочку на _Debug_ в списке _Display in favorites menu_ для упрощения перехода в режим отладки.
Далее окно настроек можно закрыть и запустить отладку через меню _Debug_.
Бинарник должен прошиться в память программ и начаться отладка, с остановкой в начале функции _main_.

# Обновление проекта
Данная структура проекта позволяет обновить проект черех генератор кода STM32CubeMX без особых усилий, при соблюдении рекомендаций к написанию пользовательского кода в предназначенных для того участках.
Запускаем STM32CubeMX. Загружаем проект STM32CubeMX (файл *.ioc, сохранённый в каталоге проекта при генерации кода).
Меняем необходимые настройки, отключаем или подключаем модули.
Потом запускаем генерацию кода и файла описания.
Файлы перезаписываются поверх существующего проекта, сохраняя упомянутые выше участки пользовательского кода.


**На этом всё.**