# INSTALLATION MANUAL

## Python Virtual Environment

Create a new _Python virtual environment_ with the following command:

```bash
python3 -m venv venv
```

The command might differ depending on your operating system. The above command is for _Linux_. Consult [this documen](https://docs.python.org/3/library/venv.html "Python venv — Creation of virtual environments") to find the correct command for your operating system.

**This software was built using Python version 3.10.12**. You can check your Python version with the following command:

```bash
python3 -V
```

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
