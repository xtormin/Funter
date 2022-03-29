import os
import csv
import sys
import json
import logging
from utils.colors import colors as c


def write_csv(csv_filename, header, data):
    with open(csv_filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter = ";")
        writer.writerow(header)
        for d in data:
            writer.writerow(d)

def read_file(filename):
    try:
        with open(filename) as f: lines = f.read()
        return lines
    except Exception as e:
        logging.error(e)
        return None

def write_file(content, filename):
    f = open(filename, "w")
    f.write(content)
    f.close()

def write_json_file(filename, content):
    try:
        with open(filename, "w") as outfile: json.dump(content, outfile)
    except Exception as e:
        logging.erro(f"|-| Error writing output to {filename} file")
        logging.error(e)
        pass

def read_filelines(filename):
    try:
        with open(filename) as f: lines = f.readlines()
        return lines
    except Exception as e:
        print("|-| Error reading file...")
        logging.error(e)
        return None

def write_output_to_json_file(output, output_filename):
    # Convert dict to json
    output = json.dumps(output)
    output_json_file = f"{output_filename}.json"

    write_json_file(output_json_file, output)

def write_db_data_to_csv(data, csv_filename):
    headers = ["url", "action", "method", "type", "name", "value"]
    write_csv(csv_filename, headers, data)
    return csv_filename

def get_all_data(sess, Url, Form, Input):
    all_urls_from_db = sess.query(Url)
    all_forms_from_db = sess.query(Form)
    all_inputs_from_db = sess.query(Input)

    alldata = []
    for u in all_urls_from_db:
        for f in all_forms_from_db:
            for i in all_inputs_from_db:
                if u.id == f.id_url:
                    if f.id == i.id_form:
                        alldata.append([u.url, f.action,f.method,i.type,i.name,i.value])
    return alldata

# Program interruption
def programInterruption():
    print("\n\n" + c.RED + f' Program Interrupted ... Bye! 8) ' + c.END)
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)