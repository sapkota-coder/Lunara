from setuptools import setup

setup(
    name='owl',  # Name of your project
    version='0.1.0',  # Version of your package
    py_modules=['owl'],  # Name of your single module file without .py
    install_requires=[
        'transformers',  # Add any dependencies your project needs
        'torch',
        'sumy',
        'pdf2docx',
    ],
    author='Ankit Sapkota',
    author_email='sapkotasa8@gmail.com',  # Replace with your email
    description='A collection of useful text processing modules.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/owl',  # Replace with your project's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust as necessary
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
)
