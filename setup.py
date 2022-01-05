from setuptools import setup, find_packages

setup(
    name='forest-timer',
    version='1.0.0',
    url='https://github.com/RayYangFromOrderly/forest-timer',
    license='BSD',
    description='Little pretty printer for nested for-loops',
    author='RayYang',
    author_email='ray.yang@ezorderly.com',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    install_requires=['setuptools', 'termcolor'],

)
