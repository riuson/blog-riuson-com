Title: Git - корректировка дат в коммитах
Tags: Git
Summary: Как сменить дату коммита в Git

### Замена дат в предыдущих коммитах.

[Changing the timestamp of a previous Git commit](http://eddmann.com/posts/changing-the-timestamp-of-a-previous-git-commit/)


```bash
$ git filter-branch --env-filter \
"if test \$GIT_COMMIT = 'e6dbcffca68e4b51887ef660e2389052193ba4f4'
then
    export GIT_AUTHOR_DATE='Sat, 14 Dec 2013 12:40:00 +0000'
    export GIT_COMMITTER_DATE='Sat, 14 Dec 2013 12:40:00 +0000'
fi" && rm -fr "$(git rev-parse --git-dir)/refs/original/"
```

### Замена даты в новом коммите.
```bash
GIT_COMMITTER_DATE="2000-01-01 12:00:00 +0300" git commit --date "2000-01-01 12:00:00 +0300"
```
