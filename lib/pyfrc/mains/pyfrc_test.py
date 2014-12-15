
import os
import sys
import inspect

from os.path import abspath, dirname, exists, join

import pytest

from pyfrc.support import pyfrc_hal_hooks, fake_time

from hal_impl import data, functions

# TODO: setting the plugins so that the end user can invoke py.test directly
# could be a useful thing. Will have to consider that later.

class PyFrcPlugin(object):

    def __init__(self, robot_class, file_location):
        self.robot_class = robot_class
        self.file_location = file_location

    
    def pytest_runtest_setup(self):
        print('PYTEST_RUNTEST_SETUP')
        #reset the haldata
        data.reset_hal_data(self.hooks)
        
    
    #
    # Fixtures
    #
    # Each one of these can be arguments to your test, and the result of the
    # corresponding function will be passed to your test as that argument.
    #
    
    @pytest.fixture()
    def control(self):
        print('CONTROL')
        pass
    
    @pytest.fixture()
    def fake_time(self):
        print('FAKE_TIME')
        pass
    
    @pytest.fixture()
    def robot_class(self):
        return self.robot_class
    
    @pytest.fixture()
    def robot_path(self):
        return file_location
    
    @pytest.fixture()
    def wpilib_map(self):
        global hal_data
        return hal_data

#
# main test class
#
class PyFrcTest(object):
    
    def __init__(self, parser):
        parser.add_argument('--ignore_mising_test', default=False, 
                            action = 'store_true', 
                            help= 'ignore failure if tests are missing')
    
    def run(self, options, robot_class):
    
        # find test directory, change current directory so py.test can find the tests
        # -> assume that tests reside in tests or ../tests
        
        test_directory = None
        
        root = abspath(os.getcwd())
        
        print('root:' + root)
        try_dirs = [join(root, 'tests'), abspath(join(root, '..', 'tests'))]
        
        for d in try_dirs:
            if exists(d):
                test_directory = d
                break
            
        ignore_missing_test = options.ignore_mising_test
        
        if test_directory is None:
            print("Cannot run robot tests, as test directory was not found. Looked for tests at:")
            for d in try_dirs:
                print('- %s' % d)
            return 0 if ignore_missing_test else 1
        
        os.chdir(test_directory)
        file_location = abspath(inspect.getfile(robot_class))
        
        self.hooks = pyfrc_hal_hooks.PyFrcSimHooks(fake_time.FakeTime())
        
        data.reset_hal_data(self.hooks)
        
        return pytest.main(sys.argv[2:], plugins=[PyFrcPlugin(robot_class, file_location)])
