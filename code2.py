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
    val_records = list()
    inval_records = list()
    inval_records.append(records[0])
    val_records.append(records[0])
    for x in range(1, len(records)):
        # validation for EMPLOYEE_ID column datatype
        a = records[x].split(',')
        if len(a) != len(fields):
            c = False
            print('file validation failure for number of columns at: ' + str(x + 1))
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


data = open(source + filename).read()
config = json.loads(open(os.getcwd() + '/Config_2.json').read())
val_records, inval_records = validate_data(data, config)
# print(val_records)
# print(inval_records)
x=open(target+filename, 'w')
x.write('\n'.join(val_records))
x.close()
y=open(error_path+filename, 'w')
y.write('\n'.join(inval_records))
y.close()