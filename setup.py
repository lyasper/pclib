from distutils.core import setup, Extension

stdbuf = Extension('pclib/stdbuf', sources = ['src/bufmod.c'])
portfwd = Extension('pclib/portfwd', sources = ['src/portfwd.c'])

setup(
    name='pycommonlib',
    version='0.0.1',
    author='zz',
    author_email='zz7a5pe4@gmail.com',
    packages=['pclib'],
    license='LICENSE',
    url='https://github.com/zz7a5pe4/pclib',
    long_description=open('README').read(),
    description='Useful python tools',
    ext_modules = [stdbuf, portfwd]
)
