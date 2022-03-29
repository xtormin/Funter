import sys
import json
import logging
from subprocess import call
from json2html import *
from utils import banner
from bs4 import BeautifulSoup
from app.models import *
from utils import cli,functions as func
from utils.colors import colors as c
from requests_html import HTMLSession
from app.db import Session, Base, engine, add_item_to_items_table, check_if_row_exists

# SESSIONS
session = HTMLSession()
sess = Session()

# LOGGING
logger = logging.getLogger()

logger.setLevel(logging.ERROR)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.disabled = True


# FUNCTIONS

def get_forms(session, url):
    try:
        res = session.get(url)
        soup = BeautifulSoup(res.html.html, "html.parser")
        return soup.find_all("form")
    except Exception as e:
        logger.error(e)

def get_inputs_from_form(form, url_to_db):
    details = {}

    action = form.attrs.get("action")#.lower()
    method = form.attrs.get("method", "get").lower()

    # Save form data to db
    form_to_db = Form(action=action, method=method, id_url=url_to_db.id)
    add_item_to_items_table(sess, form_to_db)

    # Get Input's data
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value =input_tag.attrs.get("value", "")

        inputs.append({"type": input_type, "name": input_name, "value": input_value})

        # Save input data to db
        input_to_db = Input(type=input_type, name=input_name, value=input_value, id_form=form_to_db.id)
        
        #db_data = func.get_all_data(sess, Url, Form, Input)
        #print(db_data)
        #row_complete = [url_to_db.url, form_to_db.action, form_to_db.method, input_to_db.type, input_to_db]
        
        add_item_to_items_table(sess, input_to_db)
    
    # Get Select's data
    for select in form.find_all("select"):
        select_name = select.attrs.get("name")
        select_type = "select"
        select_options = []
        select_default_value = ""

        for select_option in select.find_all("option"):
            option_value = select_option.attrs.get("value")
            if option_value:
                select_options.append(option_value)
                if select_option.attrs.get("selected"):
                    select_default_value = option_value
        if not select_default_value and select_options:
            select_default_value = select_options[0]

        inputs.append({"type": select_type, "name": select_name, "values": select_options, "value": select_default_value})

    # Get Textarea's data
    for textarea in form.find_all("textarea"):
        textarea_name = textarea.attrs.get("name")
        textarea_type = "textarea"
        textarea_value = textarea.attrs.get("value", "")

        inputs.append({"type": textarea_type, "name": textarea_name, "value": textarea_value})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def get_forms_from_url(weblist):
    output = {}
    data = {}

    for i, url in enumerate(weblist, start=1):
        url = url.replace('\n','')
        # Save url data to db
        url_to_db = Url(url=url)
        add_item_to_items_table(sess, url_to_db)

        # Get forms from a url
        forms = get_forms(session, url)

        # If no forms were found, continue with the next URL
        if forms == [] or forms == None: continue

        # Show all forms found and his inputs
        print("\n\n" + c.GREEN + f' URL >>> {url}' + c.END)
        # Add a dict with the information of each form
        allforms = {}
        for z, form in enumerate(forms, start=1):
            form_details = get_inputs_from_form(form, url_to_db)
            print("\n" + c.CYAN + "-"*3, f"FORM #{z}" + c.END)
            allforms[z] = form_details
            data = {'url': url, 'forms': allforms}
            output[i] = data

            # Print forms data
            print(data)

    return output


# MAIN FUNCTION

def run():
    try:
        banner.ascii()
        args = cli.get()

        if args.resetdata: 
            aux = input("The '-r' options will delete all obtained data saved in formshunterdb. Are you sure? (y/n): ") 
            if aux == 'y' or aux == 'Y':
                Base.metadata.drop_all(bind=engine, tables=[Project.__table__, Scope.__table__, Url.__table__, Form.__table__, Input.__table__])
                print("\n" + c.GREEN + "|+| Data deleted" + c.END)
                sys.exit(0)

        # List of URLs to analyze
        weblist = func.read_filelines(args.urlslist[0])
        if not weblist: sys.exit(0)

        get_forms_from_url(weblist)

        db_data = func.get_all_data(sess, Url, Form, Input)

        # If output flag exists the data will be written to a csv file
        if args.outputfile: 
            output_filename = args.outputfile
            func.write_db_data_to_csv(db_data, output_filename)
        else: pass

        if args.showweb:
            print("\n\n" + c.GREEN + f' |+| Initilizing website... ' + c.END)
            rc = call("./launch-web.sh", shell=True)
    except KeyboardInterrupt:
        func.programInterruption()
