import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
from operator import attrgetter
import matplotlib.colors as mcolors
#Import the csv
df = pd.read_csv('marketbasket.csv',
                   dtype={'Email': str,
                          'Name': str},
                   parse_dates=['Created at'],
                   infer_datetime_format=True)

#replace spaces with underscores
df.columns = [c.replace(' ','_') for c in df.columns]

#define the order month. Extract year-month from the date
df['OrderPeriod'] = df.Created_at.apply(lambda x: x.strftime('%Y-%m'))

#remove rows missing emails
df.dropna(subset=['Email'], inplace=True)

"""
count unique orders for each email,
calc the percent of emails with greater than 1 order
"""

n_orders = df.groupby(['Email'])['Name'].nunique()
mult_orders_perc = np.sum(n_orders > 1) / df['Email'].nunique()
print(f'{100 * mult_orders_perc:.2f}% of customers ordered more than once.')

#create a dataframe
df = df[['Email', 'Name', 'Created_at']].drop_duplicates()
df['order_month'] = df['Created_at'].dt.to_period('M') #define order months
df['cohort'] = df.groupby('Email')['Created_at'] \
                 .transform('min') \
                 .dt.to_period('M')

df_cohort = df.groupby(['cohort', 'order_month']) \
              .agg(n_customers=('Email', 'nunique')) \
              .reset_index(drop=False)
df_cohort['period_number'] = (df_cohort.order_month - df_cohort.cohort).apply(attrgetter('n'))


cohort_pivot = df_cohort.pivot_table(index = 'cohort',
                                     columns = 'period_number',
                                     values = 'n_customers')

cohort_size = cohort_pivot.iloc[:,0]
retention_matrix = cohort_pivot.divide(cohort_size, axis = 0)
#print(retention_matrix)


with sns.axes_style("white"):
    fig, ax = plt.subplots(1, 2, figsize=(12, 8), sharey=True, gridspec_kw={'width_ratios': [1, 11]})

    # retention matrix
    sns.heatmap(retention_matrix,
                mask=retention_matrix.isnull(),
                annot=True,
                fmt='.0%',
                cmap='RdYlGn',
                ax=ax[1])
    ax[1].set_title('Monthly Cohorts: User Retention', fontsize=16)
    ax[1].set(xlabel='# of periods',
              ylabel='')

    # cohort size
    cohort_size_df = pd.DataFrame(cohort_size).rename(columns={0: 'cohort_size'})
    white_cmap = mcolors.ListedColormap(['white'])
    sns.heatmap(cohort_size_df,
                annot=True,
                cbar=False,
                fmt='g',
                cmap=white_cmap,
                ax=ax[0])

    fig.tight_layout()
plt.show()
