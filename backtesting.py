from session import session
import pandas as pd
import datetime

# Backtesting

# Klines is the candles of some symbol (up to 1500 candles). Dataframe, last elem has [-1] index
def klines(symbol, start_date_time, end_date_time, timeframe):
    try:
        # Convert the string to a datetime object
        datetime_obj_start = datetime.datetime.strptime(start_date_time, "%Y-%m-%d %H:%M:%S")
        datetime_obj_end = datetime.datetime.strptime(end_date_time, "%Y-%m-%d %H:%M:%S")
        # Convert the datetime object to epoch time (milliseconds since January 1, 1970)
        epoch_time_start = int(datetime_obj_start.timestamp() * 1000)
        epoch_time_end = int(datetime_obj_end.timestamp() * 1000)
        # Initialize an empty DataFrame to store the results
        df = pd.DataFrame()
        # Make multiple requests and concatenate the results
        while epoch_time_start < epoch_time_end:
            resp = session.get_kline(
                category='linear',
                symbol=symbol,
                interval=timeframe,
                start=epoch_time_start,
                end=epoch_time_start + 1000 * 60 * 60 * 24,  # End the current request at the next day
            )['result']['list']
            epoch_time_start = epoch_time_start + 1000 * 60 * 60 * 24
            # Convert the response to a DataFrame and append it to the main DataFrame
            tmp_df = pd.DataFrame(resp)
            tmp_df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Turnover']
            tmp_df = tmp_df.set_index('Time')
            tmp_df = tmp_df.astype(float)
            tmp_df = tmp_df[::-1]
            df = pd.concat([df, tmp_df], ignore_index=False)

            # Update the start time for the next request
            epoch_time_start = int(tmp_df.index[-1]) + 1
        return df
    except Exception as err:
        print(err)

for coin in coins:
    symbol = coin['symbol']
    start_date_time = "2023-07-01 00:00:00"
    end_date_time = "2023-07-10 00:00:00"
    timeframe = 240 #1,3,5,15,30,60,120,240,360,720,D,M,W
    
    df = klines(symbol, start_date_time, end_date_time, timeframe)
    print("")
    print(f"-- Data for {symbol}:")
    print(df)


