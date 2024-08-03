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
5. Module src/generators.py is created for data filtering and generation. Create a list of dicts containing 
full information of your operations including operation id, state, date, operationAmount and description, etc.
Specify the currency of interest and transmit both parameters to filter_by_currency function. 
Print out information of relevant operations one by one using `next()`.
If you want to see only operations descriptions you can then transmit your filtered or original list to
transaction_descriptions function and then print out the results in a same way you did with filter_by_currency function.
**NOTE!** In case you only want to see description of filtered operations don't forget to turn function's output
into a list before transmitting it to filter_by_currency function.
The card_number_generator function is used to generate card numbers between 0000000000000001 and 9999999999999999 in a 
specified range. To use it simply transmit the start and the end number of a card and print the result.
   ```commandline
   transactions = [
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
   ]
   
   usd_transactions = filter_by_currency(transactions, "USD") # creates transactions filter 
   print(next(usd_transactions)) # outputs 1st USD transaction
   
   usd_transactions = list(filter_by_currency(transactions, "USD")) # creates list of USD transactions
   usd_descriptions = transaction_descriptions(usd_transactions) # generates descriptions of USD transactions
   print(next(usd_descriptions)) # outputs 1st USD transaction description
   
   card_numbers_list = list(card_number for card_number in card_number_generator(1, 5))
   print(card_numbers_list) # outputs a list of card numbers from "0000 0000 0000 0001" to "0000 0000 0000 0005"
   ```
6. Module src/decorators.py contains function logging decorator that logs function start and end time, 
execution result and errors information. To use it simply place decorator above your function and then run it. 
If you want the logs to be written in a separate file, transmit a file name to decorator.
   ```commandline
   # logs are printed to the console
   @log
   def your_func():
       ....
   
   # logs are written in a special file
   @log("file.txt")
   def your_func():
       ....
   ```
7. Module src/utils.py contains functions for working with JSON-files. 
Create a JSON-file with information about financial transactions and transmit a path to it to get_operations_data_from_json 
function. The function will return a python object of list of dicts type where each dict refers to a transaction.
You can now transmit any transaction to get_transaction_amount function to see the transaction amount in rubles. 
If transaction is made in other currency, the amount is converted to rubles via Exchange Rates Data API.
   ```commandline
   transactions_list = get_operations_data_from_json("operation.json") # creates a list of all transactions in the file
   
   for transaction in transactions_list:
      print(get_transaction_amount(transaction)) # prints value of each transaction in rubles
   ```
8. Module src/external_api.py is created to work with external services. To use the module first change the name of
".env.example" file in the root of the project to ".env" and replace data in it with correct data (your API-token).
After that you can call get_exchange_rate function either directly from src/external_api.py module 
or by transmitting non-ruble transaction to get_transaction_amount function. 
On default currency to which amount is converted is set to RUB, but you can change it whenever you want by transmitting
the 3rd parameter to the function. The function returns a tuple with operation status and transaction amount in case
operation was successful or with status and error message in case an error occurred.
   ```commandline
   # convert 120 USD to RUB
   status, result = get_exchange_rate(120, "USD")
   print(result)
   
   # convert 120 USD to EUR
   status, result = get_exchange_rate(120, "USD", "EUR") # converts 120 USD to EUR
   print(result)
   ```
9. Module src/read_from_file.py contains functions for working with CSV and Excel-files. 
They first read transmitted files and then transform the information and output it in the format same to that of
get_operations_data_from_json function.
   ```commandline
   # get a list of all transactions in the CSV-file
   transactions = get_operations_data_from_csv("transactions.csv")
   
   # get a list of all transactions in the Excel-file
   transactions = get_operations_data_from_excel("transactions.xlsx")
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
4. Filtering by currency function:
   ```commandline
   usd_transactions = filter_by_currency(transactions, "USD")
   for _ in range(2):
       print(next(usd_transactions))

   >>> {
             "id": 939719570,
             "state": "EXECUTED",
             "date": "2018-06-30T02:08:58.425572",
             "operationAmount": {
                 "amount": "9824.07",
                 "currency": {
                     "name": "USD",
                     "code": "USD"
                 }
             },
             "description": "Перевод организации",
             "from": "Счет 75106830613657916952",
             "to": "Счет 11776614605963066702"
         }
         {
                 "id": 142264268,
                 "state": "EXECUTED",
                 "date": "2019-04-04T23:20:05.206878",
                 "operationAmount": {
                     "amount": "79114.93",
                     "currency": {
                         "name": "USD",
                         "code": "USD"
                     }
                 },
                 "description": "Перевод со счета на счет",
                 "from": "Счет 19708645243227258542",
                 "to": "Счет 75651667383060284188"
          }
   ```
5. Transactions descriptions generator:
   ```commandline
   descriptions = transaction_descriptions(transactions)
   for _ in range(5):
       print(next(descriptions))
   
   >>> Перевод организации
       Перевод со счета на счет
       Перевод со счета на счет
       Перевод с карты на карту
       Перевод организации
   ```
6. Cards numbers generator:
   ```commandline
   for card_number in card_number_generator(21, 25):
       print(card_number)
   
   >>> 0000 0000 0000 0021
       0000 0000 0000 0022
       0000 0000 0000 0023
       0000 0000 0000 0024
       0000 0000 0000 0025
   ```
7. Logging decorator:
   ```commandline
   # successful function execution
   your_func start time: 2024-07-15 20:49:39.914280
   your_func ok
   your_func end time: 2024-07-15 20:49:40.914280
   
   # error log
   your_func start time: 2024-07-15 20:49:39.914280
   your_func error: Something went wrong!. Inputs: (), {}
   your_func end time: 2024-07-15 20:49:39.914280
   ```
8. Transaction amount calculating function:
   ```commandline
   file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.json")
   rub_transaction = get_transaction_amount(file_path)[0]
   usd_transaction = get_transaction_amount(file_path)[1]
   
   print(get_transaction_amount(rub_transaction)) # returns 31957.58
   
   # successful conversion
   print(get_transaction_amount(usd_transaction)) 
   >>> 706814.75
   
   # unsuccessful conversion
   print(get_transaction_amount(usd_transaction))
   >>> None
   ```

## Testing

The project is tested by 56 different ways which provides 100%-code coverage. 
Project testing is performed using pytest. To run the tests install pytest in a develop group
and write a relevant command in your terminal:
```commandline
    poetry add --group dev pytest
    pytest
```
To see code coverage statistics install pytest-cov `poetry add --group dev pytest-cov` and enter
`pytest --cov` in your terminal.
