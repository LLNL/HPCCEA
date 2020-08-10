# Installation steps

*Note: Some of these documentation pages can only be accessed with a LLNL VPN*

## Install Dependencies
[Documentation](https://lc.llnl.gov/confluence/display/HPCCEA/Dependencies)
- To Install Genders: byac, flex, gcc-c++, python-devel (for python2), and python3-devel (for python3)
- Install pip3
- Python Packages: os, mysql.connector, numpy (delete?), sys, wheel

## Install py-hostlist 
[Repository](https://github.com/LLNL/py-hostlist) | [Documentation](https://py-hostlist.readthedocs.io/en/latest/index.html)

- Our Modified Steps
    - `git clone https://github.com/llnl/py-hostlist.git`
    - `cd py-hostlist`
    - `python3 setup.py sdist bdist_wheel`
    - `pip3 install dist/py_hostlist-0.0.1.dev0-py2.py3-none-any.whl`
    - NOTE: *need to copy `/py-hostlist/hostlist/hostlist.py` into the library directory

## Install Genders with Python3
[Documentation](https://lc.llnl.gov/confluence/display/HPCCEA/Genders+Installation+with+Python3)
- `export PYTHON = /usr/bin/python3` (or wherever python3 is stored using `which python3`)
- configure without any extensions other than python
   - `./configure –with-perl-extensions=no –with-python-extensions=yes –with-cplusplus-extensions=no –with-java-extensions=no`
- follow the remaining instructions in the genders INSTALLATION document

## pip install link (might need to change this) 
- copy the link from PyPi and install the package

## mySQL server set up 

#### Dependencies 
1. download MySQL repositories: `sudo wget https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm`
2. prepare the repository: `sudo rpm -Uvh mysql80-community-release-el7-3.noarch.rpm`
3. install MySQL: `sudo yum install mysql-server`
4. start MySQL: `sudo systemctl start mysqld`
5. check status: `sudo systemctl status mysqld: copy mysqld.service path`
6. add export path statement to end of .bash_profile file

#### Password set up 
1. `grep 'temporary password' /var/log/mysqld.log`
2. copy password
3. `mysql -u root -p`
4. enter copied password 
5. `SET GLOBAL validate_password.policy=LOW;`
6. exit mySQL server
7. `run python3 -m centralgendersdatabase --password` 
8. This will promt you to add in the offical password 
9. Now tool can be run "passwordlessly" by all users 


