from setuptools import setup

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='dstack-bot',
    version='1.1.6',
    description=(
        'Simple bot that allows you to run commands on your server using invoke'),
    long_description=long_description,
    url='https://github.com/obitec/dstack-bot',
    author='J Minnaar',
    author_email='jr.minnaar+pypi@gmail.com',
    license='MIT License',
    keywords='automation deploy telegram bots server administration',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Software Distribution',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=['dstack_bot', ],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'invoke',
        'python-dotenv',
        'python-telegram-bot',
    ],
    extras_require={
        'dev': [
            'sphinx',
            'twine',
            'wheel',
        ],
        'stats': [
            'psutil',  # easier to install with conda
        ]
    },
    entry_points={
        'console_scripts': ['dbot = dstack_bot.main:main']
    }
)
