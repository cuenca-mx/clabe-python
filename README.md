## CLABE 

[![Build Status](https://travis-ci.com/cuenca-mx/clabe.svg?branch=master)](https://travis-ci.com/cuenca-mx/clabe)

Librería para validar y calcular un número CLABE basado en
https://es.wikipedia.org/wiki/CLABE

**Requerimientos**

Python v3 o superior.

**Instalación**

Se puede instalar desde Pypi usando

```
pip install clabe
```

**Test**

Para ejecutar los test utlizando el archivo Makefile

```
$ make test
```

**Uso básico**

Obtener el dígito de control de un número CLABE

``` Python
import clabe

clabe.compute_control_digit(clabe_number)
```

Para validar si un número CLABE es válido

``` Python
import clabe

clabe.validate_clabe(clabe_number)
```

Para obtener el banco a partir de 3 dígitos

``` Python
import clabe

clabe.get_bank_name('002')
```