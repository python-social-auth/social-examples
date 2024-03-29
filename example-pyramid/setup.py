import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.txt")) as f:
    README = f.read()

with open(os.path.join(here, "CHANGES.txt")) as f:
    CHANGES = f.read()

requires = [
    "pyramid",
    "SQLAlchemy",
    "transaction",
    "pyramid_tm",
    "pyramid_debugtoolbar",
    "zope.sqlalchemy",
    "waitress",
    "pyramid_chameleon",
]

setup(
    name="example",
    version="0.0",
    description="example",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="",
    author_email="",
    url="",
    keywords="web wsgi bfg pylons pyramid",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="example",
    install_requires=requires,
    entry_points="""\
      [paste.app_factory]
      main = example:main
      [console_scripts]
      initialize_example_db = example.scripts.initializedb:main
      """,
)
