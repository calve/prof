from distutils.core import setup

setup(
    name='prof',
    packages=['prof'],
    version='1.0',
    description='A tool to upload student work to http://prof.fil.univ-lille1.fr',
    author='calve',
    author_email='calvinh34@gmail.com',
    url='http://github.com/calve/prof',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Environment :: Console',
    ],
    install_requires=[
        "requests",
    ]
)
