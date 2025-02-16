#import modules

def user_input():

    #welcome user and select a function
    #TODO : 1. Design a welcome message that ask user to select a function, assign this message to a string variable 'word'

    #TODO : 2. Define a string variable 'function' . (This variable will be used to hold user's choice of function.)

    #TODO : 3. Define a string variable 'next_step', assign this string as '1' . (This variable will be used to construct a branch in following project blocks.)

    return word,function,next_step

def check_code():

    #ask user to input keyword
    #TODO : 4. Define a string variable 'input_keyword' . (This variable will be used to hold user's input of keyword to search.)

    #get source data (code provided), the source data is stored in code_dic, a dictionary with all tickers' company name as key and stock code as value

    #filter out tickers containing user's keyword

    #ask for next step
    #TODO : 5. Define a string variable 'next_step' . (This variable will be used to hold user's choice of next step to take.)

    #return
    return input_keyword,next_step

def view_trend():

    #ask user to input stock code, start date and end date
    #TODO : 6. Define 3 string variables 'code','input_start','input_end' . (These variable will be used to hold user's choice of stock code,start date and end date)

    #convert string to datetime

    #get source data (code provided), the source data is stored in df, a pandas dataframe

    #ask for graph choice
    #TODO : 7. Define a string variable 'graph_choice' . (This variable will be used to hold user's choice of types of graphs to plot.)

    #manipulate choice input

    #draw graph based on input
    #TODO : 8. Define a int variable 'ma' with value 10 . (This variable will be used to hold user's choice of moving average graph frequency.)

    #ask for next step
    #TODO : 9. Define a string variable 'next_step' . (This variable will be used to hold user's choice of next step to take.)

    #return
    return code,input_start,input_end,graph_choice,ma,next_step

def next_request():

    #ask user to select next step to proceed with
    #TODO : 10. Design a message that ask user to select next step to take, assign this message to a string variable 'next_word'

    #TODO : 11. Define a string variable 'next_step' . (This variable will be used to hold user's choice of next step to take.)

    #return
    return next_word,next_step


def input_to_date(input_date):

    #string to integer

    #TODO: 12. Define 3 int variables 'year','month','day', initialise their values randomly

    #integer to datetime

    #return
    return year,month,day

def main():
    word,function,user_input_next = user_input()
    input_keyword,check_code_next = check_code()
    code,input_start,input_end,graph_choice,ma,view_trend_next = view_trend()
    next_word,next_request_next= next_request()
    year,month,day = input_to_date()

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
