Title: Git for Windows - указание домашнего каталога
Tags: Git
Summary: Что делать, если требуется изменить расположение домашнего каталога *~/home*, например для хранения ключей SSH в определённом месте.

Если требуется изменить расположение домашнего каталога *~/home*, например для хранения ключей SSH в определённом месте.

* Скачать [Git for Windows](https://git-scm.com/downloads).
* Установить.
* Перейти в каталог установки. Например '*d:\Software\Installed\Git\*'
* Открыть файл '*./etc/profile*' .
* Добавить первой строкой:
```bash
# HOME="path-to-home-dir"
HOME="d:/Software/Installed/Git/home/"
```
