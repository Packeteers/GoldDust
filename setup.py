# Copyright 2015-2017 John "LuaMilkshake" Marion
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

setup(
    name='golddust',
    version='0.0.1',
    description='A package manager for modded Minecraft.',
    url='https://github.com/Packeteers/GoldDust',
    author='John Marion',
    author_email='jmariondev@gmail.com',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',

        'Topic :: Games/Entertainment',
        'Topic :: System :: Software Distribution',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'gdgame=golddust.clitools.gdgame:GDGameTool'
        ],
    },
    keywords='minecraft forge mods packages',
)
