#TODO : 1. import all the modules required in your program
#Reference: In sample answer code, pandas_datareader is imported
#pandas_datareader : get source data



def user_input():

    #welcome user and select a function
    word = '''
Welcome to Stock Master!

Please select a function to continue:

(1) Search for a stock code by keyword
(2) View stock trend by code

(sample input 1 or 2)
'''

    next_step = '1'
    while next_step == '1':
        function = str(input(word))

        if function == '1':
            check_code()
            
        else:
            view_trend()

        next_step = next_request()
    else:
        print("Thank you for using the system. Bye-bye.")


def check_code():

    #ask user to input keyword
    input_keyword = input('Please input keyword for the stock searching for:')

    #get source data 
    all_ticker = data.get_nasdaq_symbols()

    #TODO : 2. display last 3 rows of the dataframe
    
    #TODO : 3. save dataframe to tickers.csv file
    
    #TODO : 4. select Security Name and Symbol only or delete all the columns in dataframe except Security Name and Symbol

    #TODO : 5. save result dataframe to simple_tickers.csv file
    
    #TODO : 6. filter the dataframe, only keep those rows, whose Security Name contains input_keyword 
    
    #TODO : 7. set the index of the dataframe to be 'Symbol'
      
    print(selected_ticker)

    #TODO : 8. save result dataframe to simple_tickers V2.csv file
    
    


def view_trend():

    #ask user to input stock code, start date and end date
    code = str(input('Please input the code of the stock requested:\n'))
    
    while True:
    #convert string to datetime
        try:
            input_start = str(input('please enter start date (eg. 2019-1-1):'))
            input_end = str(input('please enter end date (eg. 2019-1-1):'))
            start = input_to_date(input_start)
            end = input_to_date(input_end)
            break
        except:
            print('the format of the date you entered is incorrect. Please try again.')

    print('start:'+str(start))
    print('end:'+str(end))
    
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

You may select multiple choices, separate each choice by comma.


Sample input for candle stick + High + Volume:
1,2,8

'''))

    #manipulate choice input
    graph_choice = graph_choice.split(',')

    choice_dic = {'2':'High',
                    '3':'Low',
                    '4':'Open',
                    '5':'Close',
                    '6':'Adj Close',
                    '7':'MA'}

    #draw graph based on input
    if '8' in graph_choice:
        graph_choice.remove('8')

        if len(graph_choice) != 0:

            #allocate space for both volume and non-volume graphs
            #plot volume graph
            print('Allocated space for volume graph and non-volume graphs.')
            print('Volume graph plotted.')

            if '1' in graph_choice:

                print('Candle stick plotted.')
                graph_choice.remove('1')


            if '7' in graph_choice:

                ma = int(input('''

Please input the frequency for the moving average.

Sample input for 100 days moving average:
100
'''))

                print('Moving average graph with frequency '+str(ma)+ ' is plotted.')
                graph_choice.remove('7')

            #plot other graph if there is any
            for item in graph_choice:
                print(item)
            print('Other graphs plotted.')


        else:

            #allocate space for volume graph only and plot volume
            print('Allocated space for volume graph only.')
            print('Volume graph plotted.')

    else:

        #allocate space for non-volume graphs only
        print('Allocated space for non-volume graphs only.')

        if '1' in graph_choice:

            print('Candle stick plotted.')
            graph_choice.remove('1')

        if '7' in graph_choice:
            ma = int(input('''

Please input the frequency for the moving average.

Sample input for 100 days moving average:
100
'''))
            print('Moving average graph with frequency '+str(ma)+ ' is plotted.')
            graph_choice.remove('7')

        #plot other graph if there is any
        for item in graph_choice:
            print(item)
        print('Other graphs plotted.')
    
       
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
    return next_step


def main():
  #function call
  user_input()

if __name__== "__main__":
  main()
