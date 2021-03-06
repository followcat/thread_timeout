#!/usr/bin/python
from setuptools import setup, find_packages, Command


class PyTest(Command):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import nose
        nose.run(argv=['', 'run_test.py', '-v'])


setup(name='thread_timeout',
      version='1.0',
      description='''Decorator to execute functionin in
        separate thread with timeout''',
      author='George Shuklin, followcat',
      author_email='george.shuklin@gmail.com, followcat@gmail.com',
      url='https://github.com/followcat/thread_timeout',
      packages=find_packages(),
      install_requires=[],
      cmdclass = {'test': PyTest},

      license='LGPL',
      classifiers=[
                   "Development Status :: 4 - Beta",
                   "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
                   "Topic :: Software Development :: Libraries"
      ],
      )
