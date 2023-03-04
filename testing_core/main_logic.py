import subprocess
import os
import config
from testing_core.modules_loader import ModulesLoader
from testing_core.phone_prepare import Preparer
from testing_core.base_classes.default_data_collector import DefaultDataCollector
from testing_core.base_classes.default_results_writer import DefaultResultsWriter
from typing import Tuple


class MainLogic:
    def __init__(self):
        self.loader = ModulesLoader()
        self.preparer = Preparer(*config.standard_test_args)

        self.adb = os.path.join(config.path_adb, 'adb')
        self.check_adb_connection()

    def check_adb_connection(self):
        root_cmd = f'"{self.adb}" root'
        shell_exit_cmd = f'"{self.adb}" shell exit'

        try:
            out = subprocess.check_output(root_cmd)

            out = subprocess.check_output(shell_exit_cmd)

        except subprocess.CalledProcessError as e:
            print("Can not connect Via adb to device\n"
                  f"command: <{e.cmd}> did not executed successfully")
            raise Exception(f"Can not connect Via adb to device, did not execute <{e.cmd}>")

    def get_data_collector(self):
        if config.use_default_test_data_collector:
            return DefaultDataCollector(self.adb)

        else:
            self.loader.load_data_collector()
            collector = self.loader.get_data_collector(config.custom_data_collector_class_name)

            return collector(*config.data_collector_args)

    def get_writer(self,):
        if config.use_default_test_results_writer:
            return DefaultResultsWriter(config.path_results)

        else:
            self.loader.load_writer()
            writer = self.loader.get_writer(config.custom_test_results_writer_class_name)
            return writer(*config.test_results_writer_args)

    def get_required_test_list(self) -> list:
        self.loader.load_tests()
        all_tests = self.loader.get_tests_dict()

        test_list = []
        if config.run_all_tests and len(config.tests_run_queue) != 0:
            print("WARNING test_run_queue have to be empty or run_all_test have to be False\n"
                  "using test from test_run_queue")

        for name in config.tests_run_queue:
            if name in all_tests.keys():
                test_list.append((name, all_tests[name]))
            else:
                print(f"ERROR CONFIG: No <{name}> was found")

        if len(test_list) == 0 and config.run_all_tests:
            test_list = [(key, value) for key, value in all_tests.items()]

        return test_list

    def get_args_for_tests(self, test_list: list[Tuple]) -> dict:

        args_dict = {}
        for name, _ in test_list:
            args_lst = [self.get_data_collector(), self.get_writer()]
            if name in config.tests_init_args.keys():

                if config.tests_init_args[name]['use_standard_args']:
                    args_lst = args_lst + config.standard_test_args.copy()

                args_lst = args_lst + config.tests_init_args[name]['custom_args']

            else:
                args_lst = args_lst + config.standard_test_args.copy()

            args_dict[name] = args_lst

        return args_dict

    def get_pre_test_list(self) -> list:
        prepare_exec_lst = []

        if config.need_anti_hotplug:
            prepare_exec_lst.append(self.preparer.anti_hotplug)

        if config.need_push_data_folder:
            prepare_exec_lst.append(self.preparer.push_required_files)

        if config.need_install_apks:
            prepare_exec_lst.append(self.preparer.install_all_apks)

        return prepare_exec_lst

    def execute_list(self):

        # Make all pretest executions
        pre_test_lst = self.get_pre_test_list()
        for pre_test in pre_test_lst:
            pre_test()

        # Get required tests
        test_lst = self.get_required_test_list()
        test_args = self.get_args_for_tests(test_lst)

        print("------ executing tests ------")
        # Execute required tests
        for name, test_type in test_lst:
            test_obj = test_type(*test_args[name])

            args = []
            if name in config.tests_func_args.keys():
                args = config.tests_func_args[name]

            if name in config.tests_func_times.keys():
                for i in range(0, config.tests_func_times[name]):
                    print(f"{name}, attempt: {i+1}/{config.tests_func_times[name]} | args {args}")
                    test_obj.exec_test(*args)
            else:
                print(f"{name}, one time | args {args}")
                test_obj.exec_test(*args)

            test_obj.write_results_on_disk()

