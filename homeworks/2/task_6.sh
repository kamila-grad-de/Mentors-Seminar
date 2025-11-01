#!/bin/bash

# Скрипт читает содержимое файла input.txt, считает количество строк
# и записывает результат в output.txt. Ошибки команды ls для несуществующего
# файла перенаправляются в error.log.

# Основные действия:
wc -l < input.txt > output.txt
ls nonexistent_file.txt 2> error.log

# Наблюдение:
echo "Содержимое input.txt:"
cat input.txt

echo
echo "Содержимое output.txt:"
cat output.txt

echo
echo "Содержимое error.log:"
cat error.log
