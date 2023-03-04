import json
import os
import csv


class DefaultResultsWriter:
    def __init__(self, path_results):
        self.path_results = path_results

    def write_results(self, test_name, freq_gov_name, stats_of_tests, results):
        for test_id in range(0, len(results)):

            curr_path_results = os.path.join(self.path_results, test_name, f'{test_id}')

            if not os.path.exists(curr_path_results):
                os.makedirs(curr_path_results)

            # Write JSON additional test stats
            path_stat = os.path.join(curr_path_results, f'{test_id}_{freq_gov_name}_{test_name}.json')
            with open(path_stat, 'w') as outfile:
                json.dump(stats_of_tests[test_id], outfile)

            # Write idle stats
            for cur_name in results[test_id].keys():

                cpu_amount = len(results[test_id][cur_name]['idle'].keys())

                idle_state_amount = 0
                for i in range(0, cpu_amount):
                    if idle_state_amount < len(results[test_id][cur_name]['idle'][i].keys()):
                        idle_state_amount = len(results[test_id][cur_name]['idle'][i].keys())

                header = ['State'] + [f'cpu{i}' for i in range(0, cpu_amount)]

                full_path = os.path.join(curr_path_results,
                                         f'{test_id}_idle_{cur_name}_{freq_gov_name}_{test_name}.csv')
                with open(full_path, 'w', newline="") as file_out:
                    writer = csv.writer(file_out, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                    writer.writerow(header)

                    for state in range(0, idle_state_amount):
                        data_row = [f'state{state}']

                        for cpu in range(0, cpu_amount):
                            if state in results[test_id][cur_name]['idle'][cpu].keys():
                                data_row.append(results[test_id][cur_name]['idle'][cpu][state])
                            else:
                                data_row.append('')

                        writer.writerow(data_row)

            # Write freq stats
            for cur_name in results[test_id].keys():
                for cluster_id in range(0, len(results[test_id][cur_name]['freq'])):

                    header = ['Freq',
                              f'cpu_{results[test_id][cur_name]["freq"][cluster_id]["start_core"]}-'
                              f'{results[test_id][cur_name]["freq"][cluster_id]["end_core"]}']

                    full_path = os.path.join(curr_path_results,
                                             f'{test_id}_freq_{cur_name}_'
                                             f'cluster{cluster_id}_{freq_gov_name}_{test_name}.csv')

                    with open(full_path, 'w', newline="") as file_out:
                        writer = csv.writer(file_out, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                        writer.writerow(header)

                        for freq in results[test_id][cur_name]["freq"][cluster_id]["data"].keys():
                            writer.writerow([freq, results[test_id][cur_name]["freq"][cluster_id]["data"][freq]])
