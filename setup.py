#!/usr/bin/env python

"""Python setuptools modules for building/installing/distributing"""

import os

from setuptools import setup, find_packages

from snakeoil import distutils_extensions as snk_distutils
from snakeoil.version import __version__
OptionalExtension = snk_distutils.OptionalExtension


class mysdist(snk_distutils.sdist):
    """sdist command specifying the right files and generating ChangeLog."""

    package_namespace = 'snakeoil'
    old_verinfo = False

    def _add_to_file_list(self):
        self.filelist.include_pattern('.h', prefix='include/snakeoil')
        self.filelist.include_pattern('doc/*')


class snakeoil_build_py(snk_distutils.build_py):

    package_namespace = 'snakeoil'
    generate_verinfo = True

    def _inner_run(self, py3k_rebuilds):
        snk_distutils.build_py._inner_run(self, py3k_rebuilds)

        # distutils is stupid.  restore +x on appropriate scripts
        for script_name in ("caching_2to3.py", "pyflakes_extension.py"):
            path = os.path.join(self.build_lib, 'snakeoil', script_name)
            mode = os.stat(path).st_mode
            # note, we use the int here for python3k compatibility.
            # 365 == 0555, 4095 = 0777
            os.chmod(path, ((mode | 365) & 4095))


common_includes = [
    'include/snakeoil/heapdef.h',
    'include/snakeoil/common.h',
]

extra_kwargs = dict(
    depends=common_includes,
    include_dirs=['include'],
)

extensions = []

if not snk_distutils.is_py3k:
    extensions.extend([
        OptionalExtension(
            'snakeoil._posix', ['src/posix.c'], **extra_kwargs),
        OptionalExtension(
            'snakeoil._klass', ['src/klass.c'], **extra_kwargs),
        OptionalExtension(
            'snakeoil._caching', ['src/caching.c'], **extra_kwargs),
        OptionalExtension(
            'snakeoil._lists', ['src/lists.c'], **extra_kwargs),
        OptionalExtension(
            'snakeoil.osutils._readdir', ['src/readdir.c'], **extra_kwargs),
        OptionalExtension(
            'snakeoil._formatters', ['src/formatters.c'], **extra_kwargs),
        OptionalExtension(
            'snakeoil.chksum._whirlpool_cdo', ['src/whirlpool_cdo.c'], **extra_kwargs),
        ])

cmdclass = {
    'sdist': mysdist,
    'build_ext': snk_distutils.build_ext,
    'build_py': snakeoil_build_py,
}

setup(
    name='snakeoil',
    version=__version__,
    description='misc common functionality, and useful optimizations',
    url='https://github.com/pkgcore/snakeoil',
    license='BSD',
    author='Brian Harring',
    author_email='ferringb@gmail.com',
    packages=find_packages(),
    ext_modules=extensions,
    cmdclass=cmdclass,
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
