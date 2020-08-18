Title: GCC, Windows и длинные команды
Date: 2020-08-18 18:00:00 +0500
Tags: STM32
Summary: Как обойти ограничение на длину команды при сборке проекта с GCC под управлением Windows.

## Проблема

С увеличением количества файлов в проекте, собираемом с использованием GCC под Windows, однажды можно получить подобную ошибку:

```text
arm-none-eabi-g++ <прочие параметры> <100500 объектных файлов...> 
collect2.exe: fatal error: CreateProcess: No such file or directory
compilation terminated.
make[1]: *** [Makefile:140: Output/ReleaseApp/myapplication.elf] Error 1
make[1]: Leaving directory 'D:/projects/Embedded/myapplication'
make: *** [Makefile:70: all] Error 2
The terminal process "cmd.exe /C make -j4 all CONF=ReleaseApp" terminated with exit code: 2.
```

Причиной является ограничение на длину команды в Windows.

[What is the command line length limit? [devblogs.microsoft.com]](https://devblogs.microsoft.com/oldnewthing/20031210-00/?p=41553)

При выполнении команды через cmd.exe команда ограничена **8192** символами. При выполнении команды через функцию `CreateProcess`, ограничение (из-за структуры [UNICODE_STRING](https://docs.microsoft.com/en-us/windows/win32/api/subauth/ns-subauth-unicode_string)) составляет **32767** символов. Вроде бы много. Но с линкером, принимающим список объектных файлов через аргументы командной строки, достигнуть такой величины - не проблема.

## Варианты решения

### xPack Windows Build Tools

<https://xpack.github.io/windows-build-tools>

Позволяет обойти ограничение на длину 8192 символа при сборке проктов под Windows тем, что не использует `cmd.exe` для запуска процессов.

### Сокращение путей к файлам

Объектные файлы перечисляются в аргументах c указанием путей к ним
```text
...
Output/ReleaseApp/Sources/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal.o
Output/ReleaseApp/Sources/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_adc.o
Output/ReleaseApp/Sources/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_adc_ex.o
 ...
```
Если сократить названия каталогов и вынести их на как можно более высокий уровень в проекте, сократятся пути и, как следствие, длина команды.

### Применение архивов

Группу объектных файлов можно объеденить в архив `*.a` и уже его передавать линкеру. Это позволит уменьшить длину командной строки тем значительнее, чем больше файлов собрано в архиве.

Однако, следует следить за тем, чтобы длина команды сборки архива также не была превышена.

Также следует учесть, что `__attribute__((weak))` ([Weak symbol - Wikipedia](https://en.wikipedia.org/wiki/Weak_symbol)) работает с архивами не так, как ожидается. Данный атрибут широко используется в  исходниках от ST для обработчиков прерываний и функций обратного вызова.

Вкратце - weak символ не переопределяется символом, находящимся в библиотеке.
Подробнее [STM32 weak exception handler override in ASM not working (ARM-EABI-GCC)](https://community.st.com/s/question/0D50X0000ALx8Fh/stm32-weak-exception-handler-override-in-asm-not-working-armeabigcc) :

>  Linkers (including the GNU linker) treat libraries in a different way than they treat objects, even if the libraries appear to be only a collection of objects. This has both rational and historical reasons and I am yet to see a concise document outlining all the linker idiosyncrasies in historical context. One of the underlying (unwritten) idea is, that users are not supposed to create libraries, they are supposed to stick with objects, libraries are to be a domain of system creators. Nevertheless, users are often caught with unpleasant surprise when they move their objects into libraries to find that the result is quite different from what it used to be with standalone objects.
> 
> Here, in particular, the fact, that linkers don't search for symbols in libraries if they were already fulfilled, weak or not, is probably the surprising factor. The probable reason for this is the (unwritten, again, and with historic roots too) rule that you should be always able to override library functions with your own version (because of the potentially buggy library one); and the weak/strong mechanism is supposed to help resolving a similar problem entirely in the user (objects) domain.
>
> Other such factor is that linkers don't iterate when searching for a symbol in libraries (unless forced to do so by some set of command-line switches), ie. if there's a new symbol found in the library (or, in a more rare case in an object linked *after* having linking libraries) it can't be fulfilled by a definition from a library linked earlier (but it can be fulfilled by a user definition, even if objects were liked earlier). The visible effect is, that library ordering in command line (and/or specs) does matter, and sometimes manual reordering or overriding specs-given ordering results in surprising faults.

### Список файлов в файле

У линкера **ld** и утилиты **ar** имеется опция **@file**:
> Read command-line options from file. The options read are inserted in place of the original **@file** option. If file does not exist, or cannot be read, then the option will be treated literally, and not removed.
> 
> Options in file are separated by whitespace. A whitespace character may be included in an option by surrounding the entire option in either single or double quotes. Any character (including a backslash) may be included by prefixing the character to be included with a backslash. The file may itself contain additional **@file** options; any such options will be processed recursively.

Можно вынести длинный список объектных файлов (да и вообще все опции) в отдельный файл, который затем и передать аргументом.

Для архива:
```make
${OUTPUT_DIR}/libapplication.a: ${APP_C_OBJECTS} ${APP_CPP_OBJECTS} ${APP_ASM_OBJECTS}
	@echo > ${OUTPUT_DIR}/application.files <<EOF ${^}
	@${AR} -crs ${@} @${OUTPUT_DIR}/application.files
```

Или для линкера:
```make
${TARGET_ELF}: ${C_OBJECTS} ${CPP_OBJECTS} ${ASM_OBJECTS}
	@echo > ${OUTPUT_DIR}/object.files <<EOF $(sort $(filter %.o %.a, ${^}))
	${LD} ${LINKER_PARAMS} -o ${@} @${OUTPUT_DIR}/object.files
```
