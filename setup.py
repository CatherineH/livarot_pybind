from glob import glob
import os
import sys
import sysconfig
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
            env = os.environ

            if os.path.exists('/usr/bin/gcc-8'):
                env['CC']='/usr/bin/gcc-8'
            if os.path.exists('/usr/bin/g++-8'):
                env['CXX'] = '/usr/bin/g++-8'

            # Config
            extra_config_args = []
            extra_config_args.append(f"-DPYTHON_LIBRARIES={sysconfig.get_config_var('LIBDEST')}")
            extra_config_args.append(f"-DPYTHON_INCLUDE_DIRS={sysconfig.get_config_var('INCLUDEPY')}") # this might need to be the subdir
            extra_config_args.append(f"-DPYTHON_EXECUTABLE={sys.executable}")
            extra_config_args.append(f"-DPYTHON_MAJOR={sys.version_info.major}")
            extra_config_args.append(f"-DPYTHON_MINOR={sys.version_info.minor}")
            extra_config_args.append("-DCMAKE_POSITION_INDEPENDENT_CODE=ON")
            if os.path.exists('/usr/include/boost69'):
                extra_config_args.append(f"-DBOOST_INCLUDEDIR=/usr/include/boost169")
            if os.path.exists('/usr/lib64/boost169/'):
                extra_config_args.append(f"-DBOOST_LIBRARYDIR=/usr/lib64/boost169")
            subprocess.check_call(['cmake', "-S", extdir]+extra_config_args, cwd=self.build_temp, env=env)
            
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
        pylivarot_sos = glob(os.path.join(self.build_temp, f"*{sys.version_info.major}{sys.version_info.minor}*.so"))
        if len(pylivarot_sos) == 0:
            raise FileNotFoundError(f"could not find *{sys.version_info.major}{sys.version_info.minor}*.so in {os.listdir(self.build_temp)}")
        for _file in pylivarot_sos:
            print("copying ", _file," to ", os.path.join(lib_dir, os.path.basename(_file)))
            shutil.move(_file, os.path.join(lib_dir, os.path.basename(_file)))
        

setup(
      packages=['pylivarot'],
      ext_modules = [Extension("pylivarot", ["pybind11", "lib2geom"])],
      cmdclass = {'build_ext': cmake_build_ext}
)
