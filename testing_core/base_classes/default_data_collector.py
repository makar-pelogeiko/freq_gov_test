import subprocess


class DefaultDataCollector:
    def __init__(self, path_adb_usage):
        self.adb = path_adb_usage

    def _get_freq_data_cluster(self, core_n):
        # Get stats for the first core in certain cluster and frequencies
        out = subprocess.check_output(f'{self.adb} shell cat /sys/devices/system/cpu/cpu{core_n}'
                                      f'/cpufreq/stats/time_in_state'.split(' '))

        # create first part of stats result for certain cluster
        freqs_stats = out.decode('utf-8').replace("\r", "").split('\n')[:-1]

        # make list of list with int data type in it
        processed_stats = list(map(lambda lst_item: list(map(lambda st_item: int(st_item), lst_item)),
                                   map(lambda item: item.split(' '), freqs_stats)))

        cluster_data = dict()
        for stat_part in processed_stats:
            cluster_data[stat_part[0]] = stat_part[1]

        return cluster_data

    def _get_idle_data(self, core_n):
        idle_data = dict()

        try:
            _ = subprocess.check_output(
                f'{self.adb} shell echo 1 > /sys/devices/system/cpu/cpu{core_n}/online'.split(' '))
            out = subprocess.check_output(
                f'{self.adb} shell cd /sys/devices/system/cpu/cpu{core_n}/cpuidle && ls | grep state'.split(' '))

        except subprocess.CalledProcessError as e:
            print(f"Cpu {core_n} idle permission exception!\n"
                  f"probably hotplug enabled")
            raise e

        states_out = out.decode('utf-8').replace("\r", "").split('\n')
        states_amount = len(list(filter(lambda item: item[5:].isnumeric(), states_out)))

        for state in range(0, states_amount):
            out = subprocess.check_output(
                f'{self.adb} shell cat /sys/devices/system/cpu/cpu{core_n}/cpuidle/state{state}/time'.split(' '))

            time_in_state = int(out.decode("utf-8"))

            idle_data[state] = time_in_state

        return idle_data

    def collect_data(self) -> dict:
        """
        :return: {'idle': {int_core_n: {int_state: int_time_int_state}} ,
                  'freq': [ {'start_core': int, 'end_core': int, 'data':  <cluster_0 dict {freq : core_time}> }]}
        """

        main_result = {'idle': {}, 'freq': []}

        out = subprocess.check_output(f'{self.adb} shell cd /sys/devices/system/cpu && ls | grep cpu'.split(' '))

        cpus_out = out.decode('utf-8').replace("\r", "").split('\n')
        cpus_amount = len(list(filter(lambda item: item[3:].isnumeric(), cpus_out)))

        core_n = 0
        next_cluster = core_n
        cluster = -1

        while core_n < cpus_amount:

            if core_n == next_cluster:
                cluster += 1
                _ = subprocess.check_output(
                    f'{self.adb} shell echo 1 > /sys/devices/system/cpu/cpu{core_n}/online'.split(' '))
                # Get number of cores in this cluster
                out = subprocess.check_output(
                    f'{self.adb} shell cat /sys/devices/system/cpu/cpu{core_n}/cpufreq/related_cpus'.split(' '))

                related_cpus = list(map(lambda cpu_s: int(cpu_s), out.decode('utf-8').strip().split(' ')))
                related_cpus_number = len(related_cpus)

                next_cluster = max(related_cpus) + 1

                cluster_freq_data = self._get_freq_data_cluster(core_n)
                result_full_cluster = {'start_core': core_n, 'end_core': max(related_cpus), 'data': cluster_freq_data}

                main_result['freq'].append(result_full_cluster)

            core_idle_data = self._get_idle_data(core_n)
            main_result['idle'][core_n] = core_idle_data

            core_n += 1

        return main_result

    @staticmethod
    def make_diff_data(before: dict, after: dict) -> dict:
        """
        :return: {'idle': {int_core_n: {int_state: int_time_int_state}} ,
                  'freq': [ {'start_core': int, 'end_core': int, 'data': <cluster_0 dict {freq : core_time}> }]}
        """
        diff_result = {'idle': {}, 'freq': []}

        # Freq diff
        for i in range(0, len(after['freq'])):
            cluster_freq = {'start_core': after['freq'][i]['start_core'],
                            'end_core': after['freq'][i]['end_core'],
                            'data': {}}

            for freq in after['freq'][i]['data'].keys():
                cluster_freq['data'][freq] = after['freq'][i]['data'][freq] - before['freq'][i]['data'][freq]

            diff_result['freq'].append(cluster_freq)

        # Idle diff
        for core in after['idle'].keys():
            diff_result['idle'][core] = dict()

            for state in after['idle'][core].keys():
                diff_result['idle'][core][state] = after['idle'][core][state] - before['idle'][core][state]

        return diff_result
