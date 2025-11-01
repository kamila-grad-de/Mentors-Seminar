#!/bin/bash

dir="$1"

echo "Текущее значение PATH:"
echo "$PATH"

export PATH="$PATH:$dir"

echo
echo "Новое значение PATH:"
echo "$PATH"

echo
echo "Чтобы изменение PATH сохранялось после перезапуска терминала:"
echo "Добавьте эту строку в ~/.bashrc:"
echo "export PATH=\"\$PATH:$dir\""
echo
echo "После этого выполните: source ~/.bashrc"
