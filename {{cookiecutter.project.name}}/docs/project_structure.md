# Main app
The main django app is {{cookiecutter.project.slug}}. This is a standard django app with the required settings for wsgi and asgi. 

It also divides the settings into 3 separate files.
- [base settings](../%7B%7Bcookiecutter.project.slug%7D%7D/settings/base.py) includes the base settings that the application will have in all environments
- [dev settings](../%7B%7Bcookiecutter.project.slug%7D%7D/settings/dev.py) and [prod settings](../%7B%7Bcookiecutter.project.slug%7D%7D/settings/prod.py) represent the settings required exclusively in dev and prod environments respectively

# Additional Apps
While the main app is the entrypoint into the entire application, it's not supposed to have any actual business logic. Each logically distinct part of the project should be in it's own separate app. As an example [accounts](../accounts/) is an app that deals with user accounts and user management exclusively 
