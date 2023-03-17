# Configuration file for all utils in this folder

# path to adb executable file.
#
# path to adb do not required because
# path to adb is already added in PATH environmental variable
# put an empty string here
path_adb = "D:\\diploma\\console_tools\\adb-tools"

# path to folder where tests data results will be present
path_results = "D:\\diploma\\tests_results"

# path to folder where all required *.apk files are presented
path_apk = "D:\\diploma\\projects_scripts\\freq_gov_test\\apk"

# path to folder on the PC where all files required by tests are presented
# WARNING last folder name have to be same as last folder name in `path_phone_data` variable
path_pc_data = "D:\\diploma\\projects_scripts\\freq_gov_test\\phoneFiles"

# path to folder on the smartphone where all files required by tests have to be presented
# WARNING last folder name have to be same as last folder name in `path_pc_data` variable
path_phone_data = "/sdcard/Download/phoneFiles"

# list of arguments for standard tests, for phone_prepare class and e.t.c
standard_test_args = [path_adb, path_results, path_apk, path_pc_data, path_phone_data]

# pushes all folder with data files to smartphone when set to True
need_push_data_folder = False

# install all apk files from PC apk folder to smartphone when set to True
# WARNING: do not start test without checking all test apps for correct working on your phone
need_install_apks = False

# For Galaxy S7 (lineage 17.1 stock rom only)
# set all cores available to online
need_anti_hotplug = False

#####################################################################
# run all test from <test_scenario> folder if set to True
run_all_tests = False

# run only a specified list of tests from <test_scenario> in strict order as in list
tests_run_queue = ['videoVLC', 'flappyBird', 'trialXTreme3', 'camera', 'type', 'twitch']
# tests_run_queue = ['trialXTreme3']#, 'flappyBird', 'trialXTreme3', 'camera', 'type', 'twitch']

# init for custom test (not used in stock version of this project)
# specifies ordered list of arguments for test scenario init ()
# passes separated args from list
tests_init_args = {}
# {'test_name': {'use_standard_args': True, 'custom_args': []}}

# arguments for test function of specified test scenario
# as default uses list with 1 argument - test time duration in sec
# WARNING test time duration is about 20 seconds longer in fact
tests_func_args = {'videoVLC': [60], 'flappyBird': [60],
                   'trialXTreme3': [60], 'camera': [60],
                   'type': [60], 'twitch': [60]}
# {'test_name': list(int_time_sec, ...)}

# dictionary specifies times to repeat particular test scenario
tests_func_repeat_num = {'videoVLC': 3, 'flappyBird': 3, 'trialXTreme3': 3, 'camera': 3, 'type': 3, 'twitch': 3}
# {'test_name': int_times_to_run}

# time to sleep before test in sec
test_cool_time = 30

#####################################################################

# default data collector is used when flag set to True
use_default_test_data_collector = True

# class name of custom data collector from <data_collectors> folder
custom_data_collector_class_name = ''

# arguments for initialization custom data collector class
data_collector_args = []

# EXAMPLE:
# use_default_test_data_collector = False
# custom_data_collector_class_name = 'FreqOnlyCollector'
# data_collector_args = ["D:\\diploma\\console_tools\\adb-tools\\adb"]

#####################################################################

# default results writer is used when flag set to True
use_default_test_results_writer = True

# class name of custom data writer from <test_result_writers> folder
custom_test_results_writer_class_name = ''

# arguments for initialization custom data writer class
test_results_writer_args = []

# EXAMPLE:
# use_default_test_results_writer = False
# custom_test_results_writer_class_name = 'FreqOnlyWriter'
# test_results_writer_args = [path_results]

#####################################################################
# CONFIG FOR PLOTTER
#####################################################################

# smartphone power values form powerprofile.xml or from /proc/last_kmsg
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
        442000: 15,

        338000: 15
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
        728000: 230,

        624000: 230,
        520000: 230
    }
}

# ordered list of lists. inner list represents cores in one cluster. Zero cluster represents by list index 0.
clusters = [[0, 1, 2, 3], [4, 5, 6, 7]]

# path where data for making plots presented
path_plotter_results = path_results

# path where plots images should be saved
path_plot_img_results = path_plotter_results

# DVFS governors names to take into consideration in plots drawn
freq_governors_plot = ['spsa2tmpn', 'schedutil', 'interactive', 'ondemand']

# plots for all available test names would be made when flag set to True
use_all_test_names = False

# plots only for specified by list test names would be made
# WARNING: use_all_test_names HAVE TO BE False
test_names = tests_run_queue

# plot would be shown right after making when flag set to True
show_plot = False

# plot would be saved as *.png file right after making when flag set to True
save_img = True

#####################################################################
# CONFIG FOR TEST GOVS MANAGER
#####################################################################

# time to sleep after governor switched and tuners prepared in sec.
gov_cool_time = 30

# list of DVFS governors to test
freq_governors = freq_governors_plot

# dictionary defines tunable params of DVFS governor
# value of 'name' key would be added to governor name in order to make uniq governor name
# several sets of tunable params may be specified
freq_govs_tuners = {
    'spsa2tmpn': [
        {'name': '-a2b1t70',
         'cores': [0, 4],
         'core_tuners': [{'alpha': 2, 'betta': 1, 'target_load': 70},
                         {'alpha': 2, 'betta': 1, 'target_load': 70}]
         },
        {'name': '-a2b2t70',
         'cores': [0, 4],
         'core_tuners': [{'alpha': 2, 'betta': 2, 'target_load': 70},
                         {'alpha': 2, 'betta': 2, 'target_load': 70}]
         },
        {'name': '-a3b1t70',
         'cores': [0, 4],
         'core_tuners': [{'alpha': 3, 'betta': 1, 'target_load': 70},
                         {'alpha': 3, 'betta': 1, 'target_load': 70}]
         },
        {'name': '-a3b2t70',
         'cores': [0, 4],
         'core_tuners': [{'alpha': 3, 'betta': 2, 'target_load': 70},
                         {'alpha': 3, 'betta': 2, 'target_load': 70}]
         },
        {'name': '-a3b3t70',
         'cores': [0, 4],
         'core_tuners': [{'alpha': 3, 'betta': 3, 'target_load': 70},
                         {'alpha': 3, 'betta': 3, 'target_load': 70}]
         }
    ]
}

# labels that would be added to DVFS governor name after governor name and 'name' value of
# freq_govs_tuners if it defined
# this setting is only for convenience for running <test_govs.py> several times without missing of previous results
freq_govs_tuners_labels = {}
# freq_govs_tuners_labels = {'spsa2tmpn': 'nice'}

# plots are made after all test tasks are done if flag set to True
make_plot = True
