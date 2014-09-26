# Automatically generated by configure - do not modify
# Configured with: './configure.sh'
all:
prefix=/usr/local
bindir=${prefix}/bin
libdir=${prefix}/lib
mandir=${prefix}/share/man
datadir=${prefix}/share/charm
sysconfdir=${prefix}/etc
docdir=${prefix}/share/doc/charm
confdir=${prefix}/etc/charm
ARCH=x86_64
VERSION=0.42
PKGVERSION=
SRC_PATH=/home/andkof/Downloads/Charm-Crypto-0.42
TARGET_DIRS=
CONFIG_UNAME_RELEASE=""
TOOLS=
MAKE=make
INSTALL=install
INSTALL_DIR=install -d -m0755 -p
INSTALL_DATA=install -m0644 -p
INSTALL_PROG=install -m0755 -p
CC=gcc
CPP=gcc -E
HOST_CC=gcc
AR=ar
LD=ld
LIBTOOL=
CFLAGS=-O2 -g 
CHARM_CFLAGS=-m64 -Wall -Wundef -Wwrite-strings -Wmissing-prototypes  -fstack-protector-all -Wendif-labels -Wmissing-include-dirs -Wempty-body -Wnested-externs -Wformat-security -Wformat-y2k -Winit-self -Wignored-qualifiers -Wold-style-declaration -Wold-style-definition -Wtype-limits
CHARM_INCLUDES=-I. -I$(SRC_PATH)
HELPER_CFLAGS=
LDFLAGS=-m64 
CPPFLAGS=
ARLIBS_BEGIN=
ARLIBS_END=
LIBS+=
LIBS_TOOLS+=
PYTHON=/usr/bin/python
INT_MOD=yes
ECC_MOD=yes
PAIR_MOD=yes
USE_PBC=yes
USE_GMP=yes
USE_MIRACL=no
DISABLE_BENCHMARK=no
wget=/usr/bin/wget
HAVE_LIBM=yes
HAVE_LIBGMP=yes
HAVE_LIBPBC=no
HAVE_LIBCRYPTO=yes
PYPARSING=