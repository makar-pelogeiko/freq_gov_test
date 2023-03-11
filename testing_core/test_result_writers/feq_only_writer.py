import json
import os
import csv
from testing_core.base_classes.default_results_writer import DefaultResultsWriter


class FreqOnlyWriter(DefaultResultsWriter):
    def __init__(self, path_results):
        super(FreqOnlyWriter, self).__init__(path_results)

    def write_results(self, test_name, freq_gov_name, metka, stats_of_tests, results):
        for test_id in range(0, len(results)):

            path_stat = os.path.join(self.path_results, f'{test_id}_{freq_gov_name}{metka}_{test_name}.json')
            with open(path_stat, 'w') as outfile:
                json.dump(stats_of_tests[test_id], outfile)

            for cur_name in results[test_id].keys():

                core_n = -1
                for cluster_id in range(0, len(results[test_id][cur_name])):

                    header = ['Freq']
                    first_key = list(results[test_id][cur_name][cluster_id].keys())[0]
                    for _ in results[test_id][cur_name][cluster_id][first_key]:
                        core_n += 1
                        header.append(f'cpu{core_n}')

                    full_path = os.path.join(self.path_results,
                                             f'{test_id}_{cur_name}_'
                                             f'cluster{cluster_id}_{freq_gov_name}{metka}_{test_name}.csv')

                    with open(full_path, 'w', newline="") as file_out:
                        writer = csv.writer(file_out, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                        writer.writerow(header)
                        for freq, times in results[test_id][cur_name][cluster_id].items():
                            temp = [freq] + times
                            writer.writerow(temp)
