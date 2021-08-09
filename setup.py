try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='searchtool',
    packages=[
        'search_tool',
    ],
)
