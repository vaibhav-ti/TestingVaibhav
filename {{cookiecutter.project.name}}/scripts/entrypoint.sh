set -e

if [[ $STAGE == "PROD" ]]
then
  python3 setup/load_env.py
  python3 manage.py collectstatic --no-input
else
  echo "Not in production"
fi

python3 manage.py makemigrations
python3 manage.py migrate

if [[ $STAGE == "PROD" ]]
then
  gunicorn --bind 0.0.0.0:8000 {{cookiecutter.project.slug}}.wsgi:application
else
  python manage.py runserver 0.0.0.0:8000
fi