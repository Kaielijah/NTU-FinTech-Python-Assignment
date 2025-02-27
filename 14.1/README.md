# Required Assignment 14.1_Built-in Functions

| TODO | Task to complete |
|------|------------------|
| 1 | Ask for user input using `'word'` and save response in a string variable `'function'` |
| 2 | Ask for user to input keyword and save response into a string variable `'input_keyword'` |
| 3 | Ask for input and save response into string variables `'code'`, `'input_start'`, `'input_end'` |
| 4 | Ask for input and save response into string variable `'graph_choice'`, the types of the `graph_choice` can be found in the functional requirements inside the overall project manual. |
| 5 | Ask user to input moving average frequency and save response into an integer variable `'ma'` |
| 6 | Ask for user input using `'next_word'` and save response in a string variable `'next_step'` |

---
## User Output
Welcome to Stock Master!  

Please select a function to continue:

(1) Search for a stock code by keyword
(2) View stock trend by code

(sample input 1 or 2)
1

Please input keyword for the stock searching for: apple
Please input the code of the stock requested:
APPL

Please enter start date (eg. 2019-1-1): 2019-4-5  
Please enter end date (eg. 2019-1-1): 2020-4-2  

Please select type of graph.
  
(1) Candle Stick  
(2) High  
(3) Low  
(4) Open  
(5) Close  
(6) Adj Close  
(7) Moving Average  
(8) Volume  
  
You may select multiple choices, separate each choice by a comma.

Sample input for candle stick + High + Volume:
1,2,8

1,2

Please input the frequency for the moving average.  

Sample input for 100 days moving average:
100

20

Would you like to
return to menu
exit program
(sample input: 1 or 2)
2

## Expected Output

<class 'str'> word :
Welcome to Stock Master!

Please select a function to continue:

(1) Search for a stock code by keyword
(2) View stock trend by code

(sample input 1 or 2)

<class 'str'> function : 1
<class 'str'> input_keyword : apple  
<class 'str'> code : APPL  
<class 'str'> input_start : 2019-4-5  
<class 'str'> input_end : 2020-4-2  
<class 'str'> graph_choice : 1,2  
<class 'int'> ma : 20  

<class 'str'> next_word : 
Would you like to  
return to menu
exit program
(sample input: 1 or 2)
  
<class 'int'> year : 2020  
<class 'int'> month : 2  
<class 'int'> day : 2  
<class 'str'> user_input_next : 1  
<class 'str'> check_code_next : what is the next step?  
<class 'str'> view_trend_next : what is the next step?  
<class 'str'> next_request_next : 2  