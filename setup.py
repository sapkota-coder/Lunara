from setuptools import setup

setup(
    name='owl',
    version='0.1.0',
    py_modules=['owl'],
    install_requires=[
        'transformers',
        'torch',
        'sumy',
        'pdf2docx',
    ],
    author='Ankit Sapkota',
    author_email='sapkotasa8@gmail.com',
    description='A collection of useful text processing modules.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sapkota-coder/owl', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
)
