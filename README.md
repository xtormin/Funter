# FORMS HUNTER

This tool hunts all forms and inputs found in a list of urls.

## Install

Create a postgresql docker container and install python requirements:
```
bash setup/setup.sh
bash setup/server.sh
```

## Execution

Execute the script with the list of urls as target and launch the web with the obtained data.
```
python3 formshunter.py -U data/urls.txt -s
```

![Forms displayed on the website](/images/webdata.png)

### Options

Directory            | Description
---------------------|------------
-U                   | File with the list of urls
-o                   | Output file
-s                   | Launch a website to visualize obtained data
-r                   | Reset database to defaults


Reset database data.
```
python3 formshunter.py -r
```

Execute the script with the list of urls as target and launch the web with the obtained data and save the output to a CSV file.
```
python3 formshunter.py -U data/urls.txt -s
```

### Visualize in website

Launch the website:
```
bash launch-web.sh
```

## Access to DB data

To manage the obtained data you can access to the database with:

[https://www.beekeeperstudio.io/](https://www.beekeeperstudio.io/)

DB connection:

- Port: `5434`
- Password: `secret`

![Beekeeper DB connection](/images/beekeeper_config.png)

# Accounts

* Linkedin: [https://www.linkedin.com/in/xtormin/](https://www.linkedin.com/in/xtormin/).
* Twitter: [https://twitter.com/xtormin](https://twitter.com/xtormin).
* Youtube: [https://www.youtube.com/channel/UCZs7q5QeyXS5YmUq6lexozw](https://www.youtube.com/channel/UCZs7q5QeyXS5YmUq6lexozw).
* Instagram: [https://www.instagram.com/xtormin/](https://www.instagram.com/xtormin/).