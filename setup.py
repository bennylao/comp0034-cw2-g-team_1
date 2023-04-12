from setuptools import find_packages, setup

setup(
    name='crayfish_analysis_app',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask-wtf",
        "flask-sqlalchemy",
        "Flask-WTF",
        "flask-marshmallow",
        "marshmallow-sqlalchemy",
        "pandas",
        "requests",
    ],
)
