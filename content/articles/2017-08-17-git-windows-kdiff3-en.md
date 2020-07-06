Title: Git for Windows + KDiff3
Tags: Git
Summary: How to setup KDiff3 as mergetool and difftool in Git for Windows.

Setup KDiff3 as mergetool and difftool in Git for Windows.

Download and install [KDiff3](https://sourceforge.net/projects/kdiff3).

Execute following commands at Git Bash:
```bash
git config --global --add merge.tool kdiff3
git config --global --add mergetool.kdiff3.path "C:/Program Files/KDiff3/kdiff3.exe"
git config --global --add mergetool.kdiff3.trustExitCode false

git config --global --add diff.guitool kdiff3
git config --global --add difftool.kdiff3.path "C:/Program Files/KDiff3/kdiff3.exe"
git config --global --add difftool.kdiff3.trustExitCode false
```
