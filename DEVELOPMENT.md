# Development files

Files for assistance in working on this docker image

## Pipenv 

A way to manage pip requirements in a virtual environment: https://pipenv.pypa.io/en/latest/

Installation:

```
pip install --user pipenv
```

Ensure you've set the following environment variable so that pipenv will install the virtual environment to this local directory:
```
export PIPENV_VENV_IN_PROJECT=1
```

When you want to install a requirement using pipenv, run `pipenv install <dependency>`.
For example, if I wanted to install the requests package: `pipenv install requests`, and it'll save to the Pipfile.

To run the python scripts locally, run `pipenv run python $(pwd)/src/main.py`