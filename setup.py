from setuptools import setup, find_packages
with open("requirements.txt", "rb") as r:
    install_requires = r.read().decode("utf-8").split("\n")  

# Load the long_description from README.md
with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()
setup(
    name="kkweb",
    version="0.0.1",
    author="Shengyang Wang",
    author_email="shengyang.wang2@dukekunshan.edu.cn",
    description="WebUI for KAKIQUANT AI量化实验室",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KAKIQUANT/kkdatac",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Dependent",
    ],
    python_requires='>=3.10',
    install_requires=install_requires,
    project_urls={
        "Bug Tracker": "https://github.com/KAKIQUANT/kkwebui/issues",
    },
)
