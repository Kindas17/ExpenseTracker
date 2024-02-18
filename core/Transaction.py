#####################################################################
                                                      # Transaction #
                                                      ###############

import datetime

TAGS = {
    'NONE': 'Unknown category'
}

KNOWN_CURRENCIES = [
    'EUR'
]



class Transaction:

    DEFAULT_START_DATE = datetime.datetime(1996, 1, 17, 0, 0, 0)

    def __init__(self, timestamp: int, amount: float, 
                 sender: str, receiver: str,
                 currency: str = 'EUR', description: str = '', 
                 tag: str = 'NONE') -> None:
        
        self.timestamp: int = timestamp
        self.sender: str = sender
        self.receiver: str = receiver
        self.amount: float = amount
        self.currency: str = currency
        self.description: str = description
        self.tag: str = tag

    def __reformatDate(self):
        return datetime.timedelta(seconds = self.timestamp) + self.DEFAULT_START_DATE
    
    def __repr__(self):
        return f'{self.sender} -> {self.receiver}: {self.amount} {self.currency} @ {self.__reformatDate()}'
    
    def asDic(self):
        return {
            'timestamp': self.timestamp,
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'currency': self.currency,
            'description': self.description,
            'tag': self.tag,
        }



# The End
