Title: Git for Windows - custom home directory
Tags: Git
Summary: How to change home directory *~/home*, for example to store SSH keys in other location.

If it is required to change home directory *~/home*, for example to store SSH keys in other location.

* Download [Git for Windows](https://git-scm.com/downloads).
* Install it.
* Navigate to installation directory. For example '*d:\Software\Installed\Git\*'
* Open file '*./etc/profile*' .
* Add first line like this:
```bash
# HOME="path-to-home-dir"
HOME="d:/Software/Installed/Git/home/"
```
