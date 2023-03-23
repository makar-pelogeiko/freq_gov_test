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
        _ = subprocess.check_output(f'{self.adb} shell echo 8 > '
                                    f'/sys/devices/system/cpu/cpuhotplug/max_online_cpu'.split(' '))
        _ = subprocess.check_output(f'{self.adb} shell echo 8 > '
                                    f'/sys/devices/system/cpu/cpuhotplug/min_online_cpu'.split(' '))

        self.set_all_cpu_online()

    def set_all_cpu_online(self):
        out = subprocess.check_output(f'{self.adb} shell cd /sys/devices/system/cpu && ls | grep cpu'.split(' '))
        cores_done = []

        cpus_out = out.decode('utf-8').replace("\r", "").split('\n')
        cpus_amount = len(list(filter(lambda item: item[3:].isnumeric(), cpus_out)))
        for core_n in range(0, cpus_amount):
            cores_done.append(core_n)
            _ = subprocess.check_output(f'{self.adb} shell echo 1 > '
                                        f'/sys/devices/system/cpu/cpu{core_n}/online'.split(' '))
        print(f'set cpus: {cores_done} online\n')

    def push_required_files(self):
        print("push files")
        _ = subprocess.check_output(f'{self.adb} root'.split(' '))

        # to make sure that we can push files into sdcard
        _ = subprocess.check_output(f'{self.adb} shell chmod 777 /mnt/sdcard'.split(' '))

        # push folder from pc to phone
        _ = subprocess.check_output(f'{self.adb} push {self.path_pc_data} {self.path_phone_data}'.split(' '))

        out = subprocess.check_output(f'{self.adb} shell ls '
                                      f'{self.path_phone_data}'.split(' ')).decode('utf-8')[:-2].replace("\r", "").split('\n')
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
            _ = subprocess.check_output(f'{self.adb} install {curr_apk_path}'.split(' '))

        print(f'all apks installed')


if __name__ == "__main__":
    preparer = Preparer("D:\\diploma\\console_tools\\adb-tools",
                        "D:\\diploma\\tests_results",
                        "D:\\diploma\\projects_scripts\\freq_gov_test\\apk",
                        "D:\\diploma\\projects_scripts\\freq_gov_test\\phoneFiles",
                        "/sdcard/Download/phoneFiles")

    # preparer.push_required_files()
    preparer.install_all_apks()
