from distutils.core import setup
from glob import glob

print(glob('pylivarot/_pylivarot.*.so'))
setup(name='pylivarot',
      version='1.0',
      description='Python bindings to Inkscape\'s livarot library',
      author='Catherine Holloway',
      author_email='milankie@gmail.com',
      url='https://github.com/CatherineH/livarot_pybind',
      packages=['pylivarot'],
      package_data={'pylivarot': glob('pylivarot/*.so')},
     )