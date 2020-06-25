#!/usr/bin/python3.8

from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='Lnpay',
   version='1.0',
   url='https://github.com/Zenitsudeck/Lnpay',
   long_description=long_description,
   description='Lnpay SDK',
   author='Zenitsudeck',
   author_email='',
   packages=['Lnpay'],
   install_requires=['requests'],
)
