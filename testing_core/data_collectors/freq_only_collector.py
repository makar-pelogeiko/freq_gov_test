import subprocess
from testing_core.base_classes.default_data_collector import DefaultDataCollector


class FreqOnlyCollector(DefaultDataCollector):
    def __init__(self, path_adb_usage):
        super(FreqOnlyCollector, self).__init__(path_adb_usage)

    def collect_data(self) -> list:
        """
        :return: list [ <cluster_0 dict {freq : [core_0_time, core_1_time, ...]}>, cluster_1 dict {freq : [
        core_4_time, core_5_time, ...]}]
        """

        proc = subprocess.Popen(f'"{self.adb}" shell "cd /sys/devices/system/cpu && ls | grep cpu" ',
                                stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        cpus_out = out.decode('utf-8').split('\r\n')
        cpus_number = len(list(filter(lambda item: item[3:].isnumeric(), cpus_out)))

        core_n = 0
        cluster = 0
        result_stats = []

        while core_n < cpus_number:

            # Get number of cores in this cluster
            (out, err) = (
                subprocess.Popen(f'"{self.adb}" shell cat /sys/devices/system/cpu/cpu{core_n}/cpufreq/related_cpus',
                                 stdout=subprocess.PIPE, shell=True)).communicate()
            related_cpus = out.decode('utf-8').strip().split(' ')
            related_cpus_number = len(related_cpus)

            # Get stats for the first core in certain cluster and frequencies
            (out, err) = (subprocess.Popen(f'"{self.adb}" shell cat /sys/devices/system/cpu/cpu{core_n}'
                                           f'/cpufreq/stats/time_in_state',
                                           stdout=subprocess.PIPE, shell=True)).communicate()

            # create first part of stats result for certain cluster
            freqs_stats = out.decode('utf-8').split('\r\n')[:-1]
            processed_stats = list(map(lambda item: item.split(' '), freqs_stats))

            result_stats.append(dict())
            for stat_part in processed_stats:
                result_stats[cluster][int(stat_part[0])] = [int(stat_part[1])]

            for _ in range(0, related_cpus_number - 1):
                core_n += 1
                (out, err) = (subprocess.Popen(f'"{self.adb}" shell cat /sys/devices/system/cpu/cpu{core_n}'
                                               f'/cpufreq/stats/time_in_state',
                                               stdout=subprocess.PIPE, shell=True)).communicate()

                freqs_stats = out.decode('utf-8').split('\r\n')[:-1]
                processed_stats = list(map(lambda item: item.split(' '), freqs_stats))

                for stat_part in processed_stats:
                    result_stats[cluster][int(stat_part[0])].append(int(stat_part[1]))

            cluster += 1
            core_n += 1

        return result_stats

    @staticmethod
    def make_diff_data(before: list, after: list) -> list:
        diff_result = []

        for cluster_index in range(0, len(after)):
            diff = dict()

            for freq, times in after[cluster_index].items():
                diff[freq] = []

                for time_index in range(0, len(times)):
                    diff[freq].append(after[cluster_index][freq][time_index] - before[cluster_index][freq][time_index])

            diff_result.append(diff)

        return diff_result
