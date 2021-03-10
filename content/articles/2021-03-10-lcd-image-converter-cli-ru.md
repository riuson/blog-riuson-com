Title: LCD Image Converter - командная строка
Date: 2021-03-10 21:58:00 +0500
Category: LCD Image Converter
Summary: Как использовать командную строку для автоматизации.

У программы имеется интерфейс командной строки, о котором, я полагаю, почти никто не знает. Описание [приведено на сайте](https://lcd-image-converter.riuson.com/en/docs/others/command-line/).

Создавался он для решения таких задач:

- Есть прошивка для МК и дисплея, в которой имеется множество изображений (значки в меню).
После изменения изображения надо его сохранить, открыть в программе, конвертировать, сохранить.
Что-то из этой последовательности можно забыть. Особенно, если изменяется множество изображений за короткое время.
Соответствие между графическим файлом и полученным исходником мимолётом не определяется.
- Сконвертировал файлы и готово. Через 10 лет открыл проект, надо поправить значки или добавить символы в шрифт. Открываешь сохранённый файл, а вот настроек преобразования, что ранее использовались, уже нет. Т.к. хранятся они по умолчанию в реестре (Windows) или каталогах пользователя (Linux).

Посему, было решено хранить под контролем версий изображения в их оригинальном формате, а также необходимые параметры преобразования.

В проекте создан каталог *resources*, содержащий файлы шрифтов *font\*.xml*, файлы изображений в *\*.png*, шаблоны *\*.txt*, файлы предустановок преобразования *presets.xml* :

```text
resources\.gitignore
resources\update-resources.py

resources\fonts\fontLarge.xml
resources\fonts\fontMiddle.xml
resources\fonts\fontSmall.xml
resources\fonts\presets.xml
resources\fonts\template.txt

resources\images\default.png
resources\images\presets.xml
resources\images\template.txt
```

Содержимое *.gitignore*, т.к. эти файлы будут создаваться скриптом:

```text
fonts/*.cpp
fonts/*.h*
images/*.cpp
images/*.h*
```

В *tasks.json* у VS Code добавляется задача:

```json
{
  "label": "Update resources",
  "type": "process",
  "command": "python.exe",
  "args": [
    "${workspaceFolder}\\sources\\resources\\update-resources.py",
  ],
  "options": {
    "cwd": "${workspaceFolder}",
    "env": {
      "PATH": "${workspaceFolder}\\..\\tools\\python-3.9.1;C:\\Windows\\System32;",
      "PYTHONPATH": "${workspaceFolder}\\..\\tools\\python-3.9.1;${workspaceFolder}\\..\\tools\\python-3.9.1\\Lib;\\${workspaceFolder}\\..\\tools\\python-3.9.1\\Lib\\site-packages;",
    },
  },
  "group": "build"
}
```

Далее она вызывается

```text
Update resources...
  Fonts...   
    fontLarge
    fontMiddle
    fontSmall
  Images...
    image_default
...Completed.
```

и получаем результаты преобразования

```text
resources\.gitignore
resources\update-resources.py
 
resources\fonts\fontLarge.cpp
resources\fonts\fontLarge.xml
resources\fonts\fontMiddle.cpp
resources\fonts\fontMiddle.xml
resources\fonts\fonts.hpp
resources\fonts\fontSmall.cpp
resources\fonts\fontSmall.xml
resources\fonts\presets.xml
resources\fonts\template.txt

resources\images\default.cpp
resources\images\default.png
resources\images\images.hpp
resources\images\presets.xml
resources\images\template.txt
```

В файлах *\*.hpp* собираются объявления шрифтов и изображений соответственно, для удобного обращения к ним.

Сохранение самого изображения или шрифта в заголовочный файл, при условии его дальнейшего включения/использования в нескольких местах, - идея плохая. В этом случае, для каждого места включения может быть создана своя копия данных, напрасно занимающая место во Flash. Поэтому следует разделять объявления и определения.
{: .bg-warning}

Например, *images.hpp*:

```cpp
#ifndef APP_RESOURCES_IMAGES_H
#define APP_RESOURCES_IMAGES_H

// Этот файл сгенерирован автоматически.

#include "defs/graphics/image.hpp"

namespace App::Resources::Images
{

extern const Defs::Graphics::Image image_default;

} // namespace App::Resources::Images

#endif // APP_RESOURCES_IMAGES_H
```

Использование:

```cpp
#include "resources/images/images.hpp"
...
Drivers::Display::drawImage(0, 0, App::Resources::Images::image_default, Defs::Graphics::Color::Foreground);
```

Код, выполняющий все операции, приведён ниже.

```python
#!/usr/bin/env python3
import os
import sys
import glob
import pathlib
import subprocess

# Каталог ресурсов.
resourcesDirectory = os.path.dirname(os.path.realpath(__file__))
# Программа преобразования изображений/шрифтов в исходный код.
licPath = os.path.normpath(os.path.join(
    resourcesDirectory, '../../../tools/lic/lcd-image-converter.exe'))


def makeFonts():
    print('  Fonts...')

    # Список файлов шрифтов.
    sourceDirectory = os.path.join(resourcesDirectory, 'fonts')
    sourceFiles = glob.glob(os.path.join(
        sourceDirectory, 'font*.xml'), recursive=False)
    # Путь к пресетам.
    presetsPath = os.path.join(sourceDirectory, 'presets.xml')
    # Путь к шаблону.
    templatePath = os.path.join(sourceDirectory, 'template.txt')
    # Путь к заголовочному файлу.
    headerPath = os.path.join(sourceDirectory, 'fonts.hpp')

    headerContent = '\
#ifndef APP_RESOURCES_FONTS_H\n\
#define APP_RESOURCES_FONTS_H\n\
\n\
// Этот файл сгенерирован автоматически.\n\
\n\
#include "defs/graphics/font.hpp"\n\
\n\
namespace App::Resources::Fonts\n\
{\n\n\
'

    # Обработка списка файлов.
    for sourceFile in sourceFiles:
        # Выходной путь файла шрифта.
        outputFile = pathlib.Path(sourceFile).with_suffix('.cpp')
        # Имя документа.
        documentName = os.path.splitext(os.path.basename(sourceFile))[0]
        # Добавление в заголовочный файл.
        headerContent += f'extern const Defs::Graphics::Font {documentName};\n'
        # Преобразование.
        args = [
            licPath,
            '--mode=convert-font',
            '--preset-name=MonochromeCode',
            f"--input={sourceFile}",
            f"--output={outputFile}",
            f"--template={templatePath}",
            f"--config-presets={presetsPath}"
            # f"--doc-name={documentName}",
        ]
        print('    ' + documentName)
        subprocess.run(args)
    headerContent += '\n\
} // namespace App::Resources::Fonts\n\
\n\
#endif // APP_RESOURCES_FONTS_H\n\
'
    headerFile = open(headerPath, 'w', encoding='utf-8')
    headerFile.write(headerContent)
    headerFile.close()


def makeImages():
    print('  Images...')

    # Список файлов шрифтов.
    sourceDirectory = os.path.join(resourcesDirectory, 'images')
    sourceFiles = glob.glob(os.path.join(
        sourceDirectory, '*.png'), recursive=False)
    # Путь к пресетам.
    presetsPath = os.path.join(sourceDirectory, 'presets.xml')
    # Путь к шаблону.
    templatePath = os.path.join(sourceDirectory, 'template.txt')
    # Путь к заголовочному файлу.
    headerPath = os.path.join(sourceDirectory, 'images.hpp')

    headerContent = '\
#ifndef APP_RESOURCES_IMAGES_H\n\
#define APP_RESOURCES_IMAGES_H\n\
\n\
// Этот файл сгенерирован автоматически.\n\
\n\
#include "defs/graphics/image.hpp"\n\
\n\
namespace App::Resources::Images\n\
{\n\n\
'

    # Обработка списка файлов.
    for sourceFile in sourceFiles:
        # Выходной путь файла шрифта.
        outputFile = pathlib.Path(sourceFile).with_suffix('.cpp')
        # Имя документа.
        documentName = os.path.splitext(os.path.basename(sourceFile))[0]

        if not (documentName.startswith('image') or documentName.startswith('icon')):
            documentName = 'image_' + documentName

        # Добавление в заголовочный файл.
        headerContent += f'extern const Defs::Graphics::Image {documentName};\n'
        # Преобразование.
        args = [
            licPath,
            '--mode=convert-image',
            '--preset-name=MonochromeCode',
            f"--input={sourceFile}",
            f"--output={outputFile}",
            f"--template={templatePath}",
            f"--config-presets={presetsPath}",
            f"--doc-name={documentName}"
        ]
        print('    ' + documentName)
        subprocess.run(args)
    headerContent += '\n\
} // namespace App::Resources::Images\n\
\n\
#endif // APP_RESOURCES_IMAGES_H\n\
'
    headerFile = open(headerPath, 'w', encoding='utf-8')
    headerFile.write(headerContent)
    headerFile.close()


print('Update resources...')
makeFonts()
makeImages()
print('...Completed.')
```

Для редактирования предустановок можно использовать те же задачи VS Code:

```json
{
  "label": "Run Image's Editor",
  "type": "shell",
  "command": "${workspaceRoot}/../tools/lic/lcd-image-converter.exe --config-presets ${workspaceRoot}/sources/resources/images/presets.xml",
  "options": {
    "cwd": "${workspaceRoot}",
  },
  "group": "build"
}
```

```json
{
  "label": "Run Font's Editor",
  "type": "shell",
  "command": "${workspaceRoot}/../tools/lic/lcd-image-converter.exe --config-presets ${workspaceRoot}/sources/resources/fonts/presets.xml",
  "options": {
    "cwd": "${workspaceRoot}",
  },
  "group": "build"
}
```
