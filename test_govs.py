from testing_core.test_govs_manager import TestGovsManager
import config

if __name__ == "__main__":
    all_test_sets_runner = TestGovsManager(config.freq_governors, config.make_plot, config.freq_govs_tuners,
                                           config.freq_govs_tuners_labels, config.test_cool_time, config.gov_cool_time,
                                           config.need_reboot_before_switch,
                                           config.path_adb, config.path_results,
                                           config.standard_test_args, config.tests_init_args,
                                           config.tests_func_args, config.tests_func_repeat_num,
                                           config.use_default_test_data_collector,
                                           config.custom_data_collector_class_name, config.data_collector_args,
                                           config.use_default_test_results_writer,
                                           config.custom_test_results_writer_class_name,
                                           config.test_results_writer_args,
                                           config.run_all_tests, config.tests_run_queue,
                                           config.need_anti_hotplug, config.need_push_data_folder,
                                           config.need_install_apks,
                                           config.use_all_test_names, config.test_names, config.freq_governors_plot,
                                           config.power_consts, config.clusters, config.path_plotter_results,
                                           config.path_plot_img_results, config.show_plot, config.save_img,
                                           config.z_val, config.need_ci, config.fig_size, config.rotation)

    all_test_sets_runner.exec_all_actions()
