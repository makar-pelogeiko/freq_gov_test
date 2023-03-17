import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import ticker
import os
import csv
from statistics import median

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()


@ticker.FuncFormatter
def major_formatter_y(x, pos):
    x_str = str(int(x))
    counter = 0
    out_lst = []

    for i in range(len(x_str) - 1, -1, -1):
        symb = x_str[i]
        counter += 1

        if counter % 4 == 0:
            out_lst.append('_')
            counter = 1

        out_lst.append(symb)

    out_lst.reverse()
    return ''.join(out_lst)


class StatsPlotter:
    def __init__(self, power_consts, clusters):
        self.power_consts = power_consts
        self.clusters = clusters

    def get_results_dict(self, labeled_govs, test_names, dict_test_number, path_to_results):
        results_d = {}

        for freq_gov in labeled_govs:
            results_d[freq_gov] = {}

            for test_name in test_names:
                results_d[freq_gov][test_name] = {}
                no_file_flag = False

                for test_number in range(0, dict_test_number[test_name]):
                    results_d[freq_gov][test_name][test_number] = {'freq': {}, 'idle': {}}

                    print(f'--- {freq_gov}, {test_name}, {test_number} ----')

                    # Freq reader
                    path_this_test_csvs = os.path.join(path_to_results, test_name, str(test_number))

                    for cluster_n in range(0, len(self.clusters)):
                        path_csv = os.path.join(path_this_test_csvs,
                                                f'{test_number}_freq_diff_cluster{cluster_n}_{freq_gov}_{test_name}.csv')
                        print(path_csv)

                        if not os.path.exists(path_csv):
                            print(f'FILE {path_csv} NOT EXISTS')
                            no_file_flag = True
                            break

                        with open(path_csv, 'r', newline="") as csvfile:
                            freq_reader = csv.reader(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

                            line_num = -1
                            results_d[freq_gov][test_name][test_number]['freq'][cluster_n] = {}

                            for row in freq_reader:

                                line_num += 1

                                if line_num == 0:
                                    continue

                                results_d[freq_gov][test_name][test_number]['freq'][cluster_n][int(row[0])] = int(
                                    row[1])

                    if no_file_flag:
                        no_file_flag = False
                        break

                    # IDLE reader
                    path_csv_idle = os.path.join(path_this_test_csvs,
                                                 f'{test_number}_idle_diff_{freq_gov}_{test_name}.csv')
                    print(path_csv_idle)

                    for cluster_n in range(0, len(self.clusters)):
                        for core_n in self.clusters[cluster_n]:
                            results_d[freq_gov][test_name][test_number]['idle'][core_n] = {}

                    with open(path_csv_idle, 'r', newline="") as csvfile:
                        idle_reader = csv.reader(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

                        line_num = -1

                        for row in idle_reader:

                            line_num += 1

                            if line_num == 0:
                                continue

                            for core in results_d[freq_gov][test_name][test_number]['idle'].keys():
                                results_d[freq_gov][test_name][test_number]['idle'][core][line_num - 1] = {}

                            for index_cpu in range(1, len(row)):
                                results_d[freq_gov][test_name][test_number]['idle'][index_cpu - 1][line_num - 1] = \
                                    int(row[index_cpu])
        return results_d

    def get_energy_consumption_freq(self, power_constants, clusters, freqs_dict):

        energy_sum = 0

        for cluster_n in range(0, len(clusters)):
            for freq in freqs_dict[cluster_n].keys():
                temp_sum = freqs_dict[cluster_n][freq] * power_constants[cluster_n][freq]
                energy_sum += temp_sum * len(clusters[cluster_n])

        return energy_sum / float(3600 * 100)

    def get_energy_consumption_freq_and_idle_low_freq(self, power_constants, clusters, freqs_dict, idle_dict):

        energy_sum = 0

        for cluster_n in range(0, len(clusters)):

            min_freq = min(freqs_dict[cluster_n].keys())

            for core_n in clusters[cluster_n]:

                for freq in freqs_dict[cluster_n].keys():

                    if freq == min_freq:
                        freq_time = freqs_dict[cluster_n][freq] - (float(idle_dict[core_n][1]) / 1_0_000.0)
                        if freq_time < 0:
                            # raise Exception(f"freq_time < 0 | cluster:{cluster_n}, "
                            #                 f"freq{freq} time:{freqs_dict[cluster_n][freq]}, "
                            #                 f"idle time: {idle_dict[core_n][1]}")
                            print(f'!!get_energy_consumption_freq_and_idle_low_freq!!')
                            print(f"{Fore.RED}freq_time < 0 | cluster: {cluster_n}, core: {core_n}, "
                                  f"freq {freq} time: {freqs_dict[cluster_n][freq]}, "
                                  f"idle time: {idle_dict[core_n][1]}{Style.RESET_ALL}")
                            freq_time = 0.0
                    else:
                        freq_time = freqs_dict[cluster_n][freq]

                    temp_sum = freq_time * power_constants[cluster_n][freq]

                    energy_sum += temp_sum
        return energy_sum / float(3600 * 100)

    def get_energy_consumption_freq_idle_precent(self, power_constants, clusters, freqs_dict, idle_dict):
        energy_sum = 0
        for cluster_n in range(0, len(clusters)):

            time_sum = float(sum(freqs_dict[cluster_n].values()))

            for core_n in clusters[cluster_n]:

                for freq in freqs_dict[cluster_n].keys():
                    time_precent = freqs_dict[cluster_n][freq] / time_sum

                    freq_time = freqs_dict[cluster_n][freq] - (float(idle_dict[core_n][1]) / 1_0_000.0) * time_precent

                    if freq_time < 0:
                        print(f'!!!!! get_energy_consumption_freq_idle_precent !!!!!!!')
                        print(f"{Fore.RED}freq_time < 0 | cluster:{cluster_n}, core: {core_n}, "
                              f"freq{freq} time:{freqs_dict[cluster_n][freq]}, "
                              f"idle time: {idle_dict[core_n][1]}{Style.RESET_ALL}")
                        freq_time = 0.0

                    temp_sum = freq_time * power_constants[cluster_n][freq]
                    energy_sum += temp_sum

        return energy_sum / float(3600 * 100)

    def major_formatter_x(self, x):
        x_str = f'{x:.3f}'
        counter = 0
        out_lst = []

        for i in range(len(x_str) - 5, -1, -1):
            symb = x_str[i]
            counter += 1

            if counter % 4 == 0:
                out_lst.append('_')
                counter = 1

            out_lst.append(symb)

        out_lst.reverse()
        out_lst += x_str[-4:]
        return ''.join(out_lst)

    def get_approx_data(self, results_all, test_name, power_constants):
        result = dict()

        for freq_gov in results_all.keys():

            result[freq_gov] = {'solid_freq': [], 'min_freq_idle': [], 'freq_precent': []}

            for test_num in results_all[freq_gov][test_name].keys():
                solid_res = self.get_energy_consumption_freq(power_constants, self.clusters,
                                                             results_all[freq_gov][test_name][test_num]['freq'])
                min_freq_minus_idle = self.get_energy_consumption_freq_and_idle_low_freq(power_constants,
                                                                                         self.clusters,
                                                                                         results_all[freq_gov][
                                                                                             test_name][
                                                                                             test_num]['freq'],
                                                                                         results_all[freq_gov][
                                                                                             test_name][
                                                                                             test_num]['idle'])

                freq_precent_idle = self.get_energy_consumption_freq_idle_precent(power_constants,
                                                                                  self.clusters,
                                                                                  results_all[freq_gov][test_name][
                                                                                      test_num][
                                                                                      'freq'],
                                                                                  results_all[freq_gov][test_name][
                                                                                      test_num][
                                                                                      'idle'])
                result[freq_gov]['solid_freq'].append(solid_res)
                result[freq_gov]['min_freq_idle'].append(min_freq_minus_idle)
                result[freq_gov]['freq_precent'].append(freq_precent_idle)

        return result

    def get_stats_data(self, processed_data):
        result = dict()

        for freq_gov in processed_data.keys():
            result[freq_gov] = dict()

            for approx_type in processed_data[freq_gov].keys():
                min_e = min(processed_data[freq_gov][approx_type])
                max_e = max(processed_data[freq_gov][approx_type])
                median_e = median(processed_data[freq_gov][approx_type])

                result[freq_gov][approx_type] = {'min': min_e, 'max': max_e, 'median': median_e}

        return result

    def restruct_data_for_plot(self, data_dict, list_freq_govs):

        new_result_dict = {}

        for freq_gov in list_freq_govs:

            for approx_type in data_dict[freq_gov].keys():

                if approx_type not in new_result_dict.keys():
                    new_result_dict[approx_type] = {'min': [], 'max': [], 'median': [], 'labels': []}

                new_result_dict[approx_type]['median'].append(data_dict[freq_gov][approx_type]['median'])

                new_result_dict[approx_type]['min'].append(data_dict[freq_gov][approx_type]['median'] -
                                                           data_dict[freq_gov][approx_type]['min'])

                new_result_dict[approx_type]['max'].append(data_dict[freq_gov][approx_type]['max'] -
                                                           data_dict[freq_gov][approx_type]['median'])

                new_result_dict[approx_type]['labels'].append(
                    f"{self.major_formatter_x(new_result_dict[approx_type]['median'][-1])} \n-"
                    f"{self.major_formatter_x(new_result_dict[approx_type]['min'][-1])} \n+"
                    f"{self.major_formatter_x(new_result_dict[approx_type]['max'][-1])}")
        return new_result_dict

    def make_plot(self, test_name, results_all, header, save_path, image_name,
                  save_img=True, need_white_back=True, show_plot=True):

        gov_names = list(results_all.keys())

        approx_data = self.get_approx_data(results_all, test_name, self.power_consts)
        stats_data = self.get_stats_data(approx_data)
        plot_ready_data = self.restruct_data_for_plot(stats_data, gov_names)

        matplotlib.rcParams['figure.figsize'] = [16, 9]

        if need_white_back:
            matplotlib.rcParams['axes.facecolor'] = 'white'
            matplotlib.rcParams['savefig.facecolor'] = 'white'

        fig, ax = plt.subplots()

        width = 0.9  # the width of the bars

        x_pos = np.arange(0, 3 * len(gov_names), 3)
        # x_pos = np.arange(0, 9, 2)

        bar_freq_only = ax.bar(x_pos, plot_ready_data['solid_freq']['median'], width,
                               yerr=[plot_ready_data['solid_freq']['min'], plot_ready_data['solid_freq']['max']],
                               align='center', alpha=0.5, ecolor='gray', capsize=10)

        bar_min_freq = ax.bar(x_pos + width, plot_ready_data['min_freq_idle']['median'], width,
                              yerr=[plot_ready_data['min_freq_idle']['min'], plot_ready_data['min_freq_idle']['max']],
                              align='center', alpha=0.5, ecolor='gray', capsize=10)

        bar_precent = ax.bar(x_pos + 2 * width, plot_ready_data['freq_precent']['median'], width,
                             yerr=[plot_ready_data['freq_precent']['min'], plot_ready_data['freq_precent']['max']],
                             align='center', alpha=0.5, ecolor='gray', capsize=10)

        ax.set_ylabel('power consumptoin in mAh')

        ax.set_xticks([pos + width for pos in x_pos])
        ax.set_xticklabels(gov_names)

        ax.set_title(header)
        ax.yaxis.grid(True)

        ax.bar_label(bar_freq_only, labels=plot_ready_data['solid_freq']['labels'], label_type='edge')
        ax.bar_label(bar_min_freq, labels=plot_ready_data['min_freq_idle']['labels'], label_type='edge')
        ax.bar_label(bar_precent, labels=plot_ready_data['freq_precent']['labels'], label_type='edge')

        ax.legend((bar_freq_only[0], bar_min_freq[0], bar_precent[0]), ('freq_only', 'min_freq-idle', 'precent-idle'))

        ax.yaxis.set_major_formatter(major_formatter_y)
        # ax.ticklabel_format(style='plain', axis='y')
        min_y, max_y = ax.get_ylim()
        ax.set_ylim(min_y, max_y * 1.1)

        plt.tight_layout()

        if save_img:
            img_path = os.path.join(save_path, image_name)
            plt.savefig(img_path)
            print(f'image writen on disk: {img_path}.png')

        if show_plot:
            plt.show()


if __name__ == "__main__":
    import config
    from testing_core.modules_loader import ModulesLoader

    loader = ModulesLoader()
    loader.load_tests()
    test_names = list(loader.get_tests_dict().keys())

    plotter = StatsPlotter(config.power_consts, config.clusters)

    dict_test_number = {}
    for test_name in test_names:
        dict_test_number[test_name] = len(os.listdir(os.path.join(config.path_plotter_results, test_name)))

    results_all = plotter.get_results_dict(config.freq_governors_plot, test_names,
                                           dict_test_number, config.path_plotter_results)
    plotter.make_plot('videoVLC', results_all,
                      'videoVLC power consumption',
                      config.path_plot_img_results, 'videoVLC',
                      show_plot=False)
