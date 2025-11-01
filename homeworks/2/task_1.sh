#!/bin/bash

file=$1

echo "1. Файлы и их типы:"
for f in *; do
    if [ -L "$f" ]; then
        echo "$f это ссылка"
    elif [ -d "$f" ]; then
        echo "$f это каталог"
    elif [ -f "$f" ]; then
        echo "$f это файл"
    else
        echo "$f это неизвестно"
    fi
done

echo
echo "2. Проверка файла: $file"
[ -e "$file" ] && echo "Файл найден" || echo "Файл не найден"

echo
echo "3. Права доступа:"
for f in *; do
    [ -f "$f" ] && echo "$f это $(stat -c %A "$f")"
done
