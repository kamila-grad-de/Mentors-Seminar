#!/bin/bash

read -p "Введите число: " n

if (( n > 0 )); then
    echo "$n это положительное число"
    echo "Считаем от 1 до $n:"
    count=1
    while (( count <= n )); do
        echo "$count"
        ((count++))
    done
elif (( n < 0 )); then
    echo "$n это отрицательное число"
else
    echo "Это ноль"
fi
