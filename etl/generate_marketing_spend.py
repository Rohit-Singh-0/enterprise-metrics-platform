import numpy as np
import pandas as pd

###Creating the Marketing Spend CSV file ###

# START_DATE = '2017-01-01'
# END_DATE = '2018-10-31'

# CHANNEL_CONFIG= {
#     'goolge_ads': (2000,6000),
#     'facebook_ads': (1500,4000),
#     'email':(100,700),
#     'organic':(0,0)
# }

# OUTPUT_PATH = 'marketing_spend.csv'

# dates = pd.date_range(start=START_DATE, end=END_DATE, freq= "D")

# records = []

# np.random.seed(42)

# for date in dates:
#     for channel, (low,high) in CHANNEL_CONFIG.items():
#         if low==high:
#             spend=0
#         else:
#             spend = np.random.randint(low,high)
        
#         records.append({
#             "date": date.date(),
#             "channel" : channel,
#             "spend_amount": spend
#         })

# df_marketing = pd.DataFrame(records)

# df_marketing.to_csv(OUTPUT_PATH, index= False)


### Sanity Check ###
df = pd.read_csv('marketing_spend.csv')
df.groupby('channel')['spend_amount'].describe()