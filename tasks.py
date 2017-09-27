from invoke import task


@task
def startup(ctx):
    """
    Installs packages from requirements, runs database migration,
    creates superuser for demo purposes.
    """
    ctx.run('pip install -r requirements.txt')
    ctx.run('python3 manage.py makemigrations')
    ctx.run('python3 manage.py migrate')
    create_superuser()


def create_superuser():
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keypr.settings')
    django.setup()

    from django.contrib.auth.models import User
    User.objects.create_superuser('test', 'test@example.com', 'test')
