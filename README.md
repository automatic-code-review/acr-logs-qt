# acr-logs-qt

Verifica o codigo c++, se os logs estao de acordo com o padrao esperado, por exemplo podemos definir que todos os logs tevem conter o nome da classe e o nome do method no inicio do log, para facilitar a localizacao do mesmo no codigo fonte<br>
No atributo regexLOg e bindado os valores ${CLASS_NAME} que se refere ao nome da classe, e o ${METHOD_NAME} que se refere ao nome do method<br>

1. Atributo regexLog se refere ao regex de padrao para o log em questao
2. Atributo regexFile se refere ao regex de arquivo que sera verificado os logs
3. Atributo logTypes se refere a lista de tipos de logs

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
