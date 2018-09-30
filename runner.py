import tempfile
import time
import signal
import docker
import shutil
import os
import os.path

client = docker.from_env()

def pull_image(image_name):
    try:
        client.images.get(image_name)
    except docker.errors.ImageNotFound:
        print('Pulling {image_name}, this may take a while'.format(image_name=image_name))
        name, tag = image_name.split(':')
        client.images.pull(name, tag=tag)

def get_dockerfile(py_file):
    return '''
        FROM python:3.7-alpine
        COPY . /root
        WORKDIR /root
        CMD ["python", "{file}"]
    '''.format(file=py_file)

def make_dockerfile(temp_dir, py_file):
    _, path = tempfile.mkstemp(dir=temp_dir)
    with open(path, 'w') as f:
        dockerfile = get_dockerfile(py_file)
        f.write(dockerfile)
        return path

def run_file(filename):
    pull_image('python:3.7-alpine')
    d = tempfile.mkdtemp(dir=os.path.abspath('.'))

    dockerfile_path = make_dockerfile(d, filename)
    shutil.copy(filename, d)
    image, stream = client.images.build(path=d, rm=True, dockerfile=dockerfile_path)
    for s in stream:
        if 'stream' in s:
            print(s['stream'], end='')
    os.remove(dockerfile_path)

    mount = docker.types.Mount(type='bind', source=d, target='/root')
    container = client.containers.run(image=image.id, mounts=[mount], detach=True)

    stream = container.logs(stream=True)
    for s in stream:
        print(s.decode('utf8'), end='')

    container.remove()
    client.images.remove(image=image.id)

run_file('baz.py')
