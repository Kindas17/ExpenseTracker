from parsers.RevolutParser import RevolutParser

if __name__ == '__main__':
    
    parser = RevolutParser('example_files/revolut_transactions.xlsx')
    parser.processTransactions()

    print(parser.getRawTrnsData().head())


# The End