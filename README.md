# ✨ Funter - Forms Hunter

Funter tool extract all forms and inputs found in a list of urls.

## ⭐ Features

## 💥 Key Benefits


# 💻 Install


## Virtual environment

```
sudo apt install python3-venv
```

To create a python virtual environment:
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Setup

Install requirements:
```
chmod +x setup/setup.sh
sudo bash setup/setup.sh
```

# 🎓 Usage

First start the docker database server:
```
cd setup
sudo bash server.sh
```

### Example 1 - Url

```
python3 funter.py -u https://www.google.com -o outputs/output.csv -v
```

### Example 2 - File with list of urls

```
python3 funter.py -U data/urls.txt -o outputs/output.csv -v
```

### Example 3 - Just reset database

```
python3 funter.py -r
```

## Tool options

Directory            | Description
---------------------|------------
-u                   | Url to scrape
-U                   | List of urls to scrape (url.txt)
-o                   | Dump form documents to CSV file
-r                   | Reset database to defaults
-v                   | Verbose

## Access to DB data

To manage the obtained data you can access to the database, for example, with:

[https://dbgate.org/](https://dbgate.org/)

DB credentials in project `.env` file.

![Database data](/images/database_data.png)


# 🛠️ Configuration

You can change the output formats and other settings through the [config.yaml](config%2Fconfig.yaml)  file.


# 💬 Change Log

- **25/06/2023** - XNP v1.0.0
  - New tool name "Funter".
  - New "config.yaml" file configuration.
  - Refactored code.
  - Added a module for automatic version checking and updating. XtremeNmapParser will now check if it's running the latest version at startup and update itself if a new version is available.


# 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

# 🎉 Let's Get Social!

* **Website:** [https://xtormin.com](https://xtormin.com)
* **Linkedin:** [https://www.linkedin.com/in/xtormin/](https://www.linkedin.com/in/xtormin/).
* **Twitter:** [https://twitter.com/xtormin](https://twitter.com/xtormin).
* **Youtube:** [https://www.youtube.com/channel/UCZs7q5QeyXS5YmUq6lexozw](https://www.youtube.com/channel/UCZs7q5QeyXS5YmUq6lexozw).
* **Instagram:** [https://www.instagram.com/xtormin/](https://www.instagram.com/xtormin/).