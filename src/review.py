import hashlib
import json
import os
import re
import subprocess


def review(config):
    log_types = config['logTypes']
    regex_log = config['regexLog']
    regex_file = config['regexFile']
    path_source = config['path_source']

    comments = __review_by_dir(
        path_code=path_source,
        path_code_origin=path_source,
        regex_file=regex_file,
        regex_log=regex_log,
        log_types=log_types
    )

    return comments


def __review_by_dir(path_code, path_code_origin, regex_file, regex_log, log_types):
    comments = []

    for content in os.listdir(path_code):
        path_content = os.path.join(path_code, content)

        if os.path.isfile(path_content):
            if re.search(regex_file, path_content):
                comments.extend(__review_by_file(path_code_origin, path_content, regex_log, log_types))

        elif os.path.isdir(path_content):
            comments.extend(__review_by_dir(path_content, path_code_origin, regex_file, regex_log, log_types))

    return comments


def __review_by_file(path_code_origin, path_file, regex_log, log_types):
    data = subprocess.run(
        'ctags --output-format=json --format=2 --fields=+line ' + path_file,
        shell=True,
        capture_output=True,
        text=True,
    ).stdout

    objs = []

    for function in data.split('\n'):
        if function == '':
            continue

        function = json.loads(function)

        if function['kind'] != 'function':
            continue

        if 'scopeKind' not in function or function['scopeKind'] != 'class':
            continue

        objs.append({
            'class': function['scope'],
            'method': function['name'],
            'startInLine': function['line'],
            'endInLine': function['end'],
        })

    objs = sorted(objs, key=lambda x: x['startInLine'])

    with open(path_file, 'r') as f:
        linhas = f.readlines()

    comments = []

    for obj in objs:
        start_line = obj['startInLine']
        end_line = obj['endInLine']
        check = str(regex_log).replace("${CLASS_NAME}", obj['class']).replace("${METHOD_NAME}", obj['method'])

        for i in range(start_line - 1, end_line):
            text = linhas[i]
            text_original = str(text).strip()

            for log_type in log_types:
                comments.extend(__review_by_line(
                    text=text,
                    log_type=log_type,
                    check=check,
                    path_file=path_file,
                    path_code_origin=path_code_origin,
                    text_original=text_original,
                    line=i + 1,
                ))

    return comments


def __review_by_line(text, log_type, check, path_file, path_code_origin, text_original, line):
    comments = []

    if log_type in text:
        text = text[text.index(log_type) + len(log_type + "() << \""):]

        if not re.search(check, text):
            path_internal = str(path_file).replace(path_code_origin + "/", "")
            comment = f"""Linha de código fora do padrão no arquivo: {path_internal}
Na linha: {line}
Código fora do padrão:
```c++
{text_original}
```"""
            comments.append(
                __create_comment(
                    comment_id=__generate_md5(comment),
                    comment=comment,
                    path=path_internal,
                    line=line
                )
            )

    return comments


def __create_comment(comment_id, comment, path, line):
    return {
        "id": comment_id,
        "comment": comment,
        "position": {
            "language": 'c++',
            "path": path,
            "startInLine": line,
            "endInLine": line
        }
    }


def __generate_md5(string):
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    return md5_hash.hexdigest()
