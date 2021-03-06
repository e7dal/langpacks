#!/usr/bin/env python3
from jinja2 import Template
import argparse
from os import path
from os.path import isfile
DIR_PATH_TO_TEMPATES = "languages"
DIR_PATH_TO_PACKAGES = "libraries"
RUNNER_NAME = "Dockerfile.runner.j2"
LANGSERVER_VERSION = "ce3f89098fddfaf4db8639a97ce3c0317abbd971"
LANGSERVER_IMAGE ="algorithmiahq/langserver:{}".format(LANGSERVER_VERSION)
RUNNER_PATH = path.join(DIR_PATH_TO_TEMPATES, RUNNER_NAME)

class Package:
    def __init__(self, package_name, install_script, dockerfile_path):
        self.script = install_script
        if dockerfile_path:
            self.dockerfile = get_dockerfile_as_string(dockerfile_path)
        else:
            raise Exception('dockerfile path not available for package {}'.format(package_name))


def get_dockerfile_as_string(file_path):
    with open(file_path, 'r') as fileobject:
        stringified = fileobject.read()
    output = stringified.split('\n')
    return output

def get_template(template_path):
    with open(template_path, 'r') as fileobject:
        template_string = fileobject.read()
    template = Template(template_string)
    return template

def save_generated_template(template, output_path):
    with open(output_path, 'w') as fileobject:
        fileobject.write(template)
    return output_path

def check_if_exists(filepath):
    if isfile(filepath):
        return filepath
    else:
        return None

def build(base_image, package_dirs, output_file_path):

    raw_template = get_template(RUNNER_PATH)
    packages = []
    for dir in package_dirs:
        dockerfile_path = path.join('', DIR_PATH_TO_PACKAGES, dir, "Dockerfile")
        installer_path = path.join('', DIR_PATH_TO_PACKAGES, dir, "install.sh")
        dockerfile_path = check_if_exists(dockerfile_path)
        installer_path = check_if_exists(installer_path)

        package = Package(dir, installer_path, dockerfile_path)
        packages.append(package)
    generated_template = raw_template.render(
        packages=packages,
        base_image=base_image,
        langpacks_version='',
        langserver_image=LANGSERVER_IMAGE)
    save_generated_template(generated_template, output_file_path)

    print("completed template construction, file available at {}".format(output_file_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates a packageset dockerfile, by combining package templates together.\n'
                                                 'Make sure to run this from the root directory.\n'
                                                 'Warning!! Order matters. Load your language packages first before frameworks.')
    parser.add_argument('-b', '--base-image', dest='base_image', type=str, required=True)
    parser.add_argument('-o', '--output-filename', dest='output_path', required=True)
    parser.add_argument('-p', '--package', action='append',  dest='packages', required=True)
    args = parser.parse_args()
    build(args.base_image, args.packages, args.output_path)
