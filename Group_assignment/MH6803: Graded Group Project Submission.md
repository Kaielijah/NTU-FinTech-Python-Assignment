# MH6803: Graded Group Project Submission

## **Program Prerequisite**

### **Windows**
```sh
# Install Python
winget install Python.Python.3.11

# Install pip (if not already installed)
python -m ensurepip --default-pip

# Install dependencies
pip install -r requirements.txt

```

### **macOS**
```sh
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3

# Install pip (if not installed)
pip3 install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### **CustomTkinter Documentation**
[CustomTkinter Website](https://customtkinter.tomschimansky.com/)

### **Ctk Theme Builder**
[ctk-theme-builder](https://github.com/avalon60/ctk_theme_builder/wiki/Installing-&-Upgrading-CTk-Theme-Builder)
---

## **Summarise the Key Features of the Program**

### **Portfolio Management**
- Track and manage investment portfolios.
- View real-time and historical performance.
- Analyze asset allocation and portfolio risk.

### **Visualization & Historical Data Analysis**
- Generate pie chart and allocated assets.
- Fetch and analyze historical stock market trends.
- Compare asset performance over different time periods.

---

## **Commands to Test Program**

```sh
# Run the main application
python main.py#

# kill python jobs
disown
pkill -f python3

# Check installed dependencies
pip list

# Install python-tk
brew install python-tk
```
## **Commands to Troubleshoot SQL**

```sh

# Upgrade SQL
Upgrading from MySQL <8.4 to MySQL >9.0 requires running MySQL 8.4 first:
 - brew services stop mysql
 - brew install mysql@8.4
 - brew services start mysql@8.4
 - brew services stop mysql@8.4
 - brew services start mysql

To secure it run:
    mysql_secure_installation

MySQL is configured to only allow connections from localhost by default
To connect run:
    mysql -u root

# Troubleshooting for sql for logging issues due to authentication
# Stop all services 
brew services stop mysql
sudo pkill -9 mysql

# Enter safemode 
sudo mysqld_safe --skip-grant-tables --skip-networking &
--skip-grant-tables: Allows logging in without a password
--skip-networking: Ensures MySQL is not accessible remotely (security measure)

# Check error log
tail -n 50 /usr/local/var/mysql/*.err

# MySQL 8.4 Troubleshooting on macOS (Homebrew)

# Stop Any Running MySQL Processes**
# Before troubleshooting, ensure MySQL is completely stopped.
brew services stop mysql@8.4
sudo pkill -9 mysql
sudo pkill -9 mysqld_safe

# After stopping, verify that no MySQL processes are still active.
ps aux | grep mysql

# If you see a running mysqld process, kill it manually:
sudo kill -9 <PID>


# Remove Corrupted MySQL Data (Fix Downgrade Issue)
remove the MySQL data directory: 
sudo rm -rf /usr/local/var/mysql

# Reinitialize MySQL 8.4
# initialize MySQL manually:
sudo /usr/local/opt/mysql@8.4/bin/mysqld --initialize --user=mysql --datadir=/usr/local/var/mysql
# A temporary root password is generated (copy and save it).

# Start MySQL Properly
brew services restart mysql@8.4

# Verify that MySQL is running:
ps aux | grep mysql

# Log in to MySQL
mysql -u root -p

# Reset Root Password (If Needed)
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourNewSecurePassword';
FLUSH PRIVILEGES;
EXIT;

#Verify MySQL is Working
mysqladmin -u root -p version

## **Reset MySQL Root Password (If Forgotten)**
```sh
brew services stop mysql@8.4
sudo pkill -9 mysql
sudo /usr/local/opt/mysql@8.4/bin/mysqld_safe --skip-grant-tables --skip-networking &
mysql -u root

#Inside MySQL:
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourNewSecurePassword';
FLUSH PRIVILEGES;
EXIT;

#Then, restart MySQL:
sudo pkill -9 mysqld_safe
sudo pkill -9 mysql
brew services restart mysql@8.4

#Try logging in again:
mysql -u root -p
```sh
