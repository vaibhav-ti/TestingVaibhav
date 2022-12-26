# Lint Codebase
Use the following command to lint the entire codebase
```bash
bash scripts/lint.sh
```

# Django PyLint

If you're running pylint manually, remember to set PYTHONPATH so that pylint can find the project settings module
```commandline
export PYTHONPATH='.'
```

In order to access some of the internal Django features to improve pylint inspections, you should also provide a Django settings module appropriate to your project.
This can be done either with an environment variable:

```commandline
DJANGO_SETTINGS_MODULE={{cookiecutter.project.slug}}.settings pylint --load-plugins pylint_django [..other options..] <path_to_your_sources>
```

Alternatively, this can be passed in as a commandline flag:


```commandline
pylint --load-plugins pylint_django --django-settings-module={{cookiecutter.project.slug}}.settings [..other options..] <path_to_your_sources>
```

If you do not configure Django, default settings will be used but this will not include, for example, which applications to include in INSTALLED_APPS and so the linting and type inference will be less accurate. It is recommended to specify a settings module.

### Prospector
If you have `prospector` installed, then `pylint-django` will already be installed as a dependency, and will be activated automatically if Django is detected:

```
prospector [..other options..]
```

### Features
- Prevents warnings about Django-generated attributes such as `Model.object`s or `Views.request`.
- Prevents warnings when using `ForeignKey` attributes (“Instance of ForeignKey has no <x> member”).
- Fixes pylint’s knowledge of the types of Model and Form field attributes
- Validates `Model.__unicode__` methods.
- `Meta` informational classes on forms and models do not generate errors.
- Flags dangerous use of the exclude attribute in ModelForm.Meta.
- Uses Django’s internal machinery to try and resolve models referenced as strings in ForeignKey fields. That relies on `django.setup()` which needs the appropriate project settings defined!


### Additional plugins
`pylint_django.checkers.migrations` looks for migrations which:

- add new model fields and these fields have a default value. According to [Django docs](https://docs.djangoproject.com/en/2.0/topics/migrations/#postgresql) this may have performance penalties especially on large tables. The preferred way is to add a new DB column with `null=True` because it will be created instantly and then possibly populate the table with the desired default values. Only the last migration from a sub-directory will be examined;
- are `migrations.RunPython()` without a reverse callable - these will result in non reversible data migrations;

This plugin is disabled by default! To enable it:
```
pylint --load-plugins pylint_django --load-plugins pylint_django.checkers.migrations
```