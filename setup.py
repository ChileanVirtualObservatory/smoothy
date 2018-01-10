from setuptools import setup, find_packages


setup(
    name="smoothy",
    version="0.1.0",
    description="Package that provides an easy interface and I/O operations for using astronomical libraries.",
    url="https://github.com/ChileanVirtualObservatory/smoothy",
    author="CSRG",
    author_email='contact@lirae.cl',
    classifiers=[
        'Intended Audience :: Science/Research',

        'Topic :: Scientific/Engineering :: Astronomy',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
        ],
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['numpy>=1.11.2', 'astropy>=1.2', 'matplotlib>=1.5']
)
