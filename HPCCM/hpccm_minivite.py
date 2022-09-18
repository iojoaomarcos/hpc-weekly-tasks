"""
    sdfsdf
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment

from ensurepip import version


Stage0 += baseimage(image='ubuntu:20.04')

Stage0 += packages(ospackages=['wget', 'ca-certificates'])
Stage0 += shell(commands=[
    'wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb',
    'dpkg -i cuda-keyring_1.0-1_all.deb'
])

Stage0 += packages(ospackages=['git','libtool', 'make', 'cuda'])

# Clang-14
compiler = llvm()
Stage0 += compiler

Stage0 += knem(ldconfig=True, version='1.1.4')

Stage0 += ucx(knem='/usr/local/knem', ldconfig=True, version='1.13.1')

# Mellanox OFED
Stage0 += mlnx_ofed(version='5.0-2.1.8.0')

# OpenMPI
Stage0 += openmpi(version='4.1.4', toolchain=compiler.toolchain, ucx='/usr/local/ucx')



# Stage0 += shell(commands=['cd /var/tmp',
#                           'git clone https://github.com/ECP-ExaGraph/miniVite.git',
#                           'cd miniVite',
#                           'clang main.cpp'])

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

Stage0 += environment(variables={
  'NVIDIA_VISIBLE_DEVICES': 'all',
  'NVIDIA_DRIVER_CAPABILITIES': 'compute,utility',
  'NVIDIA_REQUIRE_CUDA': '"cuda>=10.1 brand=tesla,driver>=384,driver<385 brand=tesla,driver>=396,driver<397 brand=tesla,driver>=410,driver<411"'})

with open('Dockerfile', 'w') as dockerfile:
    dockerfile.write(str(Stage0) + '\n')