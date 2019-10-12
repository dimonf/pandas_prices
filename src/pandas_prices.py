import pandas as pd



class Prices:
    def __init__(self, df=None, mapping=None):
        if df:
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

        ref_curr_name = cols['col_ref_amount']

        def calculate_price(s):
            curr_pair = ':'.join(sorted([s[col_curr_name], ref_curr_name]))
            if ref_curr_name > s[col_curr_name]:
                curr_rate = s[col_ref_amount] / s[col_curr_amount]
            else:
                curr_rate = s[col_curr_amount] / s[col_ref_amount]

            return [curr_pair, s['col_date'], curr_rate]

        if isinstance(data, pd.DataFrame):
            tmp_df = data.apply(calculate_price, result_type='expand')
            tmp_df.columns = ['curr_pair','date','rate']
            self.prices = tmp_df.set_index(['curr_pair','date'])
