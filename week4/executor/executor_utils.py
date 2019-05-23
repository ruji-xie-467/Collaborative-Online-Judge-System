import uuid
import os
import docker
import shutil
from docker.errors import *


IMAGE_NAME = 'ruji/coj_executor'

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TEMP_BUILD_DIR = "%s/tmp" % CURRENT_DIR
# CONTAINER_NAME = "%s:latest" % IMAGE_NAME

SOURCE_FILE_NAMES = {
    "java": "Solution.java",
    "python": "solution.py",
    "c++": "solution.cpp"
}

BINARY_NAMES = {
    "java": "Solution",
    "python": "solution.py",
    "c++": "./a.out"
}

BUILD_COMMANDS = {
    "java": "javac",
    "python": "python",
    "c++": "g++"
}

EXECUTE_COMMANDS = {
    "java": "java",
    "python": "python",
    "c++": ""
}

client = docker.from_env()

def load_image():
    try:
        client.images.get(IMAGE_NAME)
    except ImageNotFound:
        print "Image not found locally. Loading from Dockerhub..."
        client.images.pull(IMAGE_NAME)
    except APIError:
        print "Image not found locally. DockerHub is not accessible"
        return
    print "Image: [%s] loaded" % IMAGE_NAME

def build_and_run(code, lang):
    result = {'build': None, 'run': None, 'err': None}

    source_file_parent_dir_name = uuid.uuid4()
    source_file_host_dir = "%s/%s" % (TEMP_BUILD_DIR, source_file_parent_dir_name)
    source_file_guest_dir = "/test/%s" % (source_file_parent_dir_name)
    make_dir(source_file_host_dir)
    print(source_file_host_dir)
    with open("%s/%s" % (source_file_host_dir, SOURCE_FILE_NAMES[lang]), 'w') as source_file:
        source_file.write(code)

    try:
        client.containers.run(
            image=IMAGE_NAME,
            command="%s %s" % (BUILD_COMMANDS[lang], SOURCE_FILE_NAMES[lang]),
            #map host to docker vm
            volumes={source_file_host_dir: {'bind': source_file_guest_dir, 'mode': 'rw'}},
            working_dir=source_file_guest_dir)
        print "Source built."
        result['build'] = 'OK'
    except ContainerError as e:
        print ' Build failed.'
        result['err'] = e.stderr
        shutil.rmtree(source_file_host_dir)
        return result

    try:
        log = client.containers.run(
            image=IMAGE_NAME,
            command="%s %s" % (EXECUTE_COMMANDS[lang], BINARY_NAMES[lang]),
            #map host to docker vm
            volumes={source_file_host_dir: {'bind': source_file_guest_dir, 'mode': 'rw'}},
            working_dir=source_file_guest_dir)
        print "Executed."
        result['run'] = log

    except ContainerError as e:
        print "Execution failed."
        result['err'] = e.stderr
        shutil.rmtree(source_file_host_dir)
        return result

    shutil.rmtree(source_file_host_dir)
    return result

def make_dir(dir):
    try:
        os.mkdir(dir)
        print "Temp build directory [%s] created." % dir
    except OSError:
        print "Temp build directory [%s] exists." % dir
