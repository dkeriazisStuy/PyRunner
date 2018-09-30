import tempfile
import time
import signal
import docker
import shutil
import os
import os.path
import json
import multiprocessing

client = docker.from_env()

class TimeOutException(Exception):
    pass

def pull_image(image_name, debug):
    try:
        client.images.get(image_name)
    except docker.errors.ImageNotFound:
        if debug:
            print('Pulling {image_name}, this may take a while'.format(
                image_name=image_name
            ))
        name, tag = image_name.split(':')
        client.images.pull(name, tag=tag)

def get_dockerfile(cmd):
    return '''
        FROM python:3.7-alpine
        COPY . /root
        WORKDIR /root
        CMD {cmd}
    '''.format(cmd=cmd)

def make_dockerfile(temp_dir, py_file, arg_list):
    _, path = tempfile.mkstemp(dir=temp_dir)
    with open(path, 'w') as f:
        cmd = ["python", py_file] + arg_list
        dockerfile = get_dockerfile(json.dumps(cmd))
        f.write(dockerfile)
        return path

def build_image(d, filename, args, debug):
    dockerfile_path = make_dockerfile(d, filename, args)
    shutil.copy(filename, d)
    image, stream = client.images.build(
            path=d,
            rm=True,
            dockerfile=dockerfile_path
        )
    if debug:
        for s in stream:
            if 'stream' in s:
                print(s['stream'], end='')
    os.remove(dockerfile_path)
    return image

def run_container(d, image):
    mount = docker.types.Mount(type='bind', source=d, target='/root')
    container = client.containers.run(
            image=image.id,
            mounts=[mount],
            detach=True
        )
    return container

def get_stream(container):
    return container.logs(stream=True)

def teardown(image, container):
    if container is not None:
        try:
            container.kill()
        except docker.errors.APIError:
            pass
        container.remove()
    if image is not None:
        client.images.remove(image=image.id)

def container_stream(container):
    for s in get_stream(container):
        print(s.decode('utf8'), end='')

def start_container_stream(container, timeout):
    # Process will call container_stream(container) when started
    p = multiprocessing.Process(target=lambda: container_stream(container))
    p.start()
    # Wait until process times out or completes
    p.join(timeout)
    if p.is_alive():  # If thread is still active
        p.terminate()
        p.join()

def run_file(filename, args=None, timeout=10, debug=False):
    if args is None:
        args = []
    image = None
    container = None
    try:
        pull_image('python:3.7-alpine', debug)
        d = tempfile.mkdtemp(dir=os.path.abspath('.'))
        image = build_image(d, filename, args, debug)
        container = run_container(d, image)
        start_container_stream(container, timeout)
    finally:
        teardown(image, container)

if __name__ == "__main__":
    #  run_file('_baz.py', args=['in_file.txt', 'out_file.txt'], debug=True)
    run_file('_loop.py', debug=True)

