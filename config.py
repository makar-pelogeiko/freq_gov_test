path_adb = "D:\\course_work\\adb_Scripts_Tests"
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

tests_func_args = {'videoVLC': [10]}
# {'test_name': list(int_time_sec, ...)}

tests_func_times = {'videoVLC': 1}
# {'test_name': int_times_to_run}

#####################################################################

# Bool flag
use_default_test_data_collector = True

custom_data_collector_class_name = ''

data_collector_args = []

# use_default_test_data_collector = False
# custom_data_collector_class_name = 'FreqOnlyCollector'
# data_collector_args = ["D:\\course_work\\adb_Scripts_Tests\\adb"]

#####################################################################

use_default_test_results_writer = True

custom_test_results_writer_class_name = ''

test_results_writer_args = []

# use_default_test_results_writer = False
# custom_test_results_writer_class_name = 'FreqOnlyWriter'
# test_results_writer_args = [path_results]