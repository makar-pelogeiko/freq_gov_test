import subprocess
from time import sleep, time
from testing_core.base_classes.test_base import TestBase


class FlappyBirdTest(TestBase):
    test_name = 'flappyBird'

    def __init__(self, data_collector, test_results_writer, path_adb, path_results, path_apk, path_pc_data,
                 path_phone_data):
        super(FlappyBirdTest, self).__init__(data_collector, test_results_writer, path_adb, path_results, path_apk,
                                             path_pc_data,
                                             path_phone_data)

        # pm list packages | grep bird
        self.package_name = 'com.dotgears.flappybird'

    def video_test_script(self, test_time_sec: float):
        start_time = time()

        start_game = f'"{self.adb}" shell am start -a android.intent.action.MAIN -n {self.package_name}/com.dotgears.flappy.SplashScreen'
        _ = subprocess.check_output(start_game)
        sleep(6)

        game_contol = f'"{self.adb}" shell input tap {int(self.x_max / 3.6)} {int(self.y_max / 1.36)}'

        while time() - start_time < test_time_sec:
            _ = subprocess.check_output(game_contol)

        print('end of game time')
        self.close_recent_app()

    def certain_virtual_test(self, time_sec):
        self.video_test_script(time_sec)


if __name__ == "__main__":
    from testing_core.base_classes.default_data_collector import DefaultDataCollector
    from testing_core.base_classes.default_results_writer import DefaultResultsWriter

    collector = DefaultDataCollector("D:\\diploma\\console_tools\\adb-tools\\adb")
    writer = DefaultResultsWriter("D:\\diploma\\tests_results")

    flappy_bird_tester = FlappyBirdTest(collector, writer,
                                        "D:\\diploma\\console_tools\\adb-tools",
                                        "D:\\diploma\\tests_results",
                                        "D:\\diploma\\freq_gov_test\\apk",
                                        "D:\\diploma\\freq_gov_test\\phoneFiles",
                                        "/sdcard/Download/phoneFiles")

    # stats = flappy_bird_tester.collect_freq_data()
    flappy_bird_tester.exec_test()
    flappy_bird_tester.write_results_on_disk()
