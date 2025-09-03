import subprocess
from os import listdir
from os.path import isfile, isdir, join
from shutil import rmtree
from getpass import getpass


def files_in_dir(dir):
    return [join(dir, f) for f in listdir(dir) if isfile(join(dir, f))]


def dirs_in_dir(dir):
    return [join(dir, f) for f in listdir(dir) if isdir(join(dir, f))]


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-dir', default='.')
    args = parser.parse_args()

    if 'egg-info' in ' '.join(dirs_in_dir(args.dir)) or 'dist' in ' '.join(dirs_in_dir(args.dir)):
        print('Cleaning old directories')
        egg_dirs = [x for x in dirs_in_dir(args.dir) if x.endswith('egg-info')]
        for dir in egg_dirs:
            print(f'Deleting: {dir}')
            rmtree(dir)
        if 'dist' in ' '.join(dirs_in_dir(args.dir)):
            print(f'Deleting: {join(args.dir, "dist")}')
            rmtree(join(args.dir, 'dist'))

    print('Building!')
    subprocess.run('python setup.py sdist'.split())
    if input('Deploy to Pypi? [y/N]').lower().startswith('y'):
        key = getpass('Enter Pypi API key: ')
        p = subprocess.run(f'twine upload --username __token__ --password {key} dist/*'.split())
    else:
        print('To deploy run: twine upload dist/*')
