from importlib.machinery import SourceFileLoader

import setuptools

version = SourceFileLoader('version', 'clabe/version.py').load_module()


test_requires = [
    'pytest==5.4.3',
    'pytest-cov==2.10.0',
    'black==19.10b0',
    'isort==5.0.4',
    'flake8==3.8.3',
    'mypy==0.782',
]

with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='clabe',
    version=version.__version__,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Validate and generate the control digit of a CLABE in Mexico',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/clabe',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data=dict(clabe=['py.typed']),
    install_requires=['pydantic>=1.4,<2.0'],
    setup_requires=['pytest-runner'],
    tests_require=test_requires,
    extras_require=dict(test=test_requires),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
