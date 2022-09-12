import setuptools

setuptools.setup(
    name='spassgui',
    version='1.0.0',
    description='Random password generator.',
    url='https://github.com/sorzkode/',
    author='sorzkode',
    author_email='<sorzkode@proton.me>',
    packages=setuptools.find_packages(),
    install_requires=['Pillow', 'clipboard', 'tkinter'],
    long_description='A random password generator with a tkinter GUI.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: MIT',
        'Operating System :: OS Independent',
        ],
)