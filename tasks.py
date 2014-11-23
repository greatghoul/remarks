from invoke import run, task

@task
def test():
    run('python test.py')