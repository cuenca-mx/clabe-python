## CLABE

[![Build Status](https://travis-ci.com/cuenca-mx/clabe.svg?branch=master)](https://travis-ci.com/cuenca-mx/clabe)
[![PyPI](https://img.shields.io/pypi/v/clabe.svg)](https://pypi.org/project/clabe/)

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

```python
import clabe
clabe.compute_control_digit('03218000011835971')
```

Para validar si un número CLABE es válido

```python
import clabe
clabe.validate_clabe('032180000118359719')
```

Para obtener el banco a partir de 3 dígitos

```python
import clabe
clabe.get_bank_name('002')
```

Para generar nuevo válido CLABES

```python
import clabe
clabe.generate_new_clabes(10, '03218000011')
```
