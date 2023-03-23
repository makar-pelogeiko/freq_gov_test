import os
import subprocess
from time import sleep, time
import csv
import json


class TestBase:
    test_name = 'base_test_name'

    def __init__(self, data_collector, test_results_writer, path_adb, path_results, path_apk, path_pc_data,
                 path_phone_data):
        self.path_adb = path_adb
        self.adb = os.path.join(self.path_adb, 'adb')
        self.path_phone_data = path_phone_data
        self.path_results = path_results
        self.path_pc_data = path_pc_data
        self.path_apk = path_apk

        self.results = []
        self.stats_of_tests = []

        # Get screen size
        out = subprocess.check_output(f'{self.adb} shell wm size'.split(' '))
        self.x_max, self.y_max = out.decode('utf-8').strip().split(' ')[2].split('x')
        self.x_max = int(self.x_max)
        self.y_max = int(self.y_max)

        self.data_collector = data_collector

        self.test_results_writer = test_results_writer

        # Governor name
        self.freq_gov_name = 'no_info_gov'

        # Package name
        self.package_name = ''

    def _kill_app(self):
        if self.package_name:
            print(f'kill package {self.package_name}')
            sleep(0.3)
            _ = subprocess.check_output(f'{self.adb} shell am kill {self.package_name}'.split(' '))
            sleep(0.2)
            _ = subprocess.check_output(f'{self.adb} shell pm disable {self.package_name}'.split(' '))
            _ = subprocess.check_output(f'{self.adb} shell pm enable {self.package_name}'.split(' '))

    def lock_phone(self):
        _ = subprocess.check_output(f'{self.adb} shell dumpsys battery reset'.split(' '))
        _ = subprocess.check_output(f'{self.adb} shell input keyevent KEYCODE_POWER'.split(' '))

    def unlock_phone(self):
        _ = subprocess.check_output(f'{self.adb} shell dumpsys battery unplug'.split(' '))
        _ = subprocess.check_output(
            f'{self.adb} shell input keyevent KEYCODE_HOME && input swipe {self.x_max / 2} {3 * self.y_max / 4}'
            f' {self.x_max / 2} {self.y_max / 4} 500'.split(' '))

        self.close_recent_app()

    def close_recent_app(self, need_to_force_out_switch_screen=True):
        """ phone have to be with unlocked screen"""

        _ = subprocess.check_output(
            f'{self.adb} shell input keyevent KEYCODE_HOME'.split(' '))

        sleep(0.2)
        os.system(f'{self.adb} shell input keyevent KEYCODE_APP_SWITCH')
        sleep(0.2)
        os.system(f'{self.adb} shell input swipe {self.x_max / 2} {int(0.5 * self.y_max)}'
                  f' {self.x_max / 2} {self.y_max / 4} 300')
        sleep(0.2)

        # if smartphone does not close switch screen automatically
        if need_to_force_out_switch_screen:
            os.system(f'{self.adb} shell input keyevent KEYCODE_BACK')

    def certain_virtual_test(self, time_sec):
        print("No test scenario")

    def exec_test(self, time_sec=3):
        # os.chdir(self.path_adb)

        # Get freq governor name
        out = subprocess.check_output(f'{self.adb} shell cat '
                                      f'/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor'.split(' '))
        self.freq_gov_name = out.decode('utf-8').strip()
        self.unlock_phone()

        print(f'Collect data before test...')
        before_time = time()
        stats_freq_before = self.data_collector.collect_data()

        print(f'start test')
        self.certain_virtual_test(time_sec)

        print(f'Collect data after test...')
        stats_freq_after = self.data_collector.collect_data()
        after_time = time()

        diff = self.data_collector.make_diff_data(stats_freq_before, stats_freq_after)

        stat_test = {'test_time(sec)': after_time - before_time}
        self.stats_of_tests.append(stat_test)

        result = {'diff': diff, 'before': stats_freq_before, 'after': stats_freq_after}
        self.results.append(result)

        self.lock_phone()

    def get_results(self):
        return self.results

    def write_results_on_disk(self, metka):
        self.test_results_writer.write_results(self.test_name, self.freq_gov_name, metka,
                                               self.stats_of_tests, self.results)


if __name__ == "__main__":
    from default_data_collector import DefaultDataCollector
    from default_results_writer import DefaultResultsWriter

    # from data_collectors.freq_only_collector import FreqOnlyCollector
    # from test_result_writers.feq_only_writer import FreqOnlyWriter

    collector = DefaultDataCollector("D:\\diploma\\console_tools\\adb-tools\\adb")
    writer = DefaultResultsWriter("D:\\diploma\\tests_results")

    base_test = TestBase(collector, writer,
                         "D:\\diploma\\console_tools\\adb-tools",
                         "D:\\diploma\\tests_results",
                         "D:\\diploma\\projects_scripts\\freq_gov_test\\apk",
                         "D:\\diploma\\projects_scripts\\freq_gov_test\\phoneFiles",
                         "/sdcard/Download/phoneFiles")

    base_test.exec_test()
    base_test.write_results_on_disk('')
