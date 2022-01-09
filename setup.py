#!/usr/bin/env python
#import setuptools
from setuptools import find_packages,setup
#from distutils.core import setup

with open("./PCILib/README.md", 'r', encoding='utf-8') as f1:
    long_description1 = f1.read()

setup(name = 'PCILib',     # 包名
      version = '0.0.2',  # 版本号
      description = 'PCILib for python',
      long_description = long_description1, 
      author = 'PCI',
      author_email = 'you@example.com',
      url = 'https://github.com/HyperPh/PCILib',
      license = 'Apache-2.0',
      install_requires = [],
      classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities'
      ],
      keywords = 'pci',
      packages = find_packages(),  # 必填，就是包的代码主目录，一般是'src'，此处让它自动寻找含有
      #package_dir = {'':'src'},
      include_package_data = True,
      #python_requires='>=3.8',
)

