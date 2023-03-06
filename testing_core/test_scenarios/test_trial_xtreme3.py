import subprocess
from time import sleep, time
from testing_core.base_classes.test_base import TestBase


class TrialXTreme3(TestBase):
    test_name = 'trialXTreme3'

    def __init__(self, data_collector, test_results_writer, path_adb, path_results, path_apk, path_pc_data,
                 path_phone_data):
        super(TrialXTreme3, self).__init__(data_collector, test_results_writer, path_adb, path_results, path_apk,
                                           path_pc_data,
                                           path_phone_data)

        # pm list packages | grep <.....text...>
        self.package_name = 'com.x3m.tx3'
        self.game_activity = 'com.prime31.UnityPlayerProxyActivity'

    def trialxtreme_test_script(self, test_time_sec: float):
        start_time = time()

        start_game = f'"{self.adb}" shell am start -a android.intent.action.MAIN -n ' \
                     f'{self.package_name}/{self.game_activity}'
        _ = subprocess.check_output(start_game)
        sleep(16)

        _ = subprocess.check_output(f'"{self.adb}" shell input tap {int(self.y_max / 1.1)} {int(self.x_max / 1.2)}')
        _ = subprocess.check_output(f'"{self.adb}" shell input tap {int(self.y_max / 3.5)} {int(self.x_max / 3.7)}')

        _ = subprocess.check_output(f'"{self.adb}" shell input tap {int(self.y_max / 1.1)} {int(self.x_max / 1.1)}')
        _ = subprocess.check_output(f'"{self.adb}" shell input tap {int(self.y_max / 3.5)} {int(self.x_max / 3.7)}')

        sleep(2.6)
        _ = subprocess.check_output(f'"{self.adb}" shell input tap {int(self.y_max / 1.1)} {int(self.x_max / 1.1)}')

        main_contol = f'"{self.adb}" shell input '

        game_controles = [f'swipe {int(self.y_max / 1.1)} {int(self.x_max / 1.2)}'
                          f' {int(self.y_max / 1.1)} {int(self.x_max / 1.2)} 500',

                          f'swipe {int(self.y_max / 1.5)} {int(self.x_max / 1.2)}'
                          f' {int(self.y_max / 1.5)} {int(self.x_max / 1.2)} 500']

        while time() - start_time < test_time_sec:
            for control in game_controles:
                _ = subprocess.check_output(main_contol + control)

        print('end of game time')
        sleep(1)

        self.close_recent_app()

    def certain_virtual_test(self, time_sec):
        self.trialxtreme_test_script(time_sec)


if __name__ == "__main__":
    from testing_core.base_classes.default_data_collector import DefaultDataCollector
    from testing_core.base_classes.default_results_writer import DefaultResultsWriter

    collector = DefaultDataCollector("D:\\diploma\\console_tools\\adb-tools\\adb")
    writer = DefaultResultsWriter("D:\\diploma\\tests_results")

    flappy_bird_tester = TrialXTreme3(collector, writer,
                                      "D:\\diploma\\console_tools\\adb-tools",
                                      "D:\\diploma\\tests_results",
                                      "D:\\diploma\\projects_scripts\\freq_gov_test\\apk",
                                      "D:\\diploma\\projects_scripts\\freq_gov_test\\phoneFiles",
                                      "/sdcard/Download/phoneFiles")

    # stats = flappy_bird_tester.collect_freq_data()
    flappy_bird_tester.exec_test(30)
    flappy_bird_tester.write_results_on_disk()
