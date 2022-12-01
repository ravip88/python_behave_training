import json
import os
import shutil
import time

from behave import *
import random
from datetime import datetime


@Given('file is placed in source folder for "{scenario_param}"')
def step_impl(context, scenario_param):
    time.sleep(4)
    scenario, fieldname, datatype = scenario_param.split('|')[0], scenario_param.split('|')[1], \
                                    scenario_param.split('|')[2]
    context.source_path = os.getcwd() + '/file_transfer/Source/'
    context.target_path = os.getcwd() + '/file_transfer/Target/'
    context.error_path = os.getcwd() + '/file_transfer/Error/'
    context.validation = os.getcwd() + '/file_transfer/Validation/'
    # context.config = json.loads(open(os.getcwd() + '/Config.json').read())
    # validate if source and Target folders are empty
    if os.listdir(context.source_path) != []:
        for x in os.listdir(context.source_path):
            os.remove(context.source_path + x)
    if os.listdir(context.target_path) != []:
        for x in os.listdir(context.target_path):
            os.remove(context.target_path + x)
    if os.listdir(context.validation) != []:
        for x in os.listdir(context.validation):
            os.remove(context.validation + x)
    if os.listdir(context.error_path) != []:
        for x in os.listdir(context.error_path):
            os.remove(context.error_path + x)

    # shutil.copy(os.getcwd() + '/data/employees.csv', os.getcwd() + '/file_transfer/Source/')
    context.input_data = open(os.getcwd() + '/data/employees.csv').read()
    config = json.loads(open(os.getcwd() + '/Config.json').read())
    records = context.input_data.split('\n')
    index = random.randint(1, len(records))
    print(records[index])
    fields = records[index].split(',')
    err_records = list()
    err_records.append(records[0])
    context.Config = config
    err_record = ''
    if scenario == 'invalid datatype':
        if fieldname in ['EMPLOYEE_ID', 'SALARY', 'MANAGER_ID', 'DEPARTMENT_ID']:
            if datatype == 'int':
                fields[config[fieldname]] = fields[config[fieldname]] + "abc"
                records[index] = ','.join(fields)
        elif fieldname in ['FIRST_NAME', 'LAST_NAME', 'EMAIL', 'JOB_ID', 'HIRE_DATE']:
            if datatype == 'str':
                fields[config[fieldname]] = '1234'
                records[index] = ','.join(fields)
        context.input_data = '\n'.join(records)
        x = open(os.getcwd() + '/file_transfer/Source/employees.csv', 'w')
        x.write(context.input_data)
        x.close()
        err_record = records.pop(index)
        err_records.append(err_record)
    elif scenario == 'incorrect record length':
        fields.append('abc')
        records[index] = ','.join(fields)
        context.input_data = '\n'.join(records)

        x = open(os.getcwd() + '/file_transfer/Source/employees.csv', 'w')
        x.write(context.input_data)
        x.close()
        err_record = records.pop(index)
        err_records.append(err_record)
    elif scenario == 'null check':
        fields[config[fieldname]] = ''
        records[index] = ','.join(fields)
        context.input_data = '\n'.join(records)
        x = open(os.getcwd() + '/file_transfer/Source/employees.csv', 'w')
        x.write(context.input_data)
        x.close()
        err_record = records.pop(index)
        err_records.append(err_record)

    elif scenario == 'duplicate':
        records.append(records[index])
        x = open(os.getcwd() + '/file_transfer/Source/employees.csv', 'w')
        context.input_data = '\n'.join(records)
        x.write(context.input_data)
        x.close()
        err_records = records
        records = list()
        records.append(err_records[0])

    else:
        x = open(os.getcwd() + '/file_transfer/Source/employees.csv', 'w')
        x.write(context.input_data)
        x.close()

    context.input_data_invalid = err_records
    context.input_data_valid = '\n'.join(records)
    assert 'employees.csv' in os.listdir(os.getcwd() + '/file_transfer/Source/')


@When('Dev2 code is executed')
def step_impl(context):
    os.system('python code2.py')


@When('Dev3 code is executed')
def step_impl(context):
    os.system('python code3.py')

@When('Dev4_initial code is executed')
def step_impl(context):
    os.system('python code4_initial.py')


@Then('file is moved to target folder')
def step_impl(context):
    assert 'employees.csv' in os.listdir(os.getcwd() + '/file_transfer/target/')


@Then('"{folder_name}" folder is empty')
def step_impl(context, folder_name):
    assert os.listdir(os.getcwd() + '/file_transfer/' + folder_name + '/') == []


@Then('file exists in "{folder_name}" folder')
def step_impl(context, folder_name):
    assert 'employees.csv' in os.listdir(os.getcwd() + '/file_transfer/' + folder_name + '/')


@Then('file name is correct')
def step_impl(context):
    assert 'employees.csv' == os.listdir(os.getcwd() + '/file_transfer/target/')[0]


@Then('data is correct and matching with the input file')
def step_impl(context):
    assert context.input_data == open(os.getcwd() + '/file_transfer/target/employees.csv').read()


@Then('Validate if "{data_type}" data is moved to "{folder_name}" folder')
def step_impl(context, data_type, folder_name):
    if data_type == 'valid':
        x = open(context.validation + 'employees.csv').read()
        if x == context.input_data_valid:
            assert True
        else:
            assert False
    else:
        x = open(context.error_path + 'employees.csv').read()
        if x.split('\n') == context.input_data_invalid:
            assert True
        else:
            assert False


@Then('validate if transformed data file is created in "{folder_name}" folder')
def step_impl(context, folder_name):
    validation_data = open(context.validation + 'employees.csv').read().split('\n')
    target_data = open(context.target_path + 'employees.csv').read().split('\n')
    initial = open(os.getcwd() + '/file_transfer/initial.txt').read()
    if len(validation_data) != len(target_data):
        assert False
    else:
        for x in range(1, len(validation_data)):
            validation_fields = validation_data[x].split(',')
            target_fields = target_data[x].split(',')
            if int(target_fields[11]) != int(validation_fields[context.Config['SALARY']]) * 12:
                assert False
            elif target_fields[context.Config['PHONE_NUMBER']] != validation_fields[
                context.Config['PHONE_NUMBER']].replace('.', ''):
                assert False
            elif target_fields[context.Config['HIRE_DATE']] != datetime.strptime(validation_fields[
                                                                                              context.Config[
                                                                                                  'HIRE_DATE']],
                                                                                          '%d-%b-%y').strftime(
                '%d-%m-%Y'):
                assert False
            elif target_fields[12] != initial:
                assert False
            elif target_fields[13] != datetime.strptime('31-12-9999', '%d-%m-%Y').strftime('%d-%m-%Y %f'):
                assert False
            elif target_fields[14] != 'Y':
                assert False

    assert True


@Given('ghi')
def step_impl(context):
    assert True


@When('jkl')
def step_impl(context):
    assert True


@Then('mno')
def step_impl(context):
    print("Hello")
    assert True


@Then('pqr')
def step_impl(context):
    assert True


@Given('ghi "{param}"')
def step_impl(context, param):
    print(int(param) + 10)
    assert True


@When('jkl "{param}"')
def step_impl(context, param):
    print(int(param) + 10)
    assert True


@Then('mno "{param}"')
def step_impl(context, param):
    print("Hello")
    print(int(param) + 10)
    a = int(param) + 10
    if a == 13:
        assert True
    else:
        assert False


@Then('pqr "{param}"')
def step_impl(context, param):
    print(int(param) + 10)
    assert True
