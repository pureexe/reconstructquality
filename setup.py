import setuptools

setuptools.setup(
    name="reconstructquality",
    version="0.0.1",
    author="Vision and Learning lab",
    author_email="allist@vistec.ac.th",
    description="Calculate reconstruction quality",
    url="https://github.com/pureexe/reconstructquality",
    packages=[''],
    py_modules=['reconstructquality'],
    install_requires=[
          'scikit-image',
          'pandas'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
     'console_scripts': ['reconstructquality=reconstructquality:entry_point'],
    },
    python_requires='>=3.6'
)