# MiniWallet
Mini Wallet service is exposed through an API service

# pre-requisites
To get started with this project create a virtual environment and install the required python packages. pip install requirements.txt

# Running Tests
Navigate to  miniwallet folder run the django development server by typing the following command in terminal or cmd
``` 
python manage.py runserver 

```

* To Register a wallet
  
  Make a Post request to endpoint : http://localhost:8080/api/v1/init
 - form param : customer_xid
 
* To Enable a wallet
  
  Make a post request to endpoint : http://127.0.0.1:8000/api/v1/wallet

* To Get Wallet Details
	
  Make a GET request to endpoint : http://127.0.0.1:8000/api/v1/wallet
  
* To Add Money to wallet

  Make a POST request to endpoint :  http://127.0.0.1:8000/api/v1/wallet/deposits
  - form param : amount (decimal number)
  - form param : reference_id (unique)
  
* To Withdraw from wallet

  Make a POST request to endpoint http://127.0.0.1:8000/api/v1/wallet/withdrawals
  - form param : amount (decimal number)
  - form param : reference_id (unique)
  
* To Disable wallet
  Make a PATCH request to endpoint : http://127.0.0.1:8000/api/v1/wallet
  - form param : is_disabled (set to "true")

* Note
 - Withdrawing immediately after deposit result in unique id violation on Transaction Table as the ID is generated based on 
 UUID which is a unique combination based on timestamp and mac address
- Use user as admin, password: admin123 to login to django admin interface

# Build With
* [Django](https://www.djangoproject.com/) - Web Framework
