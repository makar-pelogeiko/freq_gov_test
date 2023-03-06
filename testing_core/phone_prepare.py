import os
import subprocess


class Preparer:
    def __init__(self, path_adb, path_results, path_apk, path_pc_data, path_phone_data):
        self.path_adb = path_adb
        self.path_phone_data = path_phone_data
        self.path_results = path_results
        self.path_pc_data = path_pc_data
        self.path_apk = path_apk
        self.adb = os.path.join(self.path_adb, 'adb')

    def anti_hotplug(self):
        print("anti hotplug")
        _ = subprocess.check_output(f'"{self.adb}" shell echo 8 > /sys/devices/system/cpu/cpuhotplug/max_online_cpu')
        _ = subprocess.check_output(f'"{self.adb}" shell echo 8 > /sys/devices/system/cpu/cpuhotplug/min_online_cpu')
        _ = subprocess.check_output(f'"{self.adb}" shell echo 1 >  /sys/devices/system/cpu/cpu6/online')
        _ = subprocess.check_output(f'"{self.adb}" shell echo 1 >  /sys/devices/system/cpu/cpu7/online')


    def push_required_files(self):
        print("push files")
        _ = subprocess.check_output(f'"{self.adb}" root')

        # to make sure that we can push files into sdcard
        _ = (subprocess.Popen(f'"{self.adb}" shell chmod 777 /mnt/sdcard',
                              stdout=subprocess.PIPE, shell=True)).communicate()

        # push folder from pc to phone
        _ = subprocess.check_output(f'"{self.adb}" push "{self.path_pc_data}" "{self.path_phone_data}"')

        out = subprocess.check_output(f'"{self.adb}" shell "ls {self.path_phone_data}"').decode('utf-8')[:-2].split('\r\n')
        print(f"---files on phone---")
        print(f"phone path: {self.path_phone_data}")
        for file in out:
            print(file)
        print(f"--------------------------------")

    def install_all_apks(self):

        apks = os.listdir(self.path_apk)
        apks = list(filter(lambda item: item[-4:] == '.apk', apks))

        for apk in apks:
            curr_apk_path = os.path.join(self.path_apk, apk)

            print(f'installing <{apk}>')
            _ = subprocess.check_output(f'"{self.adb}" install "{curr_apk_path}"')

        print(f'all apks installed')


if __name__ == "__main__":
    preparer = Preparer("D:\\diploma\\console_tools\\adb-tools",
                        "D:\\diploma\\tests_results",
                        "D:\\diploma\\projects_scripts\\freq_gov_test\\apk",
                        "D:\\diploma\\projects_scripts\\freq_gov_test\\phoneFiles",
                        "/sdcard/Download/phoneFiles")

    # preparer.push_required_files()
    preparer.install_all_apks()
