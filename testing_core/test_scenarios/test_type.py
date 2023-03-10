import subprocess
from time import sleep, time
from testing_core.base_classes.test_base import TestBase


class Typer(TestBase):
    test_name = 'type'

    def __init__(self, data_collector, test_results_writer, path_adb, path_results, path_apk, path_pc_data,
                 path_phone_data):
        super(Typer, self).__init__(data_collector, test_results_writer, path_adb, path_results, path_apk,
                                    path_pc_data,
                                    path_phone_data)

        # pm list packages | grep <.....text...>
        self.package_name = 'com.ogden.memo'
        self.game_activity = 'com.ogden.memo.ui.MemoMain'

    def type_test_script(self, test_time_sec: float):
        start_time = time()

        start_app = f'{self.adb} shell am start -a android.intent.action.MAIN -n ' \
                    f'{self.package_name}/{self.game_activity}'.split(' ')
        _ = subprocess.check_output(start_app)
        sleep(3.2)

        # make new note
        _ = subprocess.check_output(f'{self.adb} shell input tap '
                                    f'{int(self.x_max / 1.0588)} {int(self.y_max / 16)}'.split(' '))

        type_letter = f'{self.adb} shell input swipe {int(self.x_max / 1.5)} {int(self.y_max / 1.28)}' \
                      f' {int(self.x_max / 2)} {int(self.y_max / 1.27)} 100'.split(' ')

        while time() - start_time < test_time_sec:
            _ = subprocess.check_output(type_letter)

        self.close_recent_app()

    def certain_virtual_test(self, time_sec):
        self.type_test_script(time_sec)


if __name__ == "__main__":
    from testing_core.base_classes.default_data_collector import DefaultDataCollector
    from testing_core.base_classes.default_results_writer import DefaultResultsWriter

    collector = DefaultDataCollector("D:\\diploma\\console_tools\\adb-tools\\adb")
    writer = DefaultResultsWriter("D:\\diploma\\tests_results")

    flappy_bird_tester = Typer(collector, writer,
                               "D:\\diploma\\console_tools\\adb-tools",
                               "D:\\diploma\\tests_results",
                               "D:\\diploma\\projects_scripts\\freq_gov_test\\apk",
                               "D:\\diploma\\projects_scripts\\freq_gov_test\\phoneFiles",
                               "/sdcard/Download/phoneFiles")

    # stats = flappy_bird_tester.collect_freq_data()
    flappy_bird_tester.exec_test(30)
    flappy_bird_tester.write_results_on_disk()
