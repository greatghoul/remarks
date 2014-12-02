from invoke import run, task

@task
def test():
    run('python test.py')

@task
def install():
    run('sudo pip install -r requirements.txt')