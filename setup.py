from cx_Freeze import setup, Executable

modules = ['configparser', 'PIL']

packages = ['encodings']

include_files = ['dbconfig.ini', 'assets/seta_direita.png', 'assets/seta_esquerda.png']

executables = [Executable('app.py', base='Win32GUI')]

setup(
    name='Gerenciador Dados BetterCall',
    version='1.3',
    options={
        'build_exe': {
            'packages': modules + packages,
            'include_files': include_files,
            'include_msvcr': True,
        }
    },
    executables=executables
)
