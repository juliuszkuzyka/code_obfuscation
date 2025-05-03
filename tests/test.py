import sys
import os
import time
import shutil
import subprocess
import pprint
import psutil
from itertools import permutations, chain
from src.obfuscator import CodeObfuscator
from techniques.junk_code import JunkCodeInserter
from techniques.polymorphism import PolymorphismTransformer
from techniques.metamorphism import MetamorphismTransformer
from techniques.ast_manipulation import ASTManipulator
from main import load_code, get_technique_classes


# create executable of "hello_world.py" file, with given techniques
def create_exec(source_code, selected_techniques=None):
    if selected_techniques is None:
        selected_techniques = ["1"]
    techniques = []
    technique_classes = get_technique_classes()
    for num in selected_techniques:
        techniques.append(technique_classes[num]())
    code = load_code(source_code)
    obfuscator = CodeObfuscator(code, techniques)
    obfuscator.create_obfuscated_executable()

# tests if "test" directory is on in Desktop path
def test_test_dir_exec():
    subprocess.run(["dist/obfuscated_exploit.exe"])
    test_dir = os.path.join(os.path.expanduser("~"), "Desktop", "test")
    return os.path.isdir(test_dir)

# tests if calculator is running
def test_cal_exec():
    subprocess.run(["dist/obfuscated_exploit.exe"])
    time.sleep(5)
    found = False

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in ('calc.exe', 'CalculatorApp.exe'):
            found = True
            try:
                proc.terminate()  # Ask it to exit
                proc.wait(timeout=3)  # Wait up to 3 seconds
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass

    return found

# Terminate any running calc.exe or Calculator.exe processes.
def clean_calc():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in ('calc.exe', 'CalculatorApp.exe'):
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass

# delete test directory from Desktop
def clean_test_dir():
    if os.path.isdir(os.path.join(os.path.expanduser("~"), "Desktop/test")):
        shutil.rmtree(os.path.join(os.path.expanduser("~"), "Desktop/test"))

# clean "tests" directory
def clean():
    test_dir = '../tests'
    keep_file = 'test.py'

    for item in os.listdir(test_dir):
        item_path = os.path.join(test_dir, item)

        if item == keep_file:
            continue

        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)

def run_tests(clean_func, test_func, source_code):
    all_combinations = [list(p) for p in chain.from_iterable(permutations(['1', '2', '3', '4'], r) for r in range(1, 5))]
    tests_results = {}
    for i in all_combinations:
        clean()
        clean_func()
        create_exec(source_code, i)
        tests_results[','.join(i)] = test_func()
        clean_func()
        clean()
    return tests_results


if __name__ == "__main__":
    tests_test_dir_results = run_tests(clean_test_dir, test_test_dir_exec, "../hello_world.py")
    # tests_calc_results = run_tests(clean_calc, test_cal_exec, "../calc.py")

    print("==================================================")
    print("tests for hello_world.py")
    print("==================================================")
    pprint.pprint(tests_test_dir_results)

    # print("==================================================")
    # print("tests for calc.py")
    # print("==================================================")
    # pprint.pprint(tests_calc_results)
