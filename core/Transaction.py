#####################################################################
                                                      # Transaction #
                                                      ###############

TAGS = {
    'NONE': 'Unknown category'
}

KNOWN_CURRENCIES = [
    'EUR'
]



class Transaction:

    def __init__(self, date: int, amount: float, 
                 currency: str = 'EUR', description: str = '', 
                 tag: str = 'NONE') -> None:
        
        self.date: int = date
        self.amount: float = amount
        self.currency: str = currency
        self.description: str = description
        self.tag: str = tag



# The End
