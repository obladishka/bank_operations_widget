# Bank operations widget project

## Description
Bank operations widget project is a backend project aimed at preparing data for display in a new widget 
that shows several recent successful banking transactions of a client. 

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/obladishka/bank_operations_widget.git
    ```
2. Install project dependencies:
    ```commandline
    poetry intall
    ```
3. To experience masking function, go to src/widget.py and call the mask_account_card function and transmit 
relevant data to it in a form of `"your_card_name card_number"` for cards or `"Счет account_number"` for accounts. 
Don't forget to print out the result:
    ```commandline
    your_card = "your_card_name card_number"
    print(mask_account_card("your card"))
    your_account = "Счет account_number"
    print(mask_account_card("your account"))
    ```
4. Go to src/processing.py and create a list of dicts containing information of your latest operations in a form of
`{"id": operation_id, "state": "EXECUTED"/"CANCELED", "date": "operation_date"}`. 
Transmit this data to a filter_by_state function to see only "EXECUTED" operations 
or specify the filtering state by transmitting second parameter `state="CANCELED"`. 
Call a sort_by_date function to see your operations in descending chronological order (from the latest to the earliest).
To see operations in ascending order, transmit a second parameter `parameter="False"`
   ```commandline
   operations_data = [
   {"id": operation1_id, "state": "EXECUTED", "date": "operation1_date"}, 
   {"id": operation2_id, "state": "CANCELED", "date": "operation2_date"}
   ]
   print(filter_by_state(operations_data)) # outputs only executed operations
   print(filter_by_state(operations_data, state="CANCELED")) # outputs only canceled operations
   print(sort_by_date(operations_data)) # outputs operations in chronlogical order from the latest to the earliers
   print(sort_by_date(operations_data, parameter=False)) # outputs operations from the earliers to the latest
   ```

## Usage

1. Masking function:
   ```commandline
   # Card usage example
   Visa Platinum 7000 7922 8960 6361  # input data
   Visa Platinum 7000 79** **** 6361  # output data
   
   # Account usage example
   Счет 73654108430135874305  # input data
   Счет **4305  # output data
   ```
2. Filtering function:
   ```commandline
   # Function output with default state 'EXECUTED'
   [
   {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, 
   {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
   ] 
   
   # Function output with 'CANCELED' passed as the second argument
   [
   {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, 
   {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
   ]
   ```
3. Sorting function:
   ```commandline
   # Function output (sorting in descending order, i.e. from the most recent operations)
   [
   {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, 
   {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}, 
   {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, 
   {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
   ]
   ```
