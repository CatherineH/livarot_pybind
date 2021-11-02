from glob import glob
import os
import shutil
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import platform

class cmake_build_ext(build_ext):
    # adapted from https://martinopilia.com/posts/2018/09/15/building-python-extension.html
    def build_extensions(self):
        
        # Ensure that CMake is present and working
        try:
            _ = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError('Cannot find CMake executable')

        for _ in self.extensions:

            extdir = os.path.abspath(os.path.dirname(__file__))

            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)

            # Config
            subprocess.check_call(['cmake', "-S", extdir], cwd=self.build_temp)
            
            # Build
            if platform.system() == 'Windows':
                subprocess.check_call(['cmake', '--build', '.', '--config', 'Release'],
                            cwd=self.build_temp)
            else:
                subprocess.check_call(['cmake', '--build', '.'],
                            cwd=self.build_temp)
        # copy all the built files into the lib dir. Not sure why this is needed; it feels like setuptools should 
        # copy the built files into the bdist by default
        lib_dir = os.path.join(self.build_lib, "pylivarot")
        for _file in glob(os.path.join(self.build_temp, "*.so")):
            print("copying ", _file," to ", os.path.join(lib_dir, os.path.basename(_file)))
            shutil.move(_file, os.path.join(lib_dir, os.path.basename(_file)))
        

setup(name='pylivarot',
      version='1.0',
      description='Python bindings to Inkscape\'s livarot library',
      author='Catherine Holloway',
      author_email='milankie@gmail.com',
      url='https://github.com/CatherineH/livarot_pybind',
      packages=['pylivarot'],
      ext_modules = [Extension("pylivarot", [])],
      cmdclass = {'build_ext': cmake_build_ext}
)
