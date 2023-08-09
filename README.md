# campUS
Simple Feedback Web to Connect Students with Lecturers Based on Python FLASK

![image](https://github.com/YuukioFuyu/campUS/assets/79379934/06decb16-9d05-4eed-ad16-9be968e40a5d)
![image](https://github.com/YuukioFuyu/campUS/assets/79379934/6241d387-1949-4acb-a954-36be777bb717)

<hr>

## Dependency

-   Python3
-   PostgreSQL

## Pre-Installation

1. Clone this repository

```bash
git clone https://github.com/YuukioFuyu/campUS.git
```

2. Install python3 & venv

```bash
sudo dnf install python3 python3-venv
```

3. Install postgreSQL database

```bash
sudo dnf install postgresql14-server
```

4. Setup postgreSQL

```bash
sudo /usr/pgsql-14/bin/postgresql-14-setup initdb
```

5. Enable postgreSQL services

```bash
sudo systemctl enable --now postgresql-14
```

6. Create database

```bash
psql -U postgres
```
```bash
create database messages;
```
```bash
\q
```

7. Import database

```bash
psql -U postgres messages < messages.psql
```

## Installation

1. Create venv directory

```bash
python3 -m venv [path to venv]
```

2. Enable venv

```bash
source [path to venv]/bin/activate
```

3. Install requirements

```bash
pip install -r requirements.txt
```

4. Edit app.py

### Customise with your settings
- app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://[DATABASE USER]:[PASSWORD]@[IP SERVER]/[DATABASE NAME]'
- app.secret_key = 'YOUR SECRET KEY'

5. Save and exit app.py

6. Run the program

```bash
python3 ./app.py
```

7. Access via browser on localhost / http://127.0.0.1

<hr>

### Default Login:
#### Administrator
| Username | Password |
|  ------- | -------- |
|   admin  |   admin  |

#### Student 1
| Username | Password |
|  ------- | -------- |
|    mhs1  |    mhs1  |

#### Student 2
| Username | Password |
|  ------- | -------- |
|    mhs2  |    mhs2  |
