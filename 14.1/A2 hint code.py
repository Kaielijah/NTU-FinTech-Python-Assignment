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

    #TODO: 1. ask for user input using 'word' and save response in a str variable 'function'
    next_step = '1'

    return word,function,next_step


def check_code():

    #ask user to input keyword
    #TODO: 2. ask for user to input keyword and save response into a string variable 'input_keyword'

    #get source data (code provided), the source data is stored in code_dic, a dictionary with all tickers' company name as key and stock code as value

    #filter out tickers containing user's keyword

    #ask for next step
    next_step = 'what is the next step?'

    #return
    return input_keyword,next_step


def view_trend():

    #ask user to input stock code, start date and end date
    #TODO: 3. ask for input and save response into str variables 'code','input_start','input_end'


    #convert string to datetime

    #get source data (code provided), the source data is stored in df, a pandas dataframe

    #ask for graph choice
    #TODO: 4. ask for input and save response into str variable 'graph_choice'

    #manipulate choice input

    #draw graph based on input
    #TODO: 5. ask user to input moving average frequency and save response into a int variable 'ma'

    #ask for next step
    next_step = 'what is the next step? (in view_trend function)'

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

    #TODO: 6. ask for user input using 'next_word' and save response in a str variable 'next_step'

    #return
    return next_word,next_step


def input_to_date():

    #string to integer

    year = 2020
    month = 2
    day = 2

    #integer to datetime

    #return
    return year,month,day

def main():
    word,function,user_input_next = user_input()
    # input_keyword,check_code_next = check_code()
    # code,input_start,input_end,graph_choice,ma,view_trend_next = view_trend()
    # next_word,next_request_next= next_request()
    # year,month,day = input_to_date()

    print('---------------------------------------------------')
    print('Below are the variables defined and their contents:')
    print('---------------------------------------------------\n')
    print(str(type(word))+ ' word : '+ word)
    print(str(type(function))+ ' function : '+ function)
    print(str(type(input_keyword))+ ' input_keyword : '+ input_keyword)
    print(str(type(code))+ ' code : '+ code)
    print(str(type(input_start))+ ' input_start : '+ input_start)
    print(str(type(input_end))+ ' input_end : '+ input_end)
    print(str(type(graph_choice))+ ' graph_choice : '+ graph_choice)
    print(str(type(ma))+ ' ma : '+ str(ma))
    print(str(type(next_word))+ ' next_word : '+ next_word)
    print(str(type(year))+ ' year : '+ str(year))
    print(str(type(month))+ ' month : '+ str(month))
    print(str(type(day))+ ' day : '+ str(day))
    print(str(type(user_input_next))+ ' user_input_next : '+ user_input_next)
    print(str(type(check_code_next))+ ' check_code_next : '+ check_code_next)
    print(str(type(view_trend_next))+ ' view_trend_next : '+ view_trend_next)
    print(str(type(next_request_next))+ ' next_request_next : '+ next_request_next)
  #function call

if __name__== "__main__":
  main()
