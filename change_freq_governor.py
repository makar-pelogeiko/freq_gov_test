from testing_core.freq_gov_changer import FreqGovChanger
import config
import sys

if __name__ == "__main__":
    # sys.argv.append('interactive')
    if len(sys.argv) > 1:
        gov_name = sys.argv[1]

        print(f'try to set new freq governor: {gov_name}')

        changer = FreqGovChanger(config.path_adb)
        changer.change_governor(gov_name)
