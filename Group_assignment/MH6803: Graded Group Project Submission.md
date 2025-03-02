# MH6803: Graded Group Project Submission

## **Program Prerequisite**

### **Windows**
```sh
# Install Python
winget install Python.Python.3.11

# Install pip (if not already installed)
python -m ensurepip --default-pip

# Install CustomTkinter
pip install customtkinter

# Install mplfinance 
pip install mplfinanceI

```

### **macOS**
```sh
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3

# Install pip (if not installed)
pip3 install --upgrade pip

# Install CustomTkinter
pip3 install customtkinter
```

### **CustomTkinter Documentation**
[CustomTkinter Website](https://customtkinter.tomschimansky.com/)

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