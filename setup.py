from distutils.core import setup, Extension
import os

import_file_template = """ \
def __bootstrap__():                                             
   global __bootstrap__, __loader__, __file__                     
   import sys, pkg_resources, imp                                 
   __file__ = pkg_resources.resource_filename(__name__,'{0}.so')
   __loader__ = None; del __bootstrap__, __loader__               
   imp.load_dynamic(__name__,__file__)                            
                                                                  
if __name__ != "__main__":                                        
    __bootstrap__()                                               
"""

def get_quasirandom_libs(directory):
    filenames = os.listdir(directory)
    
    quasirandom_libs = filter(lambda filename: "module.cpp" in filename, filenames)
    quasirandom_libs = map(lambda filename: filename[:-len("module.cpp")], quasirandom_libs)

    return list(quasirandom_libs)

def setup_quasirandom_libs(directory):
    quasirandom_libs = get_quasirandom_libs(directory)

    # the c++ extension modules
    for quasirandom_lib in quasirandom_libs:
        extension_mod = Extension(quasirandom_lib, sources=["{0}/{1}module.cpp".format(directory, quasirandom_lib)], language="c++", extra_compile_args=["-O3", "-ffast-math", "-mavx2", "-mfma", "-std=c++1y"])

        setup(name = quasirandom_lib, ext_modules=[extension_mod])
        
        with open("{0}/{1}.py".format(directory, quasirandom_lib), "w") as import_file:
            import_file.write(import_file_template.format(quasirandom_lib))

if __name__ == '__main__':
    os.environ["CC"] = "clang++"
    os.environ["CXX"] = "clang++"
    setup_quasirandom_libs("quasirandom")
