import json
import multiprocessing
import os
import os.path
import shutil
import tempfile
import docker

# Create docker client from environment
client = docker.from_env()

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

def get_dockerfile(image, cmd):
    return '''
        FROM {image}
        COPY . /root
        WORKDIR /root
        CMD {cmd}
    '''.format(image=image, cmd=cmd)

def make_dockerfile(temp_dir, image, py_file, arg_list):
    _, path = tempfile.mkstemp(dir=temp_dir)
    with open(path, 'w') as f:
        cmd = ["python", py_file] + arg_list
        dockerfile = get_dockerfile(image, json.dumps(cmd))
        f.write(dockerfile)
        return path

def build_image(d, image, filename, args, debug):
    pull_image(image, debug)
    dockerfile_path = make_dockerfile(d, image, filename, args)
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
    stream = container.logs(stream=True)
    for s in stream:
        print(s.decode('utf8'), end='')

def start_container_stream(container, timeout):
    # Process will call container_stream(container) when started
    p = multiprocessing.Process(target=lambda: container_stream(container))
    p.start()
    # Wait until container times out or finished executing
    p.join(timeout)
    # If container is still running, terminate it
    if p.is_alive():
        p.terminate()
        p.join()

def run_file(filename, args=None, data=None, timeout=10, debug=False):
    if args is None:
        args = []
    if data is None:
        data = []
    image = None
    container = None
    d = None
    try:
        d = tempfile.mkdtemp(dir=os.path.abspath('.'))
        for f in data:
            shutil.copy(os.path.abspath(f), d)
        image = build_image(d, 'python:3.7-alpine', filename, args, debug)
        container = run_container(d, image)
        start_container_stream(container, timeout)
    finally:
        teardown(image, container)
        return d

