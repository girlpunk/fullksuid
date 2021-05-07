from setuptools import setup

setup(
    name="fullksuid",
    version="1.2.1",
    description="KSUID Implementation in python",
    url="https://github.com/cyberjacob/fullksuid",
    license="MIT",
    author="foxocube",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["fullksuid"],
    include_package_data=True,
    install_requires=["netifaces", "pybase62"]
)
