# campUS
Simple Feedback Web to Connect Students with Lecturers Based on Python FLASK

## Our Lecture
<td align="center" valign="top" width="30%"><a href="hepidad.github.io"><img src="https://media.licdn.com/dms/image/C5603AQE4A3WARH9imA/profile-displayphoto-shrink_800_800/0/1625544749335?e=2147483647&v=beta&t=959ypUT1L34lPjovI6cTMzWiRU3ljb3FfKHzYNX26rQ" width="300px;" alt="Irwan Kautsar"/><br /><sub><b>Irwan Kautsar</b></sub></a><br /><i>Back-End & Database</i></td>

## Our Team

<table>
  <tbody>
  </tbody>
    <tr>
      <td align="center" valign="top" width="30%"><a href="https://yuuki0.net"><img src="https://avatars.githubusercontent.com/u/79379934?v=4?s=100" width="300px;" alt="ゆうきお ふゆ"/><br /><sub><b>ゆうきお ふゆ</b></sub></a><br /><i>Back-End & Database</i></td>
      <td align="center" valign="top" width="30%"><a href="https://github.com/AlvitoDian"><img src="https://avatars.githubusercontent.com/u/132731944?v=4?s=100" width="300px;" alt="Alvito Dian Pratama Putra"/><br /><sub><b>Alvito Dian Pratama Putra</b></sub></a><br /><i>Back-End & Bug Hunter</i></td>
      <td align="center" valign="top" width="30%"><a href="https://github.com/rayhanantha"><img src="https://avatars.githubusercontent.com/u/111292920?v=4?s=100" width="300px;" alt="Rayhanantha Akbar Putra Prasetyo"/><br /><sub><b>Rayhanantha Akbar Putra Prasetyo</b></sub></a><br /><i>Front-End & UI/UX</i></td>
    </tr>
  </tbody>
</table>

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
