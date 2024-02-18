#####################################################################
                                                   # Revolut Parser #
                                                   ##################

############################################### DATA DESCRIPTION ####
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
#
############################################ PROCESSING STRATEGY ####
#
# 1. Remove all transactions that are not completed yet (PENDING)
#    and all transactions that were REVERTED.
#    State column can be removed at this point: only COMPLETED
#    transactions should remain.
#####################################################################

import os
import pandas as pd
import logging
import json
from core.Transaction import Transaction


# Define the logger
logger = logging.getLogger(__name__)
fileHandler = logging.FileHandler('test.log', mode = 'w')
formatter = logging.Formatter('-> %(asctime)s - %(levelname)s\n%(name)s: %(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.setLevel(logging.DEBUG)



# Check if the Fee columns contains something (don't know how to deal with it yet..)
def isFeeColumnOk(df: pd.DataFrame) -> bool:
    return (df.Fee.sum() == 0)

# Verify that all products are "Current"
def allProductIsCurrent(df: pd.DataFrame) -> bool:
    return (df.Product == 'Current').all()

# Convert a datetime pandas object into a Transaction formatted timestamp
def convertDatetime(date: pd.Timestamp) -> int:
    return int((date - Transaction.DEFAULT_START_DATE).total_seconds())



class RevolutParser:

    DEFAULT_REVOLUT_FILE_COLUMNS = [
        'Type', 'Product', 'Started Date', 'Completed Date',
        'Description', 'Amount', 'Fee', 'Currency', 'State',
        'Balance'
    ]

    RETURN_CODES = {
        0: 'Everything was ok',
        1: 'Error occurred',
    }



    def __init__(self, filepath: str) -> None:

        # Verify file existence
        if (os.path.isfile(filepath)):
            self.filepath = filepath
            logger.debug(f'Filepath is valid: {filepath}')

            # Read transaction file
            df = pd.read_excel(self.filepath)
            self.isUsable = self.__isFileValid(df)
            if (self.isUsable):
                logger.debug('Dataframe has been imported successfully')
                self.df = df
            else: 
                logger.error('Dataframe is not usable!')

        else:
            logger.error(f'{filepath} is not a file!')



    def getDatabase(self):
        return self.df



    def getTransactionJSON(self):
        trnsx = [trn.asDic() for trn in self.transactions]
        with open('trnsx.json', 'w') as f:
            json.dump(trnsx, f, indent = 4)



    def __isFileValid(self, df: pd.DataFrame) -> bool:
        return (df.columns == self.DEFAULT_REVOLUT_FILE_COLUMNS).all()
    


    def processTransactions(self):
        errorCode = self.__preprocessing()
        if (errorCode == 1):
            logger.error('Preprocessing returned an error')
            return 1
        else:
            logger.debug('Preprocessing completed')

        self.transactions = []
        self.transactions += self.__processingTOPUP()
        self.transactions += self.__processingFEE()
        self.transactions += self.__processingCARD_PAYMENT()



    def __preprocessing(self) -> int:
        self.df = self.df[self.df.State != 'PENDING']
        self.df = self.df[self.df.State != 'REVERTED']
        logger.debug('Removed all transactions that are PENDING or REVERTED')

        # Check if state column has only COMPLETED transactions
        if ((self.df.State == 'COMPLETED').all()):
            self.df = self.df.drop(['State'], axis = 1)
            logger.debug('Removed State column')
            return 0
        else:
            leftovers = self.df[self.df.State != 'COMPLETED'].State.unique()
            logger.error('Some transactions have an unknown state: {}'.format(leftovers))
            return 1



    def __processingCARD_PAYMENT(self) -> int:
        myType = 'CARD_PAYMENT'
        tmp_df = self.df[self.df.Type == myType].copy().drop(['Type', 
                                                              'Balance', 
                                                              'Completed Date'], axis = 1)

        tmp_df['Sender'] = 'THIS'
        tmp_df['Receiver'] = 'Unknown'


        # Verify that all products are "Current"
        if (not(allProductIsCurrent(tmp_df))):
            logger.error('Not all products are Current')

        # Check if the Fee columns contains something (don't know how to deal with it yet..)
        if (not(isFeeColumnOk(tmp_df))):
            logger.error('Fee columns has to be considered')


        logger.debug(f'Processing of {myType} transactions completed')


        return [Transaction(
                            timestamp = convertDatetime(row['Started Date']),
                            amount = abs(row.Amount),
                            sender = row.Sender,
                            receiver = row.Receiver,
                            currency = row.Currency,
                            description = row.Description
                            )
                for _, row in tmp_df.iterrows()]



    def __processingFEE(self) -> int:
        myType = 'FEE'
        tmp_df = self.df[self.df.Type == myType].copy().drop(['Type', 
                                                              'Balance', 
                                                              'Completed Date'], axis = 1)

        tmp_df['Sender'] = 'Unknown'
        tmp_df['Receiver'] = 'THIS'


        # Verify that all products are "Current"
        if (not(allProductIsCurrent(tmp_df))):
            logger.error('Not all products are Current')

        # Check if the Fee columns contains something (don't know how to deal with it yet..)
        if (not(isFeeColumnOk(tmp_df))):
            logger.error('Fee columns has to be considered')


        logger.debug(f'Processing of {myType} transactions completed')


        return [Transaction(
                            timestamp = convertDatetime(row['Started Date']),
                            amount = abs(row.Amount),
                            sender = row.Sender,
                            receiver = row.Receiver,
                            currency = row.Currency,
                            description = row.Description
                            )
                for _, row in tmp_df.iterrows()]



    def __processingTOPUP(self) -> int:
        myType = 'TOPUP'
        tmp_df = self.df[self.df.Type == myType].copy().drop(['Type', 
                                                            'Balance', 
                                                            'Completed Date'], axis = 1)

        tmp_df['Sender'] = 'Unknown'
        tmp_df['Receiver'] = 'THIS'


        # Verify that all products are "Current"
        if (not(allProductIsCurrent(tmp_df))):
            logger.error('Not all products are Current')

        # Check if the Fee columns contains something (don't know how to deal with it yet..)
        if (not(isFeeColumnOk(tmp_df))):
            logger.error('Fee columns has to be considered')


        logger.debug(f'Processing of {myType} transactions completed')


        return [Transaction(
                            timestamp = convertDatetime(row['Started Date']),
                            amount = abs(row.Amount),
                            sender = row.Sender,
                            receiver = row.Receiver,
                            currency = row.Currency,
                            description = row.Description
                            )
                for _, row in tmp_df.iterrows()]

# The End
