FROM ubuntu:20.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        wget && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb && \
    dpkg -i cuda-keyring_1.0-1_all.deb

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        cuda \
        git \
        libtool \
        make && \
    rm -rf /var/lib/apt/lists/*

# LLVM compiler
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        clang \
        libomp-dev && \
    rm -rf /var/lib/apt/lists/*

# KNEM version 1.1.4
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        git && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && cd /var/tmp && git clone --depth=1 --branch knem-1.1.4 https://gitlab.inria.fr/knem/knem.git knem && cd - && \
    mkdir -p /usr/local/knem && \
    cd /var/tmp/knem && \
    mkdir -p /usr/local/knem/include && \
    cp common/*.h /usr/local/knem/include && \
    echo "/usr/local/knem/lib" >> /etc/ld.so.conf.d/hpccm.conf && ldconfig && \
    rm -rf /var/tmp/knem
ENV CPATH=/usr/local/knem/include:$CPATH

# UCX version 1.13.1
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        binutils-dev \
        file \
        libnuma-dev \
        make \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://github.com/openucx/ucx/releases/download/v1.13.1/ucx-1.13.1.tar.gz && \
    mkdir -p /var/tmp && tar -x -f /var/tmp/ucx-1.13.1.tar.gz -C /var/tmp -z && \
    cd /var/tmp/ucx-1.13.1 &&   ./configure --prefix=/usr/local/ucx --disable-assertions --disable-debug --disable-doxygen-doc --disable-logging --disable-params-check --enable-optimizations --with-cuda=/usr/local/cuda --with-knem=/usr/local/knem && \
    make -j$(nproc) && \
    make -j$(nproc) install && \
    echo "/usr/local/ucx/lib" >> /etc/ld.so.conf.d/hpccm.conf && ldconfig && \
    rm -rf /var/tmp/ucx-1.13.1 /var/tmp/ucx-1.13.1.tar.gz
ENV CPATH=/usr/local/ucx/include:$CPATH \
    LIBRARY_PATH=/usr/local/ucx/lib:$LIBRARY_PATH \
    PATH=/usr/local/ucx/bin:$PATH

# Mellanox OFED version 5.0-2.1.8.0
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        gnupg \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN wget -qO - https://www.mellanox.com/downloads/ofed/RPM-GPG-KEY-Mellanox | apt-key add - && \
    mkdir -p /etc/apt/sources.list.d && wget -q -nc --no-check-certificate -P /etc/apt/sources.list.d https://linux.mellanox.com/public/repo/mlnx_ofed/5.0-2.1.8.0/ubuntu20.04/mellanox_mlnx_ofed.list && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ibverbs-providers \
        ibverbs-utils \
        libibmad-dev \
        libibmad5 \
        libibumad-dev \
        libibumad3 \
        libibverbs-dev \
        libibverbs1 \
        librdmacm-dev \
        librdmacm1 && \
    rm -rf /var/lib/apt/lists/*

# OpenMPI version 4.1.4
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        bzip2 \
        file \
        hwloc \
        libnuma-dev \
        make \
        openssh-client \
        perl \
        tar \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://www.open-mpi.org/software/ompi/v4.1/downloads/openmpi-4.1.4.tar.bz2 && \
    mkdir -p /var/tmp && tar -x -f /var/tmp/openmpi-4.1.4.tar.bz2 -C /var/tmp -j && \
    cd /var/tmp/openmpi-4.1.4 &&  CC=clang CXX=clang++ ./configure --prefix=/usr/local/openmpi --disable-getpwuid --enable-orterun-prefix-by-default --with-cuda --with-ucx=/usr/local/ucx --with-verbs && \
    make -j$(nproc) && \
    make -j$(nproc) install && \
    rm -rf /var/tmp/openmpi-4.1.4 /var/tmp/openmpi-4.1.4.tar.bz2
ENV LD_LIBRARY_PATH=/usr/local/openmpi/lib:$LD_LIBRARY_PATH \
    PATH=/usr/local/openmpi/bin:$PATH

ENV CC=mpicxx \
    OMPI_CC=clang \
    OMPI_CXX=clang++

# https://github.com/Exa-Graph/miniVite.git
RUN mkdir -p /var/tmp && cd /var/tmp && git clone --depth=1 --branch master https://github.com/Exa-Graph/miniVite.git miniVite && cd - && \
    cd /var/tmp/miniVite && \
    sed -i '2 s/CXX = CC/CXX = $${CC}/' Makefile && \
    sed -i '10 s/-xHost -qopenmp/-fopenmp/' Makefile && \
    make clean && \
    make && \
    cp miniVite / && \
    rm -rf /var/tmp/miniVite

ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    NVIDIA_REQUIRE_CUDA="cuda>=10.1 brand=tesla,driver>=384,driver<385 brand=tesla,driver>=396,driver<397 brand=tesla,driver>=410,driver<411" \
    NVIDIA_VISIBLE_DEVICES=all


