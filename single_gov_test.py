from testing_core.main_logic import MainLogic
import config

if __name__ == '__main__':

    logic = MainLogic(config.path_adb, config.path_results, '', config.test_cool_time,
                      config.standard_test_args, config.tests_init_args,
                      config.tests_func_args, config.tests_func_repeat_num,
                      config.use_default_test_data_collector, config.custom_data_collector_class_name,
                      config.data_collector_args,
                      config.use_default_test_results_writer, config.custom_test_results_writer_class_name,
                      config.test_results_writer_args,
                      config.run_all_tests, config.tests_run_queue,
                      config.need_anti_hotplug, config.need_push_data_folder, config.need_install_apks
                      )
    logic.execute_list()
