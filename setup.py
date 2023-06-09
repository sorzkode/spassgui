import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='spassgui',
    version='2.0.0',
    description='Random password generator and manager.',
    url='https://github.com/sorzkode/',
    author='Mister Riley',
    author_email='<sorzkode@proton.me>',
    packages=setuptools.find_packages(),
    install_requires=['pyperclip', 'PySimpleGUI', 'tkinter', 'cryptography'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
