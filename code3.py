import os
import shutil
import json

filename = os.listdir(os.getcwd() + '/file_transfer/Source/')[0]
source = os.getcwd() + '/file_transfer/Source/'
target = os.getcwd() + '/file_transfer/Target/'
validation = os.getcwd() + '/file_transfer/Validation/'
error_path = os.getcwd() + '/file_transfer/Error/'


def file_transfer(source, target, filename):
    shutil.move(source + filename, target)


def validate_data(data, config):
    records = data.split('\n')
    fields = list(config.keys())
    c = bool()
    d = int()
    val_records = list()
    inval_records = list()
    inval_records.append(records[0])
    val_records.append(records[0])
    # duplicate check
    if len(set(records)) != len(records):
        c = False
        print('file validation failure for duplicate records')
        # val_records=records[0]
        inval_records = records
        return val_records, inval_records

    for x in range(1, len(records)):
        # validation for EMPLOYEE_ID column datatype
        a = records[x].split(',')
        if len(a) != len(fields):
            c = False
            print('file validation failure for number of columns at: ' + str(x + 1))
            inval_records.append(records[x])
            continue

        if str(a[config['EMPLOYEE_ID']['index']]) == '':
            c = False
            print('file validation failure for null key value at: ' + str(x + 1))
            inval_records.append(records[x])
            continue

        for y in fields:
            if config[y]["dtype"] == "int":
                try:
                    # print()
                    b = int(a[config[y]["index"]])
                    c = True
                    continue
                except:
                    c = False
                    print('file validation failure for invalid datatype ' + y + ' column at: ' + str(x + 1))
                    break

            elif config[y]["dtype"] == "str":
                # validation for FIRST_NAME column datatype
                try:
                    b = int(a[config[y]["index"]])
                    c = False
                    print('file validation failure for invalid datatype ' + y + ' column at: ' + str(x + 1))
                    break
                except:
                    c = True
                    continue
        if c:
            val_records.append(records[x])
        else:
            inval_records.append(records[x])

    return val_records, inval_records


def transform_data(data, config):
    data[0] = data[0] + ",PACKAGE"
    for x in range(1, len(data)):
        record = data[x].split(',')
        package=int(record[config['SALARY']['index']])*12
        record.append(str(package))
        record[config['PHONE_NUMBER']['index']]=record[config['PHONE_NUMBER']['index']].replace('.', '')
        data[x]=','.join(record)
    return data

# reading data from source file
data = open(source + filename).read()
# reading configuration file
config = json.loads(open(os.getcwd() + '/Config_2.json').read())
# perform validations on source data
val_records, inval_records = validate_data(data, config)
x = open(validation + filename, 'w')
x.write('\n'.join(val_records))
x.close()
y = open(error_path + filename, 'w')
y.write('\n'.join(inval_records))
y.close()
# perform transformations on valid records
processed_data=transform_data(val_records, config)


z = open(target + filename, 'w')
z.write('\n'.join(processed_data))
z.close()

