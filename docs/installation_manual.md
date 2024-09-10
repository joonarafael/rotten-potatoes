# INSTALLATION MANUAL

## Python & Python Virtual Environment

**This software was built using Python version 3.10.12**. Software will likely run on other versions as well, but if you begin to encounter issues, consider installing Python 3.10.12. If you've got the Python version binaries downloaded, you can initialize the virtual environment to use the correct Python version.

Other options include global installation, as well as the managing of multiple Python versions (and specific Python versions within specific directories) with a dedicated tool, like [pyenv](https://github.com/pyenv/pyenv "Simple Python Version Management: pyenv").

You can check your Python version with the following command:

```bash
python3 -V
```

Create a new _Python virtual environment_ with the following command:

```bash
python3 -m venv venv
```

The command might differ depending on your operating system. The above command is for _Linux_. Consult [this documen](https://docs.python.org/3/library/venv.html "Python venv — Creation of virtual environments") to find the correct command for your operating system.

To activate the virtual environment, use the following command:

```bash
source venv/bin/activate
```

To deactivate the virtual environment, use the following command:

```bash
deactivate
```

## Install Dependencies

After activating the virtual environment, install the required dependencies with the following command:

```bash
pip install -r requirements.txt
```
