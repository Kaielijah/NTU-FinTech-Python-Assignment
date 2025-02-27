import matplotlib.pyplot as plt

def generate_pie_chart(portfolio):
    symbols = [asset['symbol'] for asset in portfolio]
    values = [asset['qty'] * asset['price'] for asset in portfolio]
    plt.pie(values, labels=symbols, autopct='%1.1f%%')
    plt.title("Portfolio Distribution")
    plt.show()
