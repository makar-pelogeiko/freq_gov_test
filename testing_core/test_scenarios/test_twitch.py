import os
import subprocess
from time import sleep, time
from testing_core.base_classes.test_base import TestBase


class Twitch(TestBase):
    test_name = 'twitch'

    def __init__(self, data_collector, test_results_writer, path_adb, path_results, path_apk, path_pc_data,
                 path_phone_data):
        super(Twitch, self).__init__(data_collector, test_results_writer, path_adb, path_results, path_apk,
                                     path_pc_data,
                                     path_phone_data)

        # self.test_name = 'videoVLC'
        self.package_name = "org.mozilla.firefox"
        self.game_activity = 'org.mozilla.firefox.App'
        self.twitch_link = 'https://m.twitch.tv/streamerhouse'

        print("wifi connecting ...", end='')
        _ = subprocess.check_output(f'{self.adb} shell input keyevent KEYCODE_HOME'.split(' '))
        # connect to wifi
        _ = subprocess.check_output(f'{self.adb} shell svc wifi enable'.split(' '))
        sleep(7)
        print('DONE')

    def twitch_test_script(self, test_time_sec: float):
        start_time = time()

        # adb shell am start -a android.intent.action.VIEW -n
        # com.android.browser/.BrowserActivity http://www.google.co.uk

        start_app = f'{self.adb} shell am start -a android.intent.action.VIEW  -n ' \
                    f'{self.package_name}/{self.game_activity}'.split(' ')
        _ = subprocess.check_output(start_app)
        sleep(4)

        # open address bar
        _ = subprocess.check_output(f'{self.adb} shell input tap '
                                    f'{int(self.x_max / 2)} {int(self.y_max / 1.04)}'.split(' '))

        sleep(2.2)
        # input link
        _ = subprocess.check_output(f'{self.adb} shell input text "{self.twitch_link}"'.split(' '))
        sleep(3)

        # hit ENTER
        _ = subprocess.check_output(f'{self.adb} shell input keyevent 66'.split(' '))

        while time() - start_time < test_time_sec:
            sleep(start_time + test_time_sec - time())

        self.close_recent_app()
        self._kill_app()

    def certain_virtual_test(self, time_sec):
        self.twitch_test_script(time_sec)

    def write_results_on_disk(self, metka):
        _ = subprocess.check_output(f'{self.adb} shell svc wifi disable'.split(' '))
        TestBase.write_results_on_disk(self, metka)


if __name__ == "__main__":
    from testing_core.base_classes.default_data_collector import DefaultDataCollector
    from testing_core.base_classes.default_results_writer import DefaultResultsWriter

    collector = DefaultDataCollector("D:\\diploma\\console_tools\\adb-tools\\adb")
    writer = DefaultResultsWriter("D:\\diploma\\tests_results")

    vlc_tester = Twitch(collector, writer,
                        "D:\\diploma\\console_tools\\adb-tools",
                        "D:\\diploma\\tests_results",
                        "D:\\diploma\\projects_scripts\\freq_gov_test\\apk",
                        "D:\\diploma\\projects_scripts\\freq_gov_test\\phoneFiles",
                        "/sdcard/Download/phoneFiles")

    # stats = vlc_tester.collect_freq_data()
    vlc_tester.exec_test(30)
    vlc_tester.write_results_on_disk('')
