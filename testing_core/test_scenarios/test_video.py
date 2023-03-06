import os
from time import sleep
from testing_core.base_classes.test_base import TestBase


class VideoTestVLC(TestBase):
    test_name = 'videoVLC'

    def __init__(self, data_collector, test_results_writer, path_adb, path_results, path_apk, path_pc_data,
                 path_phone_data):
        super(VideoTestVLC, self).__init__(data_collector, test_results_writer, path_adb, path_results, path_apk,
                                           path_pc_data,
                                           path_phone_data)

        # self.test_name = 'videoVLC'
        self.video = "video.mp4"
        self.package_name = "org.videolan.vlc"

        self.path_phone_video = f'{self.path_phone_data}/{self.video}'

    def video_test_script(self, test_time_sec: float):
        start_video = f'"{self.adb}" shell am start -a android.intent.action.VIEW ' \
                      f'-d file://{self.path_phone_video} -t video/mp4'
        os.system(start_video)
        sleep(1)
        os.system(f'"{self.adb}" shell input tap {self.x_max / 2} {self.y_max / 2}')

        sleep(test_time_sec)
        self.close_recent_app()

    def certain_virtual_test(self, time_sec):
        self.video_test_script(time_sec)


if __name__ == "__main__":
    from testing_core.base_classes.default_data_collector import DefaultDataCollector
    from testing_core.base_classes.default_results_writer import DefaultResultsWriter

    collector = DefaultDataCollector("D:\\diploma\\console_tools\\adb-tools\\adb")
    writer = DefaultResultsWriter("D:\\diploma\\tests_results")

    vlc_tester = VideoTestVLC(collector, writer,
                              "D:\\diploma\\console_tools\\adb-tools",
                              "D:\\diploma\\tests_results",
                              "D:\\diploma\\projects_scripts\\freq_gov_test\\apk",
                              "D:\\diploma\\projects_scripts\\freq_gov_test\\phoneFiles",
                              "/sdcard/Download/phoneFiles")

    # stats = vlc_tester.collect_freq_data()
    vlc_tester.exec_test()
    vlc_tester.write_results_on_disk()
