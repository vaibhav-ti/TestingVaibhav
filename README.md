# Cookiecutter Django 

Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter)

## Features

- For Django
- Works with Python 3.9

## Usage

First, get Cookiecutter. Trust me, it's awesome:

    $ pip install "cookiecutter>=1.7.0"

Now run it against this repo: 

context = [Sample Context](cookiecutter.json)

```python
from cookiecutter.main import cookiecutter

cookiecutter('https://github.com/trilogy-group/process-bp-django-template', no_input=True, overwrite_if_exists=True,
             extra_context=context)
```

Now take a look at your repo. Don't forget to carefully look at the generated README. Awesome, right?