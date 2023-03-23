import os
from testing_core.base_classes.test_base import TestBase
from testing_core.base_classes.default_results_writer import DefaultResultsWriter
from testing_core.base_classes.default_data_collector import DefaultDataCollector
import sys
import inspect


class ModulesLoader:
    def __init__(self):
        self.path_tests = 'test_scenarios'
        self.path_writers = 'test_result_writers'
        self.path_collectors = 'data_collectors'

        self.tests_dict = dict()
        self.writers_dict = dict()
        self.collectors_dict = dict()

        self.data_collector_type = None

        self.tests_results_writer_type = None

        self.module_path_current = '.'.join(__name__.split('.')[:-1])
        self.path_to_loader = os.path.realpath(os.path.dirname(__file__))

        # for import modules
        sys.path.append(self.path_to_loader)

    def get_tests_dict(self):
        return self.tests_dict

    def load_tests(self):
        self.load_all_modules_path('tests', self.tests_dict, self.path_tests, TestBase, test_name_flag=True)

    def load_all_modules_path(self, tag, dict_result, path_module, base_class, test_name_flag=False):
        print(f'-- start {tag} scan --')

        full_path_module = os.path.join(self.path_to_loader, path_module)

        module_dir_ls = os.listdir(full_path_module)
        modules = list(map(lambda item: item[:-3], filter(lambda item: item[-3:] == '.py', module_dir_ls)))

        for module in modules:

            mod = __import__(f'{path_module}.{module}')
            required_mod = getattr(mod, module)

            for name, obj in inspect.getmembers(required_mod):
                if inspect.isclass(obj):
                    if obj.__bases__[0] == base_class:

                        if test_name_flag:
                            print(f'Test found -- class name: {name}, test_name: {obj.test_name}')
                            self.tests_dict[obj.test_name] = obj
                        else:
                            print(f'{tag}r found -- class name: {name}')
                            dict_result[name] = obj

        print('')

    def load_writer(self):
        self.load_all_modules_path('writer', self.writers_dict, self.path_writers, DefaultResultsWriter)

    def load_data_collector(self):
        self.load_all_modules_path('collector', self.collectors_dict, self.path_collectors, DefaultDataCollector)

    def get_class_from_dict(self, source_dict, tag, class_name):
        if class_name == '':
            return source_dict

        else:
            if class_name in source_dict.keys():
                return source_dict[class_name]

            else:
                print(f'No {tag} class with name: <{class_name}>\n'
                      f'there are only these classes: <{self.writers_dict.keys()}>')
                raise Exception(f"No class <{class_name}>")

    def get_writer(self, class_name=''):
        return self.get_class_from_dict(self.writers_dict, 'writer', class_name)

    def get_data_collector(self, class_name=''):
        return self.get_class_from_dict(self.collectors_dict, 'collector', class_name)


if __name__ == '__main__':
    loader = ModulesLoader()
    loader.load_tests()
