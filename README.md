# acr-logs-qt

Arquivo config.json

```json
{
  "regexLog": "${CLASS_NAME}::${METHOD_NAME}[ \"].*",
  "regexFile": ".*\\.h|.*\\.cpp",
  "logTypes": [
    "qDebug",
    "qInfo",
    "qWarning",
    "qCritical"
  ]
}
```

Dependencias

- ctags

```shell
sudo apt-get install universal-ctags
```
