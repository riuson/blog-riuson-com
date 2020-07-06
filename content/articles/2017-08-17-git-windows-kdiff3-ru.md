Title: Git for Windows + KDiff3
Tags: Git
Summary: Настройка KDiff3 в качестве mergetool и difftool в Git for Windows.

Настройка KDiff3 в качестве mergetool и difftool в Git for Windows.

Устанавливаем [KDiff3](https://sourceforge.net/projects/kdiff3).

В Git Bash прописываем:
```
git config --global --add merge.tool kdiff3
git config --global --add mergetool.kdiff3.path "C:/Program Files/KDiff3/kdiff3.exe"
git config --global --add mergetool.kdiff3.trustExitCode false

git config --global --add diff.guitool kdiff3
git config --global --add difftool.kdiff3.path "C:/Program Files/KDiff3/kdiff3.exe"
git config --global --add difftool.kdiff3.trustExitCode false
```
