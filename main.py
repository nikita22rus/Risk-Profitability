
import pandas as pd
import numpy as np


df_rts = pd.read_excel('RTS.xlsx')


df_rts.fillna(0.1, inplace=True)


df_rts.fillna(0.1, inplace=True)

df_rts['Date'] = (pd.to_datetime(df_rts['Date'], errors='coerce')
                  .dt.strftime("%Y")
                  .replace('NaT', ''))




years_list = df_rts['Date'].unique().tolist()



years_list = years_list[0:4]


df = pd.DataFrame()





for year in years_list:
    df_rts_copy = df_rts.drop(np.where(df_rts['Date'] != year)[0])
    for ticker in df_rts_copy.columns[1:]:




        close = np.array(df_rts_copy[ticker])
        ror = np.diff(close) / close[:-1]
        aror = (ror + 1.).cumprod() - 1.
        years_total = aror.size / 12
        cagr = (aror[-1] + 1.) ** (1 / years_total) - 1 #доходнсть


        risk_monthly = ror.std()
        ror_mean = (1. + ror).mean()
        risk_yearly = np.sqrt((risk_monthly**2 + ror_mean**2)**12 - ror_mean**24) #риск

        list_of_lists = [[year,ticker,cagr,risk_yearly]]
        df_tickers = pd.DataFrame(list_of_lists, columns = ['Year','Ticker','доходнсть','риск'])

        df = pd.concat([df,df_tickers])



writer = pd.ExcelWriter('доходность_риск_RTS.xlsx', engine='xlsxwriter')

# Write your DataFrame to a file
df.to_excel(writer, 'Лист1')

# Save the result
writer.save()



