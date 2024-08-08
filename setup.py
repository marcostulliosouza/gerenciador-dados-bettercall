from cx_Freeze import setup, Executable
import os

modules = ['configparser', 'PIL']

packages = ['encodings']

include_files = [
    'dbconfig.ini',
    ('assets/', 'assets/'),  # Incluir o diretório 'assets' e seu conteúdo
]

executables = [Executable('app.py', base='Win32GUI')]

setup(
    name='Gerenciador Dados BetterCall',
    version='1.4',
    options={
        'build_exe': {
            'packages': modules + packages,
            'include_files': include_files,
            'include_msvcr': True,
        },
        'bdist_msi': {
            'add_to_path': False,  # Ajuste conforme necessário
            'upgrade_code': '1ecdae60-d54b-4ec1-b553-a6367d5c1934',  # Substitua pelo GUID gerado: https://www.guidgenerator.com/
        }
    },
    executables=executables
)