# coding=utf-8
# Created by OhBonsai at 2018/3/13

from subprocess import CalledProcessError, check_output as run

FLAKE8_COMMAND = 'flake8'

FLAKE8_INPUTS = [
    'app',
    'tests'
]


def pytest_generate_tests(metafunc):
    metafunc.parametrize('folder', FLAKE8_INPUTS)


def test_flake8(folder):
    """ Run skylines package through flake8 """
    try:
        run([FLAKE8_COMMAND, folder])
    except CalledProcessError as e:
        print(e.output)
        raise AssertionError('flake8 has found errors.')
    except OSError:
        raise OSError('Failed to run flake8. Please check that you have '
                      'installed it properly.')

