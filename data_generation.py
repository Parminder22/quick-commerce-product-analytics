import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

n_rows = 55000
user_ids = np.random.choice(range(1, 15000), size=n_rows) # ~15k unique users
dates = [datetime(2025, 1, 1) + timedelta(days=np.random.randint(0, 150), minutes=np.random.randint(0, 1440)) for _ in range(n_rows)]
order_values = np.random.lognormal(mean=3.5, sigma=0.8, size=n_rows) # Log-normal for realistic order values

df = pd.DataFrame({'transaction_id': range(1, n_rows+1), 'user_id': user_ids, 'timestamp': dates, 'order_value': order_values})

power_users = np.random.choice(user_ids, size=1500, replace=False)
df['customer_segment'] = np.where(df['user_id'].isin(power_users), 'High-Value (Power)', 'Standard')
df.loc[df['customer_segment'] == 'High-Value (Power)', 'order_value'] *= 3.5 

df['ab_test_group'] = np.random.choice(['Control', 'Test'], size=n_rows, p=[0.5, 0.5])

test_repeats = df[df['ab_test_group'] == 'Test'].sample(frac=0.15)
df = pd.concat([df, test_repeats]).reset_index(drop=True)

df['transaction_id'] = range(1, len(df) + 1)

df.to_csv('transactions.csv', index=False)
print(f"Generated {len(df)} rows. Saved to transactions.csv")   