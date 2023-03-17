from testing_core.main_logic import MainLogic
import os
import subprocess


class FreqGovChanger:
    def __init__(self, path_to_adb):
        self.adb = os.path.join(path_to_adb, 'adb')
        MainLogic.check_adb_connection(self.adb)

        out = subprocess.check_output(f'{self.adb} shell cd /sys/devices/system/cpu && ls | grep cpu'.split(' '))

        cpus_out = out.decode('utf-8').replace("\r", "").split('\n')

        cpus_amount = len(list(filter(lambda item: item[3:].isnumeric(), cpus_out)))
        self.cpus_amount = cpus_amount

        core_n = 0
        first_core_clusters = []
        while core_n < cpus_amount:
            _ = subprocess.check_output(
                f'{self.adb} shell echo 1 > /sys/devices/system/cpu/cpu{core_n}/online'.split(' '))
            out = subprocess.check_output(
                f'{self.adb} shell cat /sys/devices/system/cpu/cpu{core_n}/cpufreq/related_cpus'.split(' '))

            related_cpus = list(map(lambda cpu_s: int(cpu_s), out.decode('utf-8').strip().split(' ')))
            first_core_clusters.append(min(related_cpus))

            core_n = max(related_cpus) + 1

        self.first_core_clusters = first_core_clusters

    def change_governor(self, gov_name):

        out = subprocess.check_output(
            f'{self.adb} shell cat '
            f'/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor'.split(' ')).decode('utf-8').strip('\r\n')

        if out == gov_name:
            print(f"governor: {gov_name} is already used")
            return

        cluster_n = 0
        for core_n in self.first_core_clusters:
            _ = subprocess.check_output(
                f'{self.adb} shell echo {gov_name} > '
                f'/sys/devices/system/cpu/cpu{core_n}/cpufreq/scaling_governor'.split(' '))

            print(f'cluster: {cluster_n}, (core: {core_n}) new governor: {gov_name}')
            cluster_n += 1

    def set_tuners(self, tuners: dict, freq_gov):
        if len(tuners.keys()) == 0:
            print("no tuners")
            return

        for idx, core_n in enumerate(tuners['cores']):
            for file_name, value in tuners['core_tuners'][idx].items():
                _ = subprocess.check_output(
                    f'{self.adb} shell echo 1 > '
                    f'/sys/devices/system/cpu/cpu{core_n}/online'.split(' '))

                _ = subprocess.check_output(
                    f'{self.adb} shell echo {value} > '
                    f'/sys/devices/system/cpu/cpu{core_n}/cpufreq/{freq_gov}/{file_name}'.split(' '))

                print(f'governor: {freq_gov}, core: {core_n} || {file_name} = {value}')


if __name__ == "__main__":
    path_adb = "D:\\diploma\\console_tools\\adb-tools"
    changer = FreqGovChanger(path_adb)
    changer.change_governor("interactive")
