from testing_core.plot_manager import PlotManager
import config

if __name__ == "__main__":
    plotter = PlotManager(config.use_all_test_names, config.test_names, config.freq_governors_plot,
                          config.power_consts, config.clusters, config.path_plotter_results,
                          config.path_plot_img_results, config.show_plot, config.save_img)
    plotter.make_plots(print_all_results=True)
