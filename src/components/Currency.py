# Python program to convert the currency 
# of one country to that of another country  
  
# Import the modules needed 
import requests 
import json
  
class Currency: 
    # empty dict to store the conversion rates 
    rates = {}  
    src = 'https://api.exchangeratesapi.io/latest?base=USD'
    def updateOrCreate(self): 
        print("Requesting to " + self.src)
        data = requests.get(self.src).json() 

        print("Fetching done.")
        # Extracting only the rates from the json data 
        self.rates = data["rates"]

        # Then save to json file.
        self.saveToJson()

    def saveToJson(self):
        print("Saving: " + json.dumps(self.rates))
        with open('currency.json', 'w') as outfile:
            json.dump(self.rates, outfile)
            print("Saved.")
  
    # function to do a simple cross multiplication between  
    # the amount and the conversion rates 
    def convert(self, amount, currency = 'PHP'): 
        try:
            "{:.2f}".format(float(amount))
        except ValueError:
            print("Something went wrong with the value.")
            return False

        # parse
        with open('./currency.json') as f:
            data = json.load(f)

        if currency in data:
            return amount * data[currency]
        else:
            return False