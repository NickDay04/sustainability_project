# Setup
For this project, you need **Python 3.10** interpreter and **Flask 3.0.3**.<br>

## Prerequisites
### Install the required components.

1. Install requirements.txt: via your IDE's terminal, navigate to the clone's root (CSC2033_TEAM08_23-24/), paste the following command & execute. 
```
pip install -r requirements.txt
```

2. Create the .env environment config file.
```
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_HOST=localhost
APP_DEBUGGING=True # boolean: toggle flask's debug mode.
```

3. Ensure that docker is installed!!!
4. Create and populate your MySQL database using docker if you are on a Linux machine:
```
./build_db.sh
python create_db.py
```
6. Or if you are on a Windows machine:
```
docker pull mysql/mysql-server:latest
docker run --name db -p 3306:3306 -e MYSQL_ROOT_HOST=% -e MYSQL_ROOT_PASSWORD=root -e MYSQL_USER=root -d mysql/mysql-server
python create_db.py
```
5. Now you are ready to go! Run the application by running `app.py`:
```
python app.py

