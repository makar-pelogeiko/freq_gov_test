from testing_core.main_logic import MainLogic
from testing_core.freq_gov_changer import FreqGovChanger
from testing_core.plot_manager import PlotManager
import os
from time import sleep


class TestGovsManager:
    def __init__(self, freq_governors, make_plot, freq_govs_tuners, freq_govs_tuners_metkas,
                 test_cool_time, gov_cool_time,
                 path_adb, path_results,
                 standard_test_args, tests_init_args,
                 tests_func_args, tests_func_times,
                 use_default_test_data_collector, custom_data_collector_class_name, data_collector_args,
                 use_default_test_results_writer, custom_test_results_writer_class_name, test_results_writer_args,
                 run_all_tests, tests_run_queue,
                 need_anti_hotplug, need_push_data_folder, need_install_apks,
                 use_all_test_names, test_names, freq_governors_plot,
                 power_consts, clusters, path_plotter_results,
                 path_plot_img_results, show_plot, save_img
                 ):

        self.freq_governors = freq_governors
        self.make_plot = make_plot
        self.freq_govs_tuners = freq_govs_tuners
        self.freq_govs_tuners_metkas = freq_govs_tuners_metkas

        self.test_cool_time = test_cool_time
        self.gov_cool_time = gov_cool_time

        # For main logic ------------------------------------------------
        self.path_adb = path_adb
        self.adb = os.path.join(self.path_adb, 'adb')
        self.path_results = path_results

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

        # For plotter ------------------------------------------------
        self.use_all_test_names = use_all_test_names
        self.test_names = test_names
        self.freq_governors_plot = freq_governors_plot
        self.power_consts = power_consts
        self.clusters = clusters
        self.path_plotter_results = path_plotter_results
        self.path_plot_img_results = path_plot_img_results
        self.show_plot = show_plot
        self.save_img = save_img
        ###############

    def exec_all_actions(self):

        set_number = -1
        changer = FreqGovChanger(self.path_adb)
        executed_labels = {}

        # get number of sets & prepare labels struct
        goves_num = len(self.freq_governors)
        for gov in self.freq_governors:

            executed_labels[gov] = []
            if gov in self.freq_govs_tuners.keys():
                goves_num += len(self.freq_govs_tuners[gov]) - 1

        for freq_gov in self.freq_governors:

            if freq_gov not in self.freq_govs_tuners.keys():
                self.freq_govs_tuners[freq_gov] = [{}]

            for tun_id, tuners in enumerate(self.freq_govs_tuners[freq_gov]):
                set_number += 1
                print(f'------ test set for governor ------')
                print(f'freq_gov: {freq_gov}, part: {set_number + 1}/{goves_num}')
                print(f'-----------------------------------')

                changer.change_governor(freq_gov)
                changer.set_tuners(tuners, freq_gov)

                print(f'sleep after governor switched for {self.gov_cool_time} sec ...')
                sleep(self.gov_cool_time)

                label = ''
                if len(tuners.keys()) != 0:
                    label = tuners['name']

                if freq_gov in self.freq_govs_tuners_metkas.keys():
                    label += self.freq_govs_tuners_metkas[freq_gov]

                executed_labels[freq_gov].append(label)

                logic = MainLogic(self.path_adb, self.path_results, label, self.test_cool_time,
                                  self.standard_test_args, self.tests_init_args,
                                  self.tests_func_args, self.tests_func_times,
                                  self.use_default_test_data_collector, self.custom_data_collector_class_name,
                                  self.data_collector_args,
                                  self.use_default_test_results_writer, self.custom_test_results_writer_class_name,
                                  self.test_results_writer_args,
                                  self.run_all_tests, self.tests_run_queue,
                                  self.need_anti_hotplug, self.need_push_data_folder, self.need_install_apks
                                  )
                logic.execute_list()

                if set_number == 0:
                    self.need_push_data_folder = False
                    self.need_install_apks = False

        if self.make_plot:
            plotter = PlotManager(self.use_all_test_names, self.test_names, self.freq_governors_plot,
                                  executed_labels,
                                  self.power_consts, self.clusters, self.path_plotter_results,
                                  self.path_plot_img_results, self.show_plot, self.save_img)
            plotter.make_plots()
