from testing_core.test_diff_govs_manager import TestDiffGovsManager
import config

if __name__ == "__main__":
    all_test_sets_runner = TestDiffGovsManager(config.freq_governors, config.make_plot,
                 config.path_adb, config.path_results,
                 config.standard_test_args, config.tests_init_args,
                 config.tests_func_args, config.tests_func_times,
                 config.use_default_test_data_collector, config.custom_data_collector_class_name, config.data_collector_args,
                 config.use_default_test_results_writer, config.custom_test_results_writer_class_name, config.test_results_writer_args,
                 config.run_all_tests, config.tests_run_queue,
                 config.need_anti_hotplug, config.need_push_data_folder, config.need_install_apks,
                 config.use_all_test_names, config.test_names, config.freq_governors_plot,
                 config.power_consts, config.clusters, config.path_plotter_results,
                 config.path_plot_img_results, config.show_plot, config.save_img
                 )

    all_test_sets_runner.exec_all_actions()