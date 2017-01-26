from distutils.core import setup

setup(
    name="minions",
    version="0.1.0",
    description="A lightweight todo list application from your command line.",
    author="Rajan Santhanam",
    author_email="rajanpsanthanam@gmail.com",
    license="three-clause BSD",
    url="",
    long_description=__doc__,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers"
    ],
    py_modules=['minion', 'bucket'],
    scripts=['minion']
)
