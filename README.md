# FORMS HUNTER

This tool hunts all forms and inputs found in a list of urls.

## Virtual environment

To create a python virtual environment:
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r setup/requirements.txt
```

## Install

Install requirements:
```
cd setup
chmod +x setup.sh
bash setup.sh
```

## Execution

First start the docker database server:
```
cd setup
bash server.sh
```


### Example 1 - Url

```
python3 formshunter.py -r -u https://www.google.com -o outputs/output.csv -v
```

- -r: Reset database
- -U: Search forms on url.
- -o: Dump 'form' document ("table") to CSV file.
- -v: Verbose.


![Command output](/images/formhunter_url_example.png)

### Example 2 - File with list of urls

```
python3 formshunter.py -r -U data/urls.txt -o outputs/output.csv -v
```

- -r: Reset database
- -U: Search forms on urls within urls.txt
- -o: Dump 'form' document ("table") to CSV file.
- -v: Verbose.

![Command output](/images/formhunter_file_example.png)

### Example 3 - Just reset database

```
python3 formshunter.py -r
```

- -r: Reset database

## Tool options

Directory            | Description
---------------------|------------
-u                   | Url to scrape
-u                   | List of urls to scrape (url.txt)
-o                   | Dump form documents to CSV file
-r                   | Reset database to defaults
-v                   | Verbose

## Access to DB data

To manage the obtained data you can access to the database, for example, with:

[https://dbgate.org/](https://dbgate.org/)

DB credentials in project `.env` file.

![Database data](/images/database_data.png)

# Accounts

* Linkedin: [https://www.linkedin.com/in/xtormin/](https://www.linkedin.com/in/xtormin/).
* Twitter: [https://twitter.com/xtormin](https://twitter.com/xtormin).
* Youtube: [https://www.youtube.com/channel/UCZs7q5QeyXS5YmUq6lexozw](https://www.youtube.com/channel/UCZs7q5QeyXS5YmUq6lexozw).
* Instagram: [https://www.instagram.com/xtormin/](https://www.instagram.com/xtormin/).