#!/c/Python33/python
"""
Running this file executes all the unit tests and integration tests for the miyagi project.  It is 
recommended that you make a hard link of this file into your pre-commit hook in your .git/hooks 
directory.
"""
from subprocess import call, check_output, check_call
import sys
import os
import subprocess
import re
import json
import time
import traceback

########################################
# GET PATH TO TOP LEVEL GIT DIRECTORY  #
########################################

try:
    BASE_DIR_OF_MIYAGI_CODE = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().rstrip()
except:
    #We terminate here since subsequent commands may be relative to this toplevel directory.
    print("Could not resolve path to this top-level project directory.")
    print(sys.exc_info())
    exit(1)

######################################################
# TO DO: Check integrity of json file (ask Emmanuel) #
######################################################

#Set setting file location
os.environ['DJANGO_SETTINGS_MODULE'] = 'miyagi.settings'
setting_file = os.path.join(BASE_DIR_OF_MIYAGI_CODE, 'miyagi')
sys.path.append(setting_file)
from miyagi import settings

# Error code for tests, 0 means pass all tests, non-zero means fail some tests
error_code = 0

########################
# DELETE OLD LOG FILES #
########################
# Check if file exists
#py_file = os.path.join(BASE_DIR_OF_MIYAGI_CODE, "abc.log") # HAVE TO CHANGE THIS
                                                                # The current log file is only produced by pre-commit hook

# Filename for qunit results is stored in a JSON file                                                                
json_file_locator = os.path.join(BASE_DIR_OF_MIYAGI_CODE, 'tests', 'unit', 'js', 'qunit-results-filename.json')
json_data = json.loads(open(json_file_locator).read())
js_file_name = json_data["qunit-results-filename"]
js_file = os.path.join(BASE_DIR_OF_MIYAGI_CODE, 'tests', 'unit', 'js', js_file_name)

#if os.path.isfile(py_file):
#    os.remove(py_file)
if os.path.isfile(js_file):
    os.remove(js_file)

######################################
print ("============================")    
print ("|   RUNNING PYTHON TESTS   |")
print ("============================")
######################################
sys.stdout.flush()

#Used to store results of python tests
python_out = ""
try:
    python_dir = os.path.join(BASE_DIR_OF_MIYAGI_CODE,"tests","unit","python")
    apps = []
    for app in settings.INSTALLED_APPS:
        if not "django" in app:
            apps.append(app)      
    # You need to be in the directory containing "manage.py" for
    # the next command to work, which calls "python manage.py"
    os.chdir(os.path.join(BASE_DIR_OF_MIYAGI_CODE, 'miyagi')) 
    command = ["python","-m" , "coverage","run","--source=" + os.path.join(BASE_DIR_OF_MIYAGI_CODE, 'miyagi', 'registration'), os.path.join(BASE_DIR_OF_MIYAGI_CODE, 'miyagi', "manage.py"),"test"]+apps
    python_out = check_output(command, stderr=subprocess.STDOUT).decode()
    pathToPythonCodeCoverageReportDirectory = os.path.join(BASE_DIR_OF_MIYAGI_CODE, "tests", "reports", "python_unit_tests")
    if not os.path.exists(pathToPythonCodeCoverageReportDirectory):
         os.makedirs(pathToPythonCodeCoverageReportDirectory) 
    error_code = call(["python", "-m", "coverage", "html","--directory=" + pathToPythonCodeCoverageReportDirectory]) | error_code
except subprocess.CalledProcessError as ex:
    traceback.print_exc()
    error_code = 1
    python_out = ex.output.decode()
except Exception as ex:
    traceback.print_exc()
    error_code = 1
    raise

print ("\n")
######################################
print ("============================")    
print ("| RUNNING JAVASCRIPT TESTS |")
print ("============================")    
######################################
sys.stdout.flush()

try:
    path_to_js_directory = os.path.join(BASE_DIR_OF_MIYAGI_CODE, "tests", "unit", "js")
    path_to_test_directory = os.path.join(BASE_DIR_OF_MIYAGI_CODE,"tests")
    js_log_file_name = "jsUnitTestLog.log"
    js_log_file = os.path.join(path_to_js_directory,js_log_file_name)

    os.chdir(path_to_js_directory)
    check_call(["grunt", "unitTestOnLocalMachine"],shell=True)
