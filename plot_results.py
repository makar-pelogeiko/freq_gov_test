from testing_core.plot_manager import PlotManager
import config

if __name__ == "__main__":

    executed_labels = {}
    for gov in config.freq_governors_plot:
        executed_labels[gov] = []

        label = ''

        if gov in config.freq_govs_tuners.keys():
            for tuner in config.freq_govs_tuners[gov]:
                label = ''
                label += tuner['name']

                if gov in config.freq_govs_tuners_labels.keys():
                    label += config.freq_govs_tuners_labels[gov]

                executed_labels[gov].append(label)

        else:
            if gov in config.freq_govs_tuners_labels.keys():
                label += config.freq_govs_tuners_labels[gov]

            executed_labels[gov].append(label)

    plotter = PlotManager(config.use_all_test_names, config.test_names, config.freq_governors_plot,
                          executed_labels,
                          config.power_consts, config.clusters, config.path_plotter_results,
                          config.path_plot_img_results, config.show_plot, config.save_img)
    plotter.make_plots(print_all_results=True)
