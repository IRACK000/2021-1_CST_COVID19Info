try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

setup(
    name="Windows NT Console API",
    version="0.1",
    description="C",
    author="IRACK",
    author_email="",
    license="MIT",
    ext_modules=[Extension("winAPI", ["pywinAPI.c"])],
    python_requires=">=2.8",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows Only",
    ],
    zip_safe=False,
)
