"""
    HPCCM python template for minivite
    09/2022
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment

from ensurepip import version


Stage0 += baseimage(image='ubuntu:20.04')

compiler = llvm(openmp=True)
Stage0 += compiler

Stage0 += knem(ldconfig=True, version='1.1.4')

Stage0 += ucx(knem='/usr/local/knem', ldconfig=True, version='1.13.1', cuda=False)

# OpenMPI
Stage0 += openmpi(version='4.1.4', toolchain=compiler.toolchain, ucx='/usr/local/ucx', cuda=False, infiniband=False)

Stage0 += environment(variables={"CC": "mpicxx", "OMPI_CC": "clang", "OMPI_CXX": "clang++"})

Stage0 += generic_build(
    branch='master',
    build=[
        "sed -i '2 s/CXX = CC/CXX = $${CC}/' Makefile",
        "sed -i '10 s/-xHost -qopenmp/-fopenmp/' Makefile",
        "make clean",
        "make",
        "cp miniVite /",
    ],
    repository='https://github.com/Exa-Graph/miniVite.git',
)