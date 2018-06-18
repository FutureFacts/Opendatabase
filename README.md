#Opendatabase
The script for filling and defining views on database containing open data (so far CBS data)

Data will be read into python with the cbsodata module.
Then the data will be read into the mariadb Database.

Log in to database should not be pushed to GitHub.


One should create a file called credentials.py containing
login = {
    'user' : 'Yourusername',
    'password' : 'Yourpassword'
}

database = {
    'host' : "URL to MariaDB database"
    'DB' : 'name of database'
}

