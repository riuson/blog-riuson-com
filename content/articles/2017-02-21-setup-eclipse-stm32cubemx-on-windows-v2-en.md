Title: Installation and setup Eclipse, STM32CubeMX under Windows (v2).
Tags: STM32

Manual was updated due to changes from previous version of CubeMX.

Installation and setup development environment for STM32, with Eclipse, STM32CubeMX, GNU ARM Embedded, GNU ARM Eclipse Plugins.<br>
MCU: STM32F103RET6.

[<i class="fab fa-youtube"></i> Video: Setup Eclipse and STM32CubeMX on Windows](https://youtu.be/i5VUF1wYTQU)
<!-- more -->

Manual was updated due to changes from previous version of CubeMX.{ .bg-info .text-white }

If it is not working, please write in comments.{ .bg-warning .text-dark }

All process has been recorded on video.
Operating system: Windows 10 Home.


# Download

List of used software.:

  * [Eclipse IDE for C/C++ Developers](http://www.eclipse.org/downloads/)
  * [Java Virtual Machine](https://www.java.com/en/download/)
  * [GCC ARM Embedded](https://launchpad.net/gcc-arm-embedded) Windows Installer
  * [How to install the Windows Build Tools?](http://gnuarmeclipse.github.io/windows-build-tools/install/)
  * [The GNU ARM Eclipse plug-ins](http://gnuarmeclipse.github.io/)
    * [How to install the GNU ARM Eclipse plug-ins?](http://gnuarmeclipse.github.io/plugins/install/) (download by Eclipse)
  * [STM32CubeMX STM32Cube initialization code generator](http://www.st.com/en/development-tools/stm32cubemx.html?icmp=stm32cubemx_pron_prcube_feb2014&sc=stm32cube-pr)
    * [STM32CubeMX Eclipse plug in for STM32 configuration and initialization C code generation](http://www.st.com/content/st_com/en/products/development-tools/software-development-tools/stm32-software-development-tools/m32-configurators-and-code-generators/stsw-stm32095.html)
    * [STM32CubeF1](http://www.st.com/content/st_com/en/products/embedded-software/mcus-embedded-software/stm32-embedded-software/stm32cube-embedded-software/stm32cubef1.html)
  * [Jlink - Software and documentation pack for Windows](https://www.segger.com/jlink-software.html)

# Install

## Eclipse IDE for C/C++ Developers
Download Eclipse installer and install _Eclipse IDE for C/C++ Developers_.

## Java Virtual Machine
If Eclipse installer can't find JRE, next dialog can be shown:
> The required 64-bit Java 1.7.0 virtual machine could not be found.<br>
Do you want to browse your system for it?
{: .blockquote }

You can browse for it or open web-site by clicking _No_.

## Windows Build Tools
[Installation manual](http://gnuarmeclipse.github.io/windows-build-tools/install/). All as usual.

## GCC ARM Embedded
Disable checkboxes _Launch gccvar.bat_ and _Add path to enviroment variable_ after installation. So you can install many compilers.

## GNU ARM Eclipse plug-ins
[Installation manual](http://gnuarmeclipse.github.io/plugins/install/).
In Eclipse menu choose _Help_ -> _Install New Software..._. Add website

* name: GNU ARM Eclipse Plug-ins
* URL: http://gnuarmeclipse.sourceforge.net/updates

Select and install all components.

If you see an error about **Handshake_failure**, please read the next topic: [GNU ARM Eclipse plug-ins: Received fatal alert: handshake_failure](http://gnuarmeclipse.github.io/blog/2017/01/29/plugins-install-issue).

## STM32CubeMX Eclipse plug in
Start Eclipse. Choose menu _Help_ -> _Install New Software..._ and install plugin from archive _STSW-STM32095.zip_.
Restart Eclipse.

## STM32CubeF1
Start Eclipse. Open STM32CubeMX from menu _Window_ -> _Show View_ -> _Other..._ -> _STM32CubeMX_. 
Choose _Help_ -> _Install New Libraries_ from STM32CubeMX menu to open Libraries Manager.

Here you can install package for selected MCU series.
* Network: select checkbox and click _Install Now_.
* Local: click _From Local..._ and open file _STM32CubeF1.zip_.


## J-Link
All as usual.

# Setup

## Create project in Eclipse
Choose menu _C/C++_ -> _C Project_.
Write a project's name and select type _Hello World ARM C++ Project_, Toolchain _Cross ARM GCC_.
Replace source's directory from _src_ to _Src_. At _Linker semi-hosting options_ write only next string 
```
--specs=nosys.specs
```

Build project.

## Create project in STM32CubeMX
### Code generation
Start STM32CubeMX and create new project.<br>
Select used MCU. For example STM32F103RET6.
Change project settings.<br>
Start code generation. Set project name equals to Eclipse project. Set _Project Location_ directory in workspace, where existing Eclipse project was placed. Set Toolchain/IDE to SW4STM32. Uncheck _ Generate Under Root_.<br>
Start by clicking _Ok_.

Source codes will be saved over early created project.<br>
Close STM32CubeMX.

Refresh project tree in Eclipse. You can see newly added directories, _Driver_ and _Inc_. _Src_ directory combined with existing.<br>
Newly added directories disabled by default, so enable it thru properties dialog.<br>

Create file _startup.asm_ in _Src_ directory. Add path to generated assembler startup file:
```
.include "../Drivers/CMSIS/Device/ST/STM32F1xx/Source/Templates/gcc/startup_stm32f103xe.s"
```


### Migrate settings
How to migrate settings from CubeMX project to Eclipse?

Open Eclipse project. Open project's _Properties_ - _C/C++ General_ - _Path and Symbols_. Add some string markers to Includes и Symbols.

Then close project. Open XML file of both projects, _.cproject_ and _./SW4STM32/< project name >/.cproject_.<br>
Format XML with any tool for easy reading. For example, xmlbeautifier.

#### Symbols
Locate nodes with symbols in XML file (SW4STM32), like next:
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

Locate nodes with markers in other XML file (Eclipse) and replace it.
List of symbols looks like next:
```
__weak="__attribute__((weak))"
__packed="__attribute__((__packed__))"
USE_HAL_DRIVER
STM32F103RE
ARM_MATH_CM3
```
Last line missing in XML file, but it is required for build.<br>
Quote at \__weak and \__packed are required. In XML file quotes need to be escaped as ` " ` :
```
__weak="__attribute__((weak))"
```

#### Includes
Locate nodes with Include paths in XML file (SW4STM32) like this:
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
Change prefix from relative path
```
../../../Inc
../../../Drivers/STM32F1xx_HAL_Driver/Inc
```
to variable
```
${ProjDirPath}/Inc
${ProjDirPath}/Drivers/STM32F1xx_HAL_Driver/Inc
```

Copy nodes to other XML file (Eclipse).

#### ARM family
Open project's Properties in Eclipse, navigate to _C/C++ Build_ -> _Settings_ -> _Tool Settings_ -> _Target Processor_ -> _ARM family_, select _cortex-m3_.

#### Charset
Also you can change charset of project's resources to UTF-8.

#### Linker script
Copy linker script from _./SW4STM32/< project name >/STM32F103RETx\_FLASH.ld_ to _Scripts/STM32F103RETx\_FLASH.ld_.<br>
Open project's Properties, navigate to _C/C++ Build_ -> _Settings_ -> _Tool Settings_ -> _Cross ARM C Linker_ -> _General_. Add file to _Scripts files (-T)_ list.

# Build
Start build project.<br>
You can set _C/C++ Build_ -> _Behavior_ -> _Enable parallel build_ to speed up build.

# Debug
## Check connection with debugger and MCU thru J-Flash.
Start J-Flash. Create new project. Select debugger, _Target Interface_, _CPU_ -> _Device_. Click menu _Target_ -> _Connect_. You should see message in log: 
```
Connected successfully
```
If you don't see it, something going wrong.<br>
Then select _Target_ -> _Manual programming -> _Erase chip_.
You should see message in log: 
```
Erase operaion completed successfully.
```

## Setup debugger in Eclipse
Open menu _Debug_ -> _Debug Configurations..._.<br>
Create new connection under _GDB Segger J-Link Debugging_.<br>
Set _Device name_ on _Debugger_ page, for example _STM32F103RE_.<br> Select _Connection_ and _Interface_, if needed.<br>
To add debug configuration to favorites menu, set checlbox _Debug_ in list _Display in favorites menu_ on _Common_ page.<br>
Start debug from favorites in _Debug_ menu.

Formware shoud be programmed to flash. Debug starts with breakpoint on method _main_.

# Updating project
This project's structure allows update project with STM32CubeMX without problems.<br>
Just start STM32CubeMX.<br>
Load STM32CubeMX project (generated *.ioc file in root directory of project).<br>
Change settings.<br>
Start code generation.<br>
Files will be regenerated over existing, but user's code keeps in special sections.


** The End. **
