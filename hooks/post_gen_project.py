import os
import shutil



def append_to_gitignore_file(ignored_line):
    with open(".gitignore", "a") as gitignore_file:
        gitignore_file.write(ignored_line)
        gitignore_file.write("\n")


REMOVE_PATHS = [
    '.github/workflows/publish.yml',
    # Auth
    {% if not cookiecutter.authentication.enabled == 'True' %}
        'tests/test_auth.py',
    {% endif %}

    # Documentation
    {% if not cookiecutter.documentation.readme.enabled == 'True' %}
        'README.md',
        'docs',
    {% endif %}

    # Configuration
    {% if not cookiecutter.configuration.linter.enabled == "True" %}
        '.pylintrc',
    {% endif %}
    {% if not cookiecutter.configuration.local_debugger.enabled == "True" %}
        '.vscode/launch.json',
    {% endif %}
    {% if not cookiecutter.configuration.dockerfile.enabled == "True" %}
        '.dockerignore',
        'Dockerfile',
        'docker-compose.yml',
    {% endif %}
    {% if not cookiecutter.configuration.logger.enabled == "True" %}
        '{{cookiecutter.project.slug}}/settings/logger.py',
    {% endif %}

    # Deployment
    {% if cookiecutter.deployment.selected != 'ECS (CDK) - Recommended' %}
        'cdk-deployment',
        '.github/workflows/deploy.yml',
    {% endif %}
    {% if cookiecutter.deployment.selected != 'EYK' %}
        '.github/workflows/eyk.yml',
        'Procfile',
    {% endif %}
    # Tests
    {%- if not cookiecutter.tests.enabled == 'True' %}
        'conftest.py',
        '{{cookiecutter.project.slug}}/tests',
        '.github/workflows/pytest.yml',
    {%- endif %}

    # CI/ CD
    {% if cookiecutter.deployment.selected != 'ECS (CDK) - Recommended' %}
        '.github/workflows/deploy.yml',
    {%- endif %}
    {% if cookiecutter.deployment.selected != 'EYK' %}
        '.github/workflows/eyk.yml',
    {%- endif %}
    {% if not cookiecutter.ci_cd.testing.enabled == 'True' %}
        '.github/workflows/pytest.yml',
        '.github/workflows/pytest-coverage.yml',
        'pytest.ini',
    {%- endif %}
    {% if not cookiecutter.ci_cd.code_analysis.enabled == 'True' %}
        '.github/workflows/analysis.yml',
    {%- endif %}
    {% if not cookiecutter.ci_cd.test_coverage.enabled == 'True' %}
        '.github/workflows/pytest-coverage.yml',
    {%- endif %}
    {% if not cookiecutter.ci_cd.linting.enabled == 'True' %}
        '.github/workflows/lint.yml',
    {%- endif %}

    {% if cookiecutter.configuration.xray.enabled != 'True' or cookiecutter.deployment.selected == 'EYK' %}
        'xray',
    {%- endif %}
]

def main():
    append_to_gitignore_file(".env")
    append_to_gitignore_file(".envs/*")
    for path in REMOVE_PATHS:
        path = path.strip()
        if path and os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)




if __name__ == "__main__":
    main()