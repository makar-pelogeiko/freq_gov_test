from testing_core.stats_plotter import StatsPlotter
from testing_core.modules_loader import ModulesLoader
import os
import config


class PlotManager:
    def __init__(self):
        pass

    def _get_test_names(self):
        if config.use_all_test_names and len(config.test_names) != 0:
            print(f"config.test_names: {config.test_names} have to be empty,"
                  f" or config.use_all_test_names have to be False")

        if config.use_all_test_names:
            loader = ModulesLoader()
            loader.load_tests()
            return list(loader.get_tests_dict().keys())

        else:
            return config.test_names

    def make_plots(self):
        test_names = self._get_test_names()
        plotter = StatsPlotter(config.power_consts, config.clusters)

        dict_test_number = {}
        for test_name in test_names:
            dict_test_number[test_name] = len(os.listdir(os.path.join(config.path_plotter_results, test_name)))

        results_all = plotter.get_results_dict(config.freq_governors, test_names, dict_test_number,
                                               config.path_plotter_results)

        for name in test_names:
            plotter.make_plot(name, results_all, f'{name} power consumption in mmfWatts',
                              config.path_plot_img_results,
                              f'{name}_power_consumption',
                              show_plot=config.show_plot, save_img=config.save_img)


if __name__ == "__main__":
    plotter = PlotManager()
    plotter.make_plots()
