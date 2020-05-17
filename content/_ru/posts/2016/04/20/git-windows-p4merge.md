---
title:  "Git for Windows and P4merge"
date:   2016-04-20 00:00:00 +0500
categories:
  - "Git"
---
Настройка использования p4merge в Git for Windows в качестве mergetool.
Применять такую утилиту приходится крайне редко, т.к. Git прекрасно проводит слияние веток, если они заранее были правильно организованы.
<!-- more -->

Идёт на сайт [Perforce](https://www.perforce.com/downloads/helix#product-10).
Качаем **Helix P4Merge: Visual Merge Tool** и устанавливаем.

Выполняем команды
```bash
$ git config --global merge.tool p4merge
$ git config --global mergetool.p4merge.path "C:/Program Files/Perforce/p4merge.exe"
```

После этого в файле конфигурации Git'а добавятся строки:
```
[mergetool "p4merge"]
	path = "C:/Program Files/Perforce/p4merge.exe"
```

После выполнения merge может возникнуть конфликт
```bash
user@desktop MINGW32 /c/projects/project (develop)
$ git merge --no-ff --no-commit feature-branch

Auto-merging file1.txt
Removing file2.txt
...
Auto-merging .gitignore
CONFLICT (content): Merge conflict in .gitignore
Automatic merge failed; fix conflicts and then commit the result.
```

Запускаем mergetool
```bash
user@desktop MINGW32 /c/projects/project (develop|MERGING)
$ git mergetool
```

Git показывает список файлов с конфликтами и начинает по очереди применять к ним настроенный merge tool.
  * <span style="color:blue">REMOTE ▼</span> - удалённая версия (та, что вливается сюда извне);
  * <span style="color:green">LOCAL ●</span> - локальная, рабочая копия;
  * <span style="color:orange">BASE ■</span> - найденный общий предок этого файла для локальной и удалённой веток;
  * Внизу отображается результат слияния. Цветными галочками справа можно выбирать нужную версию принимаемых изменений. Также, можно исправить результат вручную.

![MergeTool]({{ '/assets/images/posts/2016/04/20/git-windows-p4merge-1.png' | relative_url }}){:class="img-fluid"}

После исправления конфликтов следует сохранить всё и закрыть.
