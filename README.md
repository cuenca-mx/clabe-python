# CLABE

[![test](https://github.com/cuenca-mx/clabe-python/workflows/test/badge.svg)](https://github.com/cuenca-mx/clabe-python/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/cuenca-mx/clabe-python/branch/main/graph/badge.svg)](https://codecov.io/gh/cuenca-mx/clabe-python)
[![PyPI](https://img.shields.io/pypi/v/clabe.svg)](https://pypi.org/project/clabe/)
[![Downloads](https://pepy.tech/badge/clabe)](https://pepy.tech/project/clabe)

Librería para validar y calcular un número CLABE basado en
https://es.wikipedia.org/wiki/CLABE

## Requerimientos

Python 3.8 o superior.

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

### Como tipo personalizado en un modelo de Pydantic

```python
from pydantic import BaseModel, ValidationError

from clabe import Clabe


class Account(BaseModel):
    id: str
    clabe: Clabe


account = Account(id='123', clabe='723010123456789019')
print(account)
"""
id='123' clabe='723010123456789019'
"""

try:
    account = Account(id='321', clabe='000000000000000011')
except ValidationError as exc:
    print(exc)
"""
1 validation error for Account
clabe
  código de banco no es válido [type=clabe.bank_code, input_value='000000000000000011', input_type=str]
"""
```

### Obtener el dígito de control de un número CLABE

```python
import clabe
clabe.compute_control_digit('00200000000000000')
```

### Para validar si un número CLABE es válido

```python
import clabe
clabe.validate_clabe('002000000000000008')
```

### Para obtener el banco a partir de 3 dígitos

```python
import clabe
clabe.get_bank_name('002')
```

### Para generar nuevo válido CLABES

```python
import clabe
clabe.generate_new_clabes(10, '002123456')
```

## Agregar un nuevo banco

A partir de la versión **2.0.0**, el paquete ha sido actualizado para utilizar **Pydantic v2**, lo que implica que las versiones anteriores ya no recibirán soporte ni actualizaciones.

No obstante, en versiones anteriores hemos agregado una función que permite añadir bancos adicionales a la lista sin necesidad de crear un PR. Esto es útil para quienes aún utilicen versiones anteriores. Sin embargo, a partir de la versión 2, continuaremos manteniendo y actualizando la lista oficial de bancos mediante PRs en el repositorio.

### Cómo agregar un banco

Para agregar un banco, llama a la función `add_bank` pasando el código de Banxico y el nombre del banco como parámetros.

```python
import clabe
clabe.add_bank('12345', 'New Bank')
```

### Cómo eliminar un banco

De manera similar, puedes eliminar un banco llamando a la función remove_bank con el código del banco que deseas eliminar.

```python
import clabe
clabe.remove_bank('12345')
```

**Nota**: Aunque estas funciones están disponibles para un uso más flexible, recomendamos utilizar siempre la lista oficial de bancos actualizada en la versión 2+.

## Mantener actualizada la lista de participantes

Para mantener sincronizada la lista de participantes del SPEI con la información oficial de Banxico, este repositorio incluye un script que compara automáticamente los datos locales con la lista actualizada de instituciones financieras.

### Verificar cambios en la lista de participantes

El script `compare_banks.py` detecta:

- **Nuevos participantes**: Instituciones que aparecen en Banxico pero no están en el paquete
- **Bajas de participantes**: Instituciones que ya no aparecen en la lista oficial de Banxico
- **Cambios de nombre**: Participantes que mantienen el mismo código pero han cambiado su nombre

Para ejecutar la verificación:

```bash
export PYTHONPATH=$(pwd)
python scripts/compare_banks.py
```

### Interpretar los resultados

El script mostrará un reporte con las diferencias encontradas:

- **ADDITIONS**: Nuevos participantes que deben agregarse al archivo `clabe/banks.py`
- **REMOVALS**: Participantes que deben eliminarse por ya no estar activos
- **CHANGES**: Cambios de nombre que requieren actualización

Si no hay diferencias, el script confirmará que los datos están sincronizados.

### Actualizar la lista de participantes

Una vez identificados los cambios, actualiza manualmente el archivo `clabe/banks.py` y crea un pull request para mantener la lista actualizada.