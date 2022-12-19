import json
import os
import shutil
import time
import pandas as pd
from behave import *
import random
from datetime import datetime


@Given('file is placed in source folder for "{scenario_param}" with pandas')
def step_impl(context, scenario_param):
    time.sleep(4)
    scenario, fieldname, datatype = scenario_param.split('|')[0], scenario_param.split('|')[1], \
                                    scenario_param.split('|')[2]
    print(scenario)
    context.source_path = os.getcwd() + '/file_transfer/Source/'
    context.target_path = os.getcwd() + '/file_transfer/Target/'
    context.error_path = os.getcwd() + '/file_transfer/Error/'
    context.validation = os.getcwd() + '/file_transfer/Validation/'
    context.processed = os.getcwd() + '/file_transfer/Processed/'
    # context.config = json.loads(open(os.getcwd() + '/Config.json').read())
    # validate if source and Target folders are empty
    if os.listdir(context.source_path):
        for x in os.listdir(context.source_path):
            os.remove(context.source_path + x)
    # if os.listdir(context.target_path) != []:
    #     for x in os.listdir(context.target_path):
    #         os.remove(context.target_path + x)
    if os.listdir(context.validation):
        for x in os.listdir(context.validation):
            os.remove(context.validation + x)
    if os.listdir(context.error_path):
        for x in os.listdir(context.error_path):
            os.remove(context.error_path + x)
    context.input_data = pd.read_csv(os.getcwd() + '/data/employees.csv')
    context.error_data = pd.DataFrame(columns=context.input_data.columns)
    context.valid_data = context.input_data
    # config = json.loads(open(os.getcwd() + '/Config.json').read())
    index = random.randint(0, len(context.input_data) - 1)
    print(context.input_data.iloc[index])
    a = context.input_data.iloc[index]
    if scenario == 'invalid datatype':
        if fieldname in ['EMPLOYEE_ID', 'SALARY', 'MANAGER_ID', 'DEPARTMENT_ID']:
            a[fieldname] = 'abc'
        elif fieldname in ['FIRST_NAME', 'LAST_NAME', 'EMAIL', 'JOB_ID', 'HIRE_DATE']:
            a[fieldname] = 123
        context.input_data.iloc[index] = a
        context.error_data = context.error_data.append(a)
        context.valid_data.drop(index=index, inplace=True)
    elif scenario == 'incorrect record length':
        context.input_data['new_field'] = 'abc'
        context.error_data = context.error_data.append(context.input_data)
        context.valid_data = pd.DataFrame(columns=context.input_data.columns)
    elif scenario == 'null check':
        a[fieldname] = ''
        context.input_data.iloc[index] = a
        context.error_data = context.error_data.append(a)
        context.valid_data.drop(index=index, inplace=True)
    elif scenario == 'duplicate':
        context.input_data = context.input_data.append(context.input_data.iloc[index])
        context.error_data = context.error_data.append(context.input_data)
        context.valid_data = pd.DataFrame(columns=context.input_data.columns)
    elif scenario == 'new delta':
        a['EMPLOYEE_ID'] = random.randint(250, 500)
        context.input_data = context.input_data.append(a)
        context.valid_data = context.valid_data.append(a)
    elif scenario == 'update delta':
        if fieldname in ['SALARY', 'MANAGER_ID', 'DEPARTMENT_ID']:
            a[fieldname] = 123
        elif fieldname in ['FIRST_NAME', 'LAST_NAME', 'EMAIL', 'JOB_ID']:
            a[fieldname] = 'abc'
        context.input_data.iloc[index] = a
        context.valid_data.iloc[index] = a
    elif scenario == 'delete delta':
        context.input_data.drop(index=index, inplace=True)
        # context.valid_data.drop(index=index, inplace=True)
    context.valid_data.reset_index(inplace=True, drop=True)
    context.error_data.reset_index(inplace=True, drop=True)
    context.input_data.to_csv(context.source_path + 'employees.csv', sep=',', index=False)
    assert 'employees.csv' in os.listdir(os.getcwd() + '/file_transfer/Source/')


@When('"{file}" code is executed with pandas')
def step_impl(context, file):
    context.load_type = file
    if file == 'code4_delta.py':
        context.target_data_prev = pd.read_csv(context.target_path + 'employees.csv')
        context.target_data_prev.PHONE_NUMBER = context.target_data_prev.PHONE_NUMBER.astype('str', )
    os.system('python ' + file)


@Then('Validate if "{data_type}" data is moved to "{folder_name}" folder with pandas')
def step_impl(context, data_type, folder_name):
    if data_type == 'valid':
        x = pd.read_csv(context.validation + 'employees.csv')
        # print(context.valid_data.to_json(orient='index'))
        # a=open('a.txt', 'w')
        # a.write(context.valid_data.to_json(orient='index'))
        # a.close()
        # print(x.to_json(orient='index'))
        # b = open('b.txt', 'w')
        # b.write(x.to_json(orient='index'))
        # b.close()
        if x.to_json(orient='index') == context.valid_data.to_json(orient='index'):
            assert True
        else:
            assert False
    else:
        x = pd.read_csv(context.error_path + 'employees.csv')
        if x.to_json(orient='index') == context.error_data.to_json(orient='index'):
            assert True
        else:
            assert False


def func(var):
    return var.replace('.', '')


def func2(var):
    var = datetime.strptime(var, '%d-%b-%y').strftime('%d-%m-%Y')
    return var


@Then('validate if transformed data file is created in "{folder_name}" folder with pandas')
def step_impl(context, folder_name):
    validation_data = pd.read_csv(context.validation + 'employees.csv')
    validation_data['PACKAGE'] = validation_data['SALARY'] * 12
    validation_data['PHONE_NUMBER'] = validation_data['PHONE_NUMBER'].apply(func=func)
    validation_data['HIRE_DATE'] = validation_data['HIRE_DATE'].apply(func=func2)
    target_data = pd.read_csv(context.target_path + 'employees.csv')
    target_data.PHONE_NUMBER = target_data.PHONE_NUMBER.astype('str', )
    if context.load_type == 'code4_initial.py':
        initial = open(os.getcwd() + '/file_transfer/initial.txt').read()

        if len(validation_data) != len(target_data):
            assert False
        else:

            validation_data['START_DATE'] = initial
            validation_data['END_DATE'] = datetime.strptime('31-12-9999', '%d-%m-%Y').strftime('%d-%m-%Y %f')
            validation_data['CURENT_FLAG'] = 'Y'
            # a = open('a.txt', 'w')
            # a.write(validation_data.to_json(orient='index'))
            # a.close()
            # b = open('b.txt', 'w')
            # b.write(target_data.to_json(orient='index'))
            # b.close()
            if validation_data.to_json(orient='index') == target_data.to_json(orient='index'):
                validation_data.sort_values(by=['EMPLOYEE_ID', 'END_DATE', 'CURENT_FLAG'], inplace=True,
                                            ignore_index=False)
                validation_data.reset_index(drop=True, inplace=True)
                context.target_out = validation_data
                assert True
            else:
                assert False
    elif context.load_type == "code4_delta.py":
        delta = open(os.getcwd() + '/file_transfer/delta.txt').read()
        # context.target_data_prev
        # x = context.target_data_prev[context.target_data_prev['CURENT_FLAG'] == 'Y'][
        #     ["EMPLOYEE_ID", "FIRST_NAME", "LAST_NAME", "EMAIL", "PHONE_NUMBER", "HIRE_DATE", "JOB_ID", "SALARY",
        #      "COMMISSION_PCT", "MANAGER_ID", "DEPARTMENT_ID"]]
        w = context.target_data_prev[context.target_data_prev['CURENT_FLAG'] == 'N']
        x = context.target_data_prev[context.target_data_prev['CURENT_FLAG'] == 'Y']
        y = validation_data
        zz = x.merge(y, how='outer',
                     on=["EMPLOYEE_ID", "FIRST_NAME", "LAST_NAME", "EMAIL", "PHONE_NUMBER",
                         "HIRE_DATE", "JOB_ID",
                         "SALARY", "COMMISSION_PCT", "MANAGER_ID", "DEPARTMENT_ID", "PACKAGE"],
                     indicator=True)
        zz1 = zz[zz['_merge'] == 'left_only']
        zz2 = zz[zz['_merge'] == 'right_only']

        t = set(zz1['EMPLOYEE_ID']).intersection(zz2['EMPLOYEE_ID'])
        zz3 = zz1[zz1['EMPLOYEE_ID'].isin(t)]
        zz3.END_DATE = delta
        zz3.CURENT_FLAG = 'N'
        t1 = set(zz1['EMPLOYEE_ID']).difference(zz2['EMPLOYEE_ID'])
        zz4 = zz1[(zz1['EMPLOYEE_ID'].isin(t1)) & (zz1['END_DATE'] == '31-12-9999 000000')]
        zz4.END_DATE = delta
        zz4 = zz4.append(zz1[(zz1['EMPLOYEE_ID'].isin(t1)) & (zz1['END_DATE'] != '31-12-9999 000000')],
                         ignore_index=True)
        zz2.START_DATE = delta
        zz2.END_DATE = '31-12-9999 000000'
        zz2.CURENT_FLAG = 'Y'
        zz5 = zz[zz['_merge'] == 'both']
        zz6 = zz5.append(zz4, ignore_index=True).append(zz3, ignore_index=True).append(zz2, ignore_index=True).append(w,
                                                                                                                      ignore_index=True)
        zz6.drop(columns='_merge', inplace=True)

        zz6.sort_values(by=['EMPLOYEE_ID', 'END_DATE', 'CURENT_FLAG'], inplace=True, ignore_index=False)
        zz6.reset_index(drop=True, inplace=True)
        zz6.to_csv('abc.csv')
        context.target_out = zz6

        # z = x.merge(y, how='outer', on='EMPLOYEE_ID')
        # # new records
        # z1 = z[z.FIRST_NAME_x.isnull()][
        #     ["EMPLOYEE_ID", "FIRST_NAME_y", "LAST_NAME_y", "EMAIL_y", "PHONE_NUMBER_y", "HIRE_DATE_y", "JOB_ID_y",
        #      "SALARY_y", "COMMISSION_PCT_y", "MANAGER_ID_y", "DEPARTMENT_ID_y", "PACKAGE_y"]]
        # z1.rename(columns={'EMPLOYEE_ID': 'EMPLOYEE_ID', 'FIRST_NAME_y': 'FIRST_NAME', 'LAST_NAME_y': 'LAST_NAME',
        #                    'EMAIL_y': 'EMAIL', 'PHONE_NUMBER_y': 'PHONE_NUMBER', 'HIRE_DATE_y': 'HIRE_DATE',
        #                    'JOB_ID_y': 'JOB_ID', 'SALARY_y': 'SALARY', 'COMMISSION_PCT_y': 'COMMISSION_PCT',
        #                    'MANAGER_ID_y': 'MANAGER_ID', 'DEPARTMENT_ID_y': 'DEPARTMENT_ID', 'PACKAGE_y': 'PACKAGE'}, inplace=True)
        #
        # z1['START_DATE'] = delta
        # z1['END_DATE'] = datetime.strptime('31-12-9999', '%d-%m-%Y').strftime('%d-%m-%Y %f')
        # z1['CURENT_FLAG'] = 'Y'
        # # delete records
        #
        # z2 = z[z.FIRST_NAME_y.isnull()][
        #     ["EMPLOYEE_ID", "FIRST_NAME_x", "LAST_NAME_x", "EMAIL_x", "PHONE_NUMBER_x", "HIRE_DATE_x", "JOB_ID_x",
        #      "SALARY_x", "COMMISSION_PCT_x", "MANAGER_ID_x", "DEPARTMENT_ID_x", "PACKAGE_x", "START_DATE", "END_DATE",
        #      "CURENT_FLAG"]]
        # z2.rename(columns={'EMPLOYEE_ID': 'EMPLOYEE_ID', 'FIRST_NAME_x': 'FIRST_NAME', 'LAST_NAME_x': 'LAST_NAME',
        #                    'EMAIL_x': 'EMAIL', 'PHONE_NUMBER_x': 'PHONE_NUMBER', 'HIRE_DATE_x': 'HIRE_DATE',
        #                    'JOB_ID_x': 'JOB_ID', 'SALARY_x': 'SALARY', 'COMMISSION_PCT_x': 'COMMISSION_PCT',
        #                    'MANAGER_ID_x': 'MANAGER_ID', 'DEPARTMENT_ID_x': 'DEPARTMENT_ID', 'PACKAGE_x': 'PACKAGE'}, inplace=True)
        # z2["END_DATE"] = delta
        #
        # # update records
        # # z3 = z[(z.FIRST_NAME_x.notnull()) & (z.FIRST_NAME_y.notnull())]
        #
        # z3 = context.target_data_prev.merge(y, how='outer',
        #                                     on=["EMPLOYEE_ID", "FIRST_NAME", "LAST_NAME", "EMAIL", "PHONE_NUMBER",
        #                                         "HIRE_DATE", "JOB_ID",
        #                                         "SALARY", "COMMISSION_PCT", "MANAGER_ID", "DEPARTMENT_ID", ""])
        # z4 = z3[z3.CURENT_FLAG.isnull()]
        # z4.loc[:,'START_DATE'] = delta
        # z4.loc[:,'END_DATE'] = datetime.strptime('31-12-9999', '%d-%m-%Y').strftime('%d-%m-%Y %f')
        # z4.loc[:,'CURENT_FLAG'] = 'Y'
        # for y in z4.EMPLOYEE_ID:
        #     x = z3[(z3['EMPLOYEE_ID'] == y) & (z3['CURENT_FLAG'] == 'Y')]
        #
        #     x['END_DATE'] = delta
        #     x['CURENT_FLAG'] = 'N'
        #     z4 = z4.append(x)
        #     z3.drop(x.index, inplace=True)
        # z4 = z4.append(z3[z3.CURENT_FLAG.notnull()])
        # z1=z1.append(z2)
        # z4=z4.append(z1)
        # z4.sort_values(by=['EMPLOYEE_ID', 'CURENT_FLAG'], inplace=True, ignore_index=False)
        # z4.reset_index(drop=True, inplace=True)
        target_data.sort_values(by=['EMPLOYEE_ID', 'END_DATE', 'CURENT_FLAG'], inplace=True, ignore_index=False)
        target_data.reset_index(drop=True, inplace=True)
        target_data.to_csv('abc1.csv')
        if zz6.to_json(orient='index') == target_data.to_json(orient='index'):
            assert True
        else:
            assert False


