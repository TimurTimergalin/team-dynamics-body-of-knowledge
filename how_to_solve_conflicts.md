# Как решать конфликты в git

В случае, если при мердже pull request-а возникают конфликты, действовать следует следующим образом
```shell
git checkout master
git pull
git checkout -
git rebase master
# ...
# Решаем конфликты, а потом
git push -f # В свою ветку делать force merge нестрашно
```
