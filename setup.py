import setuptools

setuptools.setup(
    name='spassgui',
    version='2.0.0',
    description='Random password generator and manager.',
    url='https://github.com/sorzkode/',
    author='sorzkode',
    author_email='<sorzkode@proton.me>',
    packages=setuptools.find_packages(),
    install_requires=['pyperclip', 'PySimpleGUI', 'tkinter', 'sqlite3'],
    long_description='A random password generator and manager using PySimpleGUI and SQLite3.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: MIT',
        'Operating System :: OS Independent',
        ],
)