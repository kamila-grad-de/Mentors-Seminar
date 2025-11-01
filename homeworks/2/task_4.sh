#!/bin/bash

greet() {
    echo "Hello, $1"
}

add() {
    echo $(($1 + $2))
}

greet "John Doe"
add 5 2
