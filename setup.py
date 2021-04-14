from setuptools import setup

# https://pymbook.readthedocs.io/en/latest/click.html
# python -m pip install --editable .

setup(
    name='bidicli',
    version='0.1',
    py_modules=['bidicli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        bidicli=bidicli:cli
    ''',
)
