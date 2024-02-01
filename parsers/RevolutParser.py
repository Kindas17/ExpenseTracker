#####################################################################
                                                   # Revolut Parser #
                                                   ##################

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



    def getRawTrnsData(self):
        if (hasattr(self, 'df')):
            return self.df
        else:
            return None


# The End