except Exception as ex:
    traceback.print_exc()
    error_code = 1

#######################
# RUN SELENIUM TESTS  #
#######################
'''
try:
  
    deployment_dir = os.path.join(BASE_DIR_OF_MIYAGI_CODE,"tests","integration","deployment")
    path = os.path.join("..","sauce-connect","sc-4.0-win32","bin","sc.exe");
    ready_file_path = os.path.join(deployment_dir,"ready.txt")
    selelinum_report_file = os.path.join(deployment_dir,"test-output","testng-results.xml")
    path_to_test_directory = os.path.join(BASE_DIR_OF_MIYAGI_CODE,"tests")
    check_file = os.path.join(path_to_test_directory,"checkResult.py")
   
    if os.path.isfile(ready_file_path):
      os.remove(ready_file_path, dir_fd=None)
    
    handle = subprocess.Popen(["cd",deployment_dir,"&&",path,'-u','miyagimove','-k','a4d73f26-2f4e-49c4-8df8-ac501e5480b0','-f','ready.txt'],shell=True)
    timer = 40
    time.sleep(40)
    while not os.path.isfile(ready_file_path) and timer < 100:
        time.sleep(10)  
        timer += 10
    subprocess.call(["cd", deployment_dir, "&&", "java","-jar" ,"MiyagiWebApplication.jar", "-f", "testng_ff.xml", "-e", "dev"], shell=True);
    subprocess.Popen("taskkill /F /T /PID %i"%handle.pid , shell=True)
    error_code = call(["python", check_file,'-s',selelinum_report_file]) | error_code

    
except Exception as ex:
    traceback.print_exc()
    error_code = 1
'''

print ("\n")
####################
# PRINTING RESULTS #
####################

# PYTHON TESTS
py_tests = [0] * 5 # [Total, Failed, Errors, Skipped, Passed]
# Check if log was produced
if not python_out:
    error_code = 1
    print ("[ERROR] Python test results were not able to be stored \n")
else:
    #with open(py_file, 'r') as f:
    #    t = f.read()
    regex = ['Ran (\d+) tests in ', 'failures=(\d+)', 'errors=(\d+)', 'SKIP=(\d+)']
    # Counting num of each test
    i = 0
    for r in regex:
        m = re.findall(r, python_out)
        if m:
            py_tests[i] = int(m[0])
        py_tests[4] -= py_tests[i]
        i = i+1
    py_tests[4] += 2*py_tests[0]

# JAVASCRIPT TESTS
js_tests = [0] * 5  # [Total, Failed, Errors, Skipped, Passed]
# Check if log was produced
if not os.path.isfile(js_file):
    error_code = 1
    print ("[ERROR] JavaScript test results file missing: \n{0}\n".format(js_file))
else:
    with open(js_file, 'r') as f:
        t = f.read()
    regex = ['\"total\":(\d+)', '\"failed\":(\d+)']
    print (t)
    # Counting num of each test
    i = 0
    for r in regex:
        m = re.findall(r, t)
        if m:
            js_tests[i] = int(m[0]) 
        js_tests[4] -= js_tests[i]
        i = i+1
    js_tests[4] += 2*js_tests[0]

print ("\n\n")
print ("============================")
print ("|       TEST RESULTS       |")
print ("============================\n")

print ("+------+---------------+--------+------+------+-----+------+")
print ("| Type | Language      | # Test | Pass | Fail | Err | Skip |")
print ("+------+---------------+--------+------+------+-----+------+")
print ("| Unit | Python        | {0}     | {1}   | {2}    | {3}   | {4}    |".format(py_tests[0], py_tests[4] , py_tests[1], py_tests[2], py_tests[3]))
print ("+------+---------------+--------+------+------+-----+------+")
print ("| Unit | Javascript    | {0}     | {1}    | {2}    | {3}   | {4}    |".format(js_tests[0], js_tests[4] , js_tests[1], js_tests[2], js_tests[3]))
print ("+------+---------------+--------+------+------+-----+------+\n\n")


if py_tests[1] or js_tests[1]:
    error_code = 1

if error_code:
    print("FAILURE(S) have occurred!")
else:
    print("[All tests PASSED!]")
exit(error_code);
