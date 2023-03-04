from testing_core.modules_loader import ModulesLoader
from testing_core.main_logic import MainLogic
import config


if __name__ == '__main__':
    #print(f"get ready {__file__}")
    #loader = ModulesLoader()
    #loader.load_tests()

    logic = MainLogic()
    logic.execute_list()