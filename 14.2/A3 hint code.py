#import modules

def user_input():

    #welcome user and select a function
    word = '''
Welcome to Stock Master!

Please select a function to continue:

(1) Search for a stock code by keyword
(2) View stock trend by code

(sample input 1 or 2)
'''
    next_word = '''
Would you like to
1. return to menu
2. exit program
(sample input : 1 or 2)
'''

    next_step = str(input(next_word))
    
    

    #TODO: 1. construct a loop according to the flowchart 1 given in the block manual
    #function = str(input(word))
    
def check_code():

    #ask user to input keyword
    input_keyword = input('Please input keyword for the stock searching for:')

    #get source data (code provided), the source data is stored in code_dic, a dictionary with all tickers' company name as key and stock code as value

    #filter out tickers containing user's keyword

    #ask for next step
    next_step = 'what is the next step?'

    #return
    return input_keyword,next_step

def view_trend():
    print("\n enter function view_trend()")
    #ask user to input stock code, start date and end date
    code = str(input('Please input the code of the stock requested:\n'))
    input_start = str(input('please enter start date (eg. 2019-1-1):'))
    input_end = str(input('please enter end date (eg. 2019-1-1):'))

    #convert string to datetime

    #get source data (code provided), the source data is stored in df, a pandas dataframe

    #ask for graph choice
    graph_choice = str(input('''
Please select type of graph.
(1) Candle Stick
(2) High
(3) Low
(4) Open
(5) Close
(6) Adj Close
(7) Moving Average
(8) Volume

You may select mutiple choices, seperate each choice by comma.

Sample input for candle stick + High + Volume:
1,2,8

'''))

    #manipulate choice input

    #draw graph based on input
    #TODO: 2. construct a branch according to flowchart 2 in lab manual

##    ma = int(input('''
##
##Please input the frequency for the moving average.
##
##Sample input for 100 days moving average:
##100
##'''))

    #ask for next step
    next_step = 'what is the next step?'

    #return
    return code,input_start,input_end,graph_choice,ma,next_step

def next_request():

    #ask user to select next step to proceed with
    next_word = '''
Would you like to
1. return to menu
2. exit program
(sample input : 1 or 2)
'''

    next_step = str(input(next_word))

    #return
    return next_word,next_step

def input_to_date(input_date):

    #string to integer

    year = 2020
    month = 2
    day = 2

    #integer to datetime

    #return
    return year,month,day

def main():
    user_input()
    view_trend()


if __name__== "__main__":
  main()
