import os
import shutil
import json

filename = os.listdir(os.getcwd() + '/file_transfer/Source/')[0]
source = os.getcwd() + '/file_transfer/Source/'
target = os.getcwd() + '/file_transfer/Target/'
error_path = os.getcwd() + '/file_transfer/Error/'


def file_transfer(source, target, filename):
    shutil.move(source + filename, target)


def validate_data(data, config):
    records = data.split('\n')
    fields = list(config.keys())
    c = bool()
    d = int()
    for x in range(1, len(records)):
        # validation for EMPLOYEE_ID column datatype
        a = records[x].split(',')
        if len(a) != len(fields):
            c = False
            print('file validation failure for number of columns at: ' + str(x + 1))
            break
        int_columns = ['EMPLOYEE_ID', 'SALARY', 'MANAGER_ID', 'DEPARTMENT_ID']
        str_columns = ['FIRST_NAME', 'LAST_NAME', 'EMAIL', 'PHONE_NUMBER', 'HIRE_DATE', 'JOB_ID',
                       'COMMISSION_PCT']
        for y in fields:
            if y in int_columns:
                try:
                    b = int(a[config[y]])
                    c = True
                    continue
                except:
                    c = False
                    print('file validation failure for invalid datatype ' + y + ' column at: ' + str(x + 1))
                    break

            elif y in str_columns:
                # validation for FIRST_NAME column datatype
                try:
                    b = int(a[config[y]])
                    c = False
                    print('file validation failure for invalid datatype ' + y + ' column at: ' + str(x + 1))
                    break
                except:
                    c = True
                    continue
        if not c:
            break

    return c


data = open(source + filename).read()
config = json.loads(open(os.getcwd() + '/Config.json').read())
if validate_data(data, config):
    file_transfer(source, target, filename)
else:
    file_transfer(source, error_path, filename)
    assert True
