# fetch-backend-assess

## Design decissions
  1. Keep totals for each payer up to date as we add new transactions and spend points. Makes it really fast to get current balances as that route just needs to return the dictionary.
  2. Have a flag for if the transactions need to be sorted. Save time by only sorting if a spend request is received and something has been added (out of order) since the last sort.
  3. It seemed important to have a record of all transactions for accounting purposes. For this reason we are not removing transactions from the list when they reach zero. We will just skip over them when processing a spend request.

## How to use

### setup
  * Go to https://www.python.org/downloads/ and download the latest version of Python 3. 
  * Execute the downloaded file.
  * Follow the on screen prompts to install the language on your machine.
  * From the command line type 'pip install flask'
  * Ensure you're in the directory where app.py exists and type 'python app.py' to start the local server
  * There should be a link in the terminal to take you to the webpage.

### accessing the routes
  * ADD
    * You can fill out the form on the index page to add new records. Timestamps for these records will be added by the server
    * You can also send this route JSON data as either single transaction or a list of transactions.
      * code examples for how to do this via javascript are available in the logic.js file.
  * SPEND
    * Use the code snippets in the logic.js file to spend points.
    * If you try to spend more points than you have you'll receive an error detailing the issue.
  * BALANCE
    * Add /balance to the end of your server URL to get current balances as JSON.

