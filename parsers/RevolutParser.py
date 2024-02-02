#####################################################################
                                                   # Revolut Parser #
                                                   ##################

#################################################### DESCRIPTION ####
# |- Type -
# |--- TOPUP:        Transactions towards the target account,
# |                  amount should be considered as positive.
# |--- FEE:          Expenses for services offered by Revolut.
# |                  Amount should be considered as negative.
# |--- CARD_PAYMENT: General payments through cards connected with
# |                  revolut account.
# |--- TRANSFER:     Money exchanged between accounts or internal
# |                  vaults.
# |--- CARD_REFUND:  Refunds of a card payment. Should be
# |                  considered as a positive transaction.
# |--- EXCHANGE:     Currency conversion. Negative is currency
# |                  is different than EUR. Positive otherwise.
# |--- ATM:          ATM money exchange.
# |
# | - Product -
# | --- Current:     Transaction concerns current account.
# | --- Savings:     Transaction concerns savings account.
# |
# | - State -
# | --- COMPLETED:   Transaction is completed and valid.
# | --- REVERTED:    Transaction has been reverted and can be
# |                  discarded.
# | --- PENDING:     Transaction has not been completed yet.
#####################################################################

import os
import pandas as pd
from core.Transaction import Transaction

class RevolutParser:

    DEFAULT_REVOLUT_FILE_COLUMNS = [
        'Type', 'Product', 'Started Date', 'Completed Date',
        'Description', 'Amount', 'Fee', 'Currency', 'State',
        'Balance'
    ]



    def __init__(self, filepath: str) -> None:
        
        # Verify file existence
        if (os.path.isfile(filepath)):
            self.filepath = filepath

            # Read transaction file
            df = pd.read_excel(self.filepath)
            self.isUsable = self.__isFileValid(df)
            if (self.isUsable): self.df = df

        else:
            print(f'FAIL: {filepath} is not a file!')



    def __isFileValid(self, df: pd.DataFrame) -> bool:
        return (df.columns == self.DEFAULT_REVOLUT_FILE_COLUMNS).all()
    


    def processTransactions(self):
        # Remove unused columns
        self.df = self.df.drop(['Currency', 'Completed Date'], axis = 1)



    def getRawTrnsData(self):
        if (hasattr(self, 'df')):
            return self.df
        else:
            return None


# The End
