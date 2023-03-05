path_adb = "D:\\diploma\\console_tools\\adb-tools"
path_results = "D:\\diploma\\tests_results"
path_apk = "D:\\diploma\\freq_gov_test\\apk"
path_pc_data = "D:\\diploma\\freq_gov_test\\phoneFiles"
path_phone_data = "/sdcard/Download/phoneFiles"

standard_test_args = [path_adb, path_results, path_apk, path_pc_data, path_phone_data]


# Flag defenition
need_push_data_folder = False

# Bool flag
need_install_apks = False

# For Galaxy S7
need_anti_hotplug = True

#####################################################################
# Bool flag
run_all_tests = False

tests_run_queue = ['videoVLC']

tests_init_args = {}
# {'test_name': {'use_standard_args': True, 'custom_args': []}}

tests_func_args = {'videoVLC': [3]}
# {'test_name': list(int_time_sec, ...)}

tests_func_times = {'videoVLC': 3}
# {'test_name': int_times_to_run}

#####################################################################

# Bool flag
use_default_test_data_collector = True

custom_data_collector_class_name = ''

data_collector_args = []

# use_default_test_data_collector = False
# custom_data_collector_class_name = 'FreqOnlyCollector'
# data_collector_args = ["D:\\diploma\\console_tools\\adb-tools\\adb"]

#####################################################################

use_default_test_results_writer = True

custom_test_results_writer_class_name = ''

test_results_writer_args = []

# use_default_test_results_writer = False
# custom_test_results_writer_class_name = 'FreqOnlyWriter'
# test_results_writer_args = [path_results]

#####################################################################
# CONFIG FOR PLOTTER
#####################################################################
power_consts = {
            0: {
                1586000: 167,
                1482000: 141,
                1378000: 120,
                1274000: 101,
                1170000: 83,
                1066000: 70,
                962000: 57,
                858000: 46,
                754000: 37,
                650000: 29,
                546000: 21,
                442000: 15
            },

            1: {
                2600000: 2431,
                2496000: 2174,
                2392000: 2009,
                2288000: 1817,
                2184000: 1606,
                2080000: 1470,
                1976000: 1314,
                1872000: 1193,
                1768000: 1034,
                1664000: 931,
                1560000: 815,
                1456000: 709,
                1352000: 627,
                1248000: 536,
                1144000: 466,
                1040000: 391,
                936000: 332,
                832000: 279,
                728000: 230
            }
        }

clusters = [[0, 1, 2, 3], [4, 5, 6, 7]]
path_plotter_results = path_results
path_plot_img_results = path_plotter_results
freq_governors = ['spsa2tmpn', 'spsa2copy']

use_all_test_names = False
test_names = ['videoVLC']

show_plot = True
save_img = True
