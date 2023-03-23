import subprocess
from time import sleep, time
from testing_core.base_classes.test_base import TestBase


class Camera(TestBase):
    test_name = 'camera'

    def __init__(self, data_collector, test_results_writer, path_adb, path_results, path_apk, path_pc_data,
                 path_phone_data):
        super(Camera, self).__init__(data_collector, test_results_writer, path_adb, path_results, path_apk,
                                     path_pc_data,
                                     path_phone_data)

        # pm list packages | grep <.....text...>
        self.package_name = 'net.sourceforge.opencamera'
        self.game_activity = 'net.sourceforge.opencamera.MainActivity'

    def camera_video_test_script(self, test_time_sec: float):
        start_time = time()

        start_app = f'{self.adb} shell am start -a android.intent.action.MAIN -n ' \
                    f'{self.package_name}/{self.game_activity}'.split(' ')
        _ = subprocess.check_output(start_app)
        sleep(4)

        # switch to camera
        # _ = subprocess.check_output(f'{self.adb} shell input swipe {int(self.y_max / 1.044)} {int(self.x_max / 1.45)}'
        #                             f' {int(self.y_max / 1.044)} {int(self.x_max / 1.45)} 200')
        # sleep(2)

        video_start_stop = f'{self.adb} shell input swipe {int(self.y_max / 1.044)} {int(self.x_max / 2)}' \
                           f' {int(self.y_max / 1.044)} {int(self.x_max / 2)} 200'.split(' ')

        _ = subprocess.check_output(video_start_stop)

        while time() - start_time < test_time_sec:
            sleep(start_time + test_time_sec - time())

        _ = subprocess.check_output(video_start_stop)

        sleep(2)

        self.close_recent_app()

        # delete videos
        _ = subprocess.check_output(
            f'{self.adb} shell rm -rf /sdcard/DCIM/OpenCamera/*.mp4'.split(' '))

        self._kill_app()

    def certain_virtual_test(self, time_sec):
        self.camera_video_test_script(time_sec)


if __name__ == "__main__":
    from testing_core.base_classes.default_data_collector import DefaultDataCollector
    from testing_core.base_classes.default_results_writer import DefaultResultsWriter

    collector = DefaultDataCollector("D:\\diploma\\console_tools\\adb-tools\\adb")
    writer = DefaultResultsWriter("D:\\diploma\\tests_results")

    flappy_bird_tester = Camera(collector, writer,
                                "D:\\diploma\\console_tools\\adb-tools",
                                "D:\\diploma\\tests_results",
                                "D:\\diploma\\projects_scripts\\freq_gov_test\\apk",
                                "D:\\diploma\\projects_scripts\\freq_gov_test\\phoneFiles",
                                "/sdcard/Download/phoneFiles")

    # stats = flappy_bird_tester.collect_freq_data()
    flappy_bird_tester.exec_test(10)
    flappy_bird_tester.write_results_on_disk('')
