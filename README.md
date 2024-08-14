# CLABE

[![test](https://github.com/cuenca-mx/clabe-python/workflows/test/badge.svg)](https://github.com/cuenca-mx/clabe-python/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/cuenca-mx/clabe-python/branch/main/graph/badge.svg)](https://codecov.io/gh/cuenca-mx/clabe-python)
[![PyPI](https://img.shields.io/pypi/v/clabe.svg)](https://pypi.org/project/clabe/)
[![Downloads](https://pepy.tech/badge/clabe)](https://pepy.tech/project/clabe)

Librería para validar y calcular un número CLABE basado en
https://es.wikipedia.org/wiki/CLABE. 

Además, incluye la clase `Clabe`, un tipo personalizado diseñado
para integrarse con Pydantic, proporcionando un validador
robusto y eficiente para números CLABE dentro de tus
modelos Pydantic. Compatible con Pydantic V1.10.x y V2.x.x

## Requerimientos

Python 3.8 o superior.

## Instalación

Se puede instalar desde Pypi usando

```
pip install clabe
```

## Pruebas

### Requisitos previos

#### Instalar PDM

Usamos PDM como administrador de paquetes y entornos virtuales (virtualenv). 
Esto nos permite ejecutar pruebas unitarias con Pydantic 
tanto en las versiones 1.x.x como 2.x.x. Sigue la [guía oficial](https://pdm-project.org/en/latest/#recommended-installation-method) 
de instalación para instalarlo.

#### Instalar dependencias

El siguiente comando creará dos virtualenv. Uno donde se instala
pydantic V1.x.x y otro donde se instala Pydantic V2. Todo esto
es gestionado por PDM.
```bash
make install
```

### Ejecutar las pruebas

El siguiente comando ejecutará el conjunto de pruebas de ambos
virtualenv y generará un único reporte de pruebas y cobertura.

```bash
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
