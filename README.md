# El interpreter

## Ejecutar el backend

1. Instalar fastapi

```
pip install fastapi
```

2. Instalar univorn

```
pip install "uvicorn[standard]"
```

3. Ejecutar el main

```
uvicorn main:app --reload
```
Por defecto la url será http://127.0.0.1:8000/

## Métodos de la API

**Nota**: El languaje solo puede procesar una línea a la vez.

### Ejecutar una linea en el interpreter

`POST /`

En el body de la solicitud debe haber un json con `"line": "<Mi línea de código>"`. Ejemplos:
```json
{
    "line": "1 + 2 * 3"
}
```
El resultado tendrá esta forma:
```json
{
    "output": 7,
    "tokens": [
        {
            "type": "NUMBER",
            "value": 1
        },
        {
            "type": "PLUS",
            "value": "+"
        },
        {
            "type": "NUMBER",
            "value": 2
        },
        {
            "type": "REPETITION",
            "value": "*"
        },
        {
            "type": "NUMBER",
            "value": 3
        }
    ],
    "tree": [
        "+",
        1,
        [
            "*",
            2,
            3
        ]
    ]
}
```

### Obtener la tabla de sínbolos

`GET /variables`


```json
{
    "myvar": "Hola",
    "a": 2
}
```

## Lo que puede hacer el lenguaje de programación

1. Puede hacer operaciones de suma, resta y multiplicación de cualquier tamaño:

```
1 + 2 - 5 * 2
```
```
>>> -7
```

2. Puede manejar cadenas de caracteres:

```
"Hola " . "Mun" . "do"
```
```
>>> Hola Mundo
```

3. Puede repetir cadenas de caracteres:

```
"Hola" * 3
```
```
>>> HolaHolaHola
```
Da el mismo resultado si se ejecuta `3 * "Hola"`

4. Uso de variables

```
a = 3
mystring = "Hola mundo"
```

5. Hacer referencia a las variables

```
new_variable = mystring * a
```

6. Imprimir

```
print new_variable
```
```
>>> Hola mundoHola mundoHola mundo
```

Además, puede manejar las operaciones de suma y concatenación

```
print 1 + 2 + a
```
```
>>> 6
```

```
print mystring . " Hello world"
```
```
>>> Hola mundo Hello world
```
