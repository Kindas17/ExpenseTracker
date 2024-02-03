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
import datetime
import time
from core.Transaction import Transaction


# Define the logger
logger = logging.getLogger(__name__)
fileHandler = logging.FileHandler('test.log', mode = 'w')
formatter = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.setLevel(logging.DEBUG)


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
            logger.debug('Filepath is valid')

            # Read transaction file
            df = pd.read_excel(self.filepath)
            self.isUsable = self.__isFileValid(df)
            if (self.isUsable):
                logger.debug('Dataframe has been assigned')
                self.df = df
            else: 
                logger.error('Dataframe is not usable!')

        else:
            logger.error(f'{filepath} is not a file!')



    def __isFileValid(self, df: pd.DataFrame) -> bool:
        return (df.columns == self.DEFAULT_REVOLUT_FILE_COLUMNS).all()
    


    def processTransactions(self):
        errorCode = self.__defaultStep1()
        if (errorCode == 1):
            logger.error('Processing step 1 returned an error')
            return 1
        else:
            logger.debug('Processing Step 1 completed')

        self.transactions = []
        self.transactions = self.__processingTOPUP()



    def __defaultStep1(self) -> int:
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
        


    def __processingTOPUP(self) -> int:
        tmp_df = self.df[self.df.Type == 'TOPUP'].copy()

        # Ignore Type column
        tmp_df = tmp_df.drop(['Type'], axis = 1)

        tmp_df['Sender'] = ['Unknown' for _ in range(len(tmp_df))]
        tmp_df['Receiver'] = ['THIS' for _ in range(len(tmp_df))]

        # Verify that all products are "Current"
        if ((tmp_df.Product == 'Current').all()):
            tmp_df = tmp_df.drop(['Product'], axis = 1)
        else:
            logger.error('Not all products are Current')

        # Ignore the Completed Date and Balance columns
        tmp_df = tmp_df.drop(['Balance', 'Completed Date'], axis = 1)

        # Check if the Fee columns contains something (don't know how to deal with it yet..)
        if (tmp_df.Fee.sum() == 0):
            tmp_df = tmp_df.drop(['Fee'], axis = 1)
        else:
            logger.error('Fee columns has to be considered')

        logger.debug('Preprocessing of TOPUP transactions completed')


        transactions = []
        for _, row in tmp_df.iterrows():
            transactions.append(
                Transaction(
                    timestamp = int(
                        (row['Started Date'] - Transaction.DEFAULT_START_DATE).total_seconds()),
                    amount = row.Amount,
                    sender = row.Sender,
                    receiver = row.Receiver,
                    currency = row.Currency,
                    description = row.Description
                )
            )

        return transactions

# The End