@Then('validate if processed data file is created in "{folder_name}" folder with pandas')
def step_impl(context, folder_name):
    data = json.loads(open(context.processed + 'employees.json').read())
    data_active = pd.DataFrame(data["active_employees"])
    data_active.PHONE_NUMBER = data_active.PHONE_NUMBER.astype('str', )
    data_active.sort_values(by=['EMPLOYEE_ID', 'END_DATE', 'CURENT_FLAG'], inplace=True, ignore_index=False)
    data_active.reset_index(drop=True, inplace=True)
    data_inactive = pd.DataFrame(data["inactive_employees"])
    if not data_inactive.empty:
        data_inactive.PHONE_NUMBER = data_inactive.PHONE_NUMBER.astype('str', )
        data_inactive.sort_values(by=['EMPLOYEE_ID', 'END_DATE', 'CURENT_FLAG'], inplace=True, ignore_index=False)
        data_inactive.reset_index(drop=True, inplace=True)
    df = context.target_out
    df_active = df[df['END_DATE'] == '31-12-9999 000000']
    df_inactive = df[(df['END_DATE'] != '31-12-9999 000000') & (df['CURENT_FLAG'] == 'Y')]

    file = open('abc1.json', 'w')
    file.write(json.dumps(json.loads(data_inactive.to_json(orient='records')), indent=2))
    file.close()
    file = open('abc.json', 'w')
    file.write(json.dumps(json.loads(df_inactive.to_json(orient='records')), indent=2))
    file.close()
    # if (json.loads(data_active.to_json(orient='records')) == json.loads(df_active.to_json(orient='records'))):
    if ((json.loads(data_active.to_json(orient='records')) == json.loads(df_active.to_json(orient='records'))) and (
            json.loads(data_inactive.to_json(orient='records')) == json.loads(
        df_inactive.to_json(orient='records')))):
        assert True
    else:
        assert False


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
    if os.listdir(context.source_path):
        for x in os.listdir(context.source_path):
            os.remove(context.source_path + x)
    if os.listdir(context.target_path):
        for x in os.listdir(context.target_path):
            os.remove(context.target_path + x)
    if os.listdir(context.validation):
        for x in os.listdir(context.validation):
            os.remove(context.validation + x)
    if os.listdir(context.error_path):
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
