from cx_Freeze import setup, Executable

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
        }
    },
    executables=executables
)