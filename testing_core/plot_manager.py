from testing_core.stats_plotter import StatsPlotter
from testing_core.modules_loader import ModulesLoader
import os


class PlotManager:
    def __init__(self, use_all_test_names, test_names, freq_governors, labels,
                 power_consts, clusters, path_plotter_results,
                 path_plot_img_results, show_plot, save_img):

        self.use_all_test_names = use_all_test_names
        self.test_names = test_names

        self.freq_governors = freq_governors

        self.labels = labels

        self.power_consts = power_consts

        self.clusters = clusters

        self.path_plotter_results = path_plotter_results

        self.path_plot_img_results = path_plot_img_results
        self.show_plot = show_plot
        self.save_img = save_img

    def _get_test_names(self):
        if self.use_all_test_names and len(self.test_names) != 0:
            print(f"config.test_names: {self.test_names} have to be empty,"
                  f" or config.use_all_test_names have to be False")

        if self.use_all_test_names:
            loader = ModulesLoader()
            loader.load_tests()
            return list(loader.get_tests_dict().keys())

        else:
            return self.test_names

    def _get_labeled_gov_names(self):
        labeled_govs = []
        for gov in self.freq_governors:

            if gov in self.labels.keys():
                for val in self.labels[gov]:
                    labeled_govs.append(gov + val)

            else:
                labeled_govs.append(gov)

        return labeled_govs

    def make_plots(self, print_all_results=True):
        test_names = self._get_test_names()
        labeled_govs = self._get_labeled_gov_names()
        plotter = StatsPlotter(self.power_consts, self.clusters)

        dict_test_number = {}
        for test_name in test_names:
            dict_test_number[test_name] = len(os.listdir(os.path.join(self.path_plotter_results, test_name)))

        results_all = plotter.get_results_dict(labeled_govs, test_names, dict_test_number,
                                               self.path_plotter_results)

        if print_all_results:
            print(f'--- all results data loaded ----')
            print(results_all)

        for name in test_names:
            plotter.make_plot(name, results_all, f'{name} power consumption in mAh',
                              self.path_plot_img_results,
                              f'{name}_power_consumption',
                              show_plot=self.show_plot, save_img=self.save_img)
