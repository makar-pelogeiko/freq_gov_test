from testing_core.main_logic import MainLogic
import os
import subprocess


class FreqGovChanger:
    def __init__(self, path_to_adb, gov_name):
        self.adb = os.path.join(path_to_adb, 'adb')
        self.gov_name = gov_name
        MainLogic.check_adb_connection(self.adb)

    def change_governor(self):

        out = subprocess.check_output(
            f'"{self.adb}" shell cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor').decode('utf-8').strip('\r\n')

        if out == self.gov_name:
            print(f"governor: {self.gov_name} is already used")
            return

        out = subprocess.check_output(f'"{self.adb}" shell "cd /sys/devices/system/cpu && ls | grep cpu" ')

        cpus_out = out.decode('utf-8').split('\r\n')
        cpus_amount = len(list(filter(lambda item: item[3:].isnumeric(), cpus_out)))

        core_n = 0
        first_core_clusters = []
        while core_n < cpus_amount:
            out = subprocess.check_output(
                f'"{self.adb}" shell cat /sys/devices/system/cpu/cpu{core_n}/cpufreq/related_cpus')

            related_cpus = list(map(lambda cpu_s: int(cpu_s), out.decode('utf-8').strip().split(' ')))
            first_core_clusters.append(min(related_cpus))

            core_n = max(related_cpus) + 1

        cluster_n = 0
        for core_n in first_core_clusters:

            _ = subprocess.check_output(
                f'"{self.adb}" shell echo {self.gov_name} > '
                f'/sys/devices/system/cpu/cpu{core_n}/cpufreq/scaling_governor')

            print(f'cluster: {cluster_n}, (core: {core_n}) new governor: {self.gov_name}')
            cluster_n += 1


if __name__ == "__main__":
    path_adb = "D:\\diploma\\console_tools\\adb-tools"
    changer = FreqGovChanger(path_adb, "interactive")
    changer.change_governor()

