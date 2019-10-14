import pandas as pd



class Prices:
    def __init__(self, df=None, mapping=None):
        if df is not None:
            self.prices = self.calculate_prices(df, mapping)

    def calculate_prices(self, data, mapping=None):
        """data can be:
           pandas.DataFrame with

        """
        cols = {
            'col_date'        : 'date',
            'col_curr_name'   : 'curr',
            'col_curr_amount' : 'amount',
            'col_ref_amount'  : 'usd',
                }

        if mapping:
            cols.update(mapping)

        col_date        = cols['col_date']
        col_curr_name   = cols['col_curr_name']
        col_curr_amount = cols['col_curr_amount']
        col_ref_amount  = cols['col_ref_amount']
        ref_curr_name   = cols['col_ref_amount'].upper()

        def calculate_price(s):
            rec_curr_name = s[col_curr_name].upper()
            curr_pair = ':'.join(sorted([rec_curr_name, ref_curr_name]))
            if ref_curr_name > rec_curr_name:
                curr_price = s[col_ref_amount] / s[col_curr_amount]
            else:
                curr_price = s[col_curr_amount] / s[col_ref_amount]

            return [curr_pair, s[col_date], curr_price]

        if isinstance(data, pd.DataFrame):
            #leave only records where currency differs from base currency
            data = data[data[col_curr_name].str.upper() != ref_curr_name]
            #
            tmp_df = data.apply(calculate_price, result_type='expand', axis=1)
            tmp_df.columns = ['curr_pair','date','price']
            #aggregate prices for same date
            return tmp_df.groupby(['curr_pair','date'])['price'].mean()
