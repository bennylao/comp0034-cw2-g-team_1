from setuptools import setup

setup(
    name="comp0034-cw2-team-01",
    version="1.0.0",
    packages=["flask_app"],
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["flask"],
)
