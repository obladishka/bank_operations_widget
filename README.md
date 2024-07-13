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
   
5. Module src/generators.py is created for data filtering nd generation. Create a list of dicts containing 
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
