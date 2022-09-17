"""
    sdfsdf
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment

from ensurepip import version


Stage0 += baseimage(image='ubuntu:20.04')
Stage0 += packages(ospackages=['git','libtool', 'make'])

# Clang-14
compiler = llvm()
Stage0 += compiler

# OpenMPI
Stage0 += openmpi(version='4.1.4', toolchain=compiler.toolchain, ucx='/usr/local/ucx')



Stage0 += shell(commands=['cd /var/tmp',
                          'git clone https://github.com/ECP-ExaGraph/miniVite.git',
                          'cd miniVite'
                          'clang++-14 main.cpp'])


