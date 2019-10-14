import pandas as pd



class Prices:
    def __init__(self, data=None, mapping=None):
        if isinstance(data, pd.DataFrame):
            self.prices = self.calculate_prices(data, mapping)
        else:
            self.prices = pd.read_csv(data, index_col=[0,1], parse_dates=True, header=0)

    def prices_to_csv(self, filename):
        """
        dump prices data to file <filename>
        """
        self.prices.to_csv(filename, header=True)

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

        def test_record(s):
            """
            applies for each row in a dataframe and returns True if
            the data is valid for rate calculation
            """
            if s[[col_curr_name,col_date,  col_curr_amount, col_ref_amount]].isna().any():
                return False
            elif s[col_curr_name] == ref_curr_name:
                return False
            elif s[col_ref_amount] == 0 or s[col_curr_amount] == 0:
                return False
            return True

        def calculate_price(s):
            rec_curr_name = s[col_curr_name]
            curr_pair = ':'.join(sorted([rec_curr_name, ref_curr_name]))
            if ref_curr_name > rec_curr_name:
                curr_price = s[col_ref_amount] / s[col_curr_amount]
            else:
                curr_price = s[col_curr_amount] / s[col_ref_amount]

            return [curr_pair, s[col_date], curr_price]

        data.loc[:,col_curr_name] = data[col_curr_name].str.upper()
        #remove records for which prices cannot be calculated
        data_a = data.loc[data.apply(test_record, result_type='reduce',axis=1)]
        #
        tmp_df = data_a.apply(calculate_price, result_type='expand', axis=1)
        tmp_df.columns = ['curr_pair','date','price']
        #aggregate prices for same date
        return tmp_df.groupby(['curr_pair','date'])['price'].mean()

    def get_price(self, curr_pair, date):
        """
        returnes the latest price
        curr_pair: "EUR:USD". Must match exactly stored value (index first level)
        date: "2019-01-01". Will match nearest value if not exact match found

        returns: the exact or nearest value
        """
        #TODO: return tuple (actual_picked_date, price)
        location = self.prices.loc[curr_pair].index.get_loc(date, method='nearest')
        return self.prices.iloc[location].iloc[-1]
