# CLABE

[![test](https://github.com/cuenca-mx/clabe-python/workflows/test/badge.svg)](https://github.com/cuenca-mx/clabe-python/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/cuenca-mx/clabe-python/branch/main/graph/badge.svg)](https://codecov.io/gh/cuenca-mx/clabe-python)
[![PyPI](https://img.shields.io/pypi/v/clabe.svg)](https://pypi.org/project/clabe/)
[![Downloads](https://pepy.tech/badge/clabe)](https://pepy.tech/project/clabe)

Librería para validar y calcular un número CLABE basado en
https://es.wikipedia.org/wiki/CLABE

## Requerimientos

Python 3.6 o superior.

## Instalación

Se puede instalar desde Pypi usando

```
pip install clabe
```

## Pruebas

Para ejecutar las pruebas

```
$ make test
```

## Uso básico

Obtener el dígito de control de un número CLABE

```python
import clabe
clabe.compute_control_digit('00200000000000000')
```

Para validar si un número CLABE es válido

```python
import clabe
clabe.validate_clabe('002000000000000008')
```

Para obtener el banco a partir de 3 dígitos

```python
import clabe
clabe.get_bank_name('002')
```

Para generar nuevo válido CLABES

```python
import clabe
clabe.generate_new_clabes(10, '002123456')
```

## Para agregar un nuevo banco

A partir de la versión 2.0.0, el paquete se actualizará a **Pydantic v2**, lo que significa que las versiones anteriores ya no recibirán soporte.

Sin embargo, hemos añadido una función para agregar bancos adicionales a la lista, en caso de que sea necesario. Esto se puede hacer sin necesidad de crear un PR. Para agregar un banco, simplemente llama a la siguiente función con el código de Banxico y el nombre del banco:

```python
import clabe
clabe.add_bank('12345', 'New Bank')
```

Para eliminar un banco

```python
import clabe
clabe.remove_bank('12345')
```
