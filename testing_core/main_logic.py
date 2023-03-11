import subprocess
import os
from testing_core.modules_loader import ModulesLoader
from testing_core.phone_prepare import Preparer
from testing_core.base_classes.default_data_collector import DefaultDataCollector
from testing_core.base_classes.default_results_writer import DefaultResultsWriter
from typing import Tuple
from time import time, sleep


class MainLogic:
    def __init__(self, path_adb, path_results, metka,
                 standard_test_args, tests_init_args,
                 tests_func_args, tests_func_times,
                 use_default_test_data_collector, custom_data_collector_class_name, data_collector_args,
                 use_default_test_results_writer, custom_test_results_writer_class_name, test_results_writer_args,
                 run_all_tests, tests_run_queue,
                 need_anti_hotplug, need_push_data_folder, need_install_apks
                 ):

        self.path_adb = path_adb
        self.path_results = path_results

        self.metka = metka

        self.standard_test_args = standard_test_args
        self.tests_init_args = tests_init_args

        self.tests_func_args = tests_func_args
        self.tests_func_times = tests_func_times

        self.use_default_test_data_collector = use_default_test_data_collector
        self.custom_data_collector_class_name = custom_data_collector_class_name
        self.data_collector_args = data_collector_args

        self.use_default_test_results_writer = use_default_test_results_writer
        self.custom_test_results_writer_class_name = custom_test_results_writer_class_name
        self.test_results_writer_args = test_results_writer_args

        self.run_all_tests = run_all_tests
        self.tests_run_queue = tests_run_queue

        self.need_anti_hotplug = need_anti_hotplug
        self.need_push_data_folder = need_push_data_folder
        self.need_install_apks = need_install_apks

        #############################
        self.loader = ModulesLoader()
        self.preparer = Preparer(*self.standard_test_args)

        self.adb = os.path.join(self.path_adb, 'adb')
        self.check_adb_connection(self.adb)

    @staticmethod
    def check_adb_connection(adb_path):
        root_cmd = f'{adb_path} root'.split(' ')
        shell_exit_cmd = f'{adb_path} shell exit'.split(' ')

        try:
            _ = subprocess.check_output(root_cmd)

            _ = subprocess.check_output(shell_exit_cmd)

        except subprocess.CalledProcessError as e:
            print("Can not connect Via adb to device\n"
                  f"command: <{e.cmd}> did not executed successfully")
            raise Exception(f"Can not connect Via adb to device, did not execute <{e.cmd}>")

    def get_data_collector(self):
        if self.use_default_test_data_collector:
            return DefaultDataCollector(self.adb)

        else:
            self.loader.load_data_collector()
            collector = self.loader.get_data_collector(self.custom_data_collector_class_name)

            return collector(*self.data_collector_args)

    def get_writer(self, ):
        if self.use_default_test_results_writer:
            return DefaultResultsWriter(self.path_results)

        else:
            self.loader.load_writer()
            writer = self.loader.get_writer(self.custom_test_results_writer_class_name)
            return writer(*self.test_results_writer_args)

    def get_required_test_list(self) -> list:
        self.loader.load_tests()
        all_tests = self.loader.get_tests_dict()

        test_list = []
        if self.run_all_tests and len(self.tests_run_queue) != 0:
            print("WARNING test_run_queue have to be empty or run_all_test have to be False\n"
                  "using test from test_run_queue")

        for name in self.tests_run_queue:
            if name in all_tests.keys():
                test_list.append((name, all_tests[name]))
            else:
                print(f"ERROR CONFIG: No <{name}> was found")

        if len(test_list) == 0 and self.run_all_tests:
            test_list = [(key, value) for key, value in all_tests.items()]

        return test_list

    def get_args_for_tests(self, test_list: list[Tuple]) -> dict:

        args_dict = {}
        for name, _ in test_list:
            args_lst = [self.get_data_collector(), self.get_writer()]
            if name in self.tests_init_args.keys():

                if self.tests_init_args[name]['use_standard_args']:
                    args_lst = args_lst + self.standard_test_args.copy()

                args_lst = args_lst + self.tests_init_args[name]['custom_args']

            else:
                args_lst = args_lst + self.standard_test_args.copy()

            args_dict[name] = args_lst

        return args_dict

    def get_pre_test_list(self) -> list:
        prepare_exec_lst = []

        if self.need_anti_hotplug:
            prepare_exec_lst.append(self.preparer.anti_hotplug)

        if self.need_push_data_folder:
            prepare_exec_lst.append(self.preparer.push_required_files)

        if self.need_install_apks:
            prepare_exec_lst.append(self.preparer.install_all_apks)

        prepare_exec_lst.append(self.preparer.set_all_cpu_online)

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
            if name in self.tests_func_args.keys():
                args = self.tests_func_args[name]

            if name in self.tests_func_times.keys():
                for i in range(0, self.tests_func_times[name]):
                    print(f"{name}, attempt: {i + 1}/{self.tests_func_times[name]} | args {args}")

                    start_t = time()
                    test_obj.exec_test(*args)
                    print(f'test time: {time() - start_t} sec')
                    sleep(2)
            else:
                print(f"{name}, one time | args {args}")

                start_t = time()
                test_obj.exec_test(*args)
                print(f'test time: {time() - start_t}  sec')
                sleep(2)
            test_obj.write_results_on_disk(self.metka)
