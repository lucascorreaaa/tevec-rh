# Loading useful libraries
import pandas as pd
import numpy as np; np.random.seed(0)
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import datetime as dt

# Loading dataset from CSV file
df = pd.read_csv("serie_vendas.csv")

# Visualizing descriptive statistics of the features
df.describe()
df.loc[:,'data_referencia'].describe()

# Visualizing total number of missing values for each column
missing_values = df.isna().sum()

# Removing rows whose values 'valor' and 'qtd_vendida' == 0 (eliminates 22.605 rows and 5 SKUs)
df.dropna(subset=['valor','qtd_vendida'], inplace=True)
m = df.shape[0]

# Adding feature 'valor_arrecadado' = valor * qtd_vendida
df['valor_arrecadado'] = df.valor * df.qtd_vendida

# Parsing 'data_referencia' to datetime and setting it as the index of data frame
df['data'] = pd.to_datetime(df['data_referencia'])
df.set_index('data', inplace=True)
df.drop(['data_referencia'], axis=1, inplace=True)

# Getting quantity of unique SKUs
qty_sku = len(df.id_produto.unique())

# Getting average selling price, sold quantity and stock quantity for every product
product_averages = df.groupby(['id_produto']).mean().drop(['qtd_estoque'], axis=1)

# --------------------
# Plotting some graphs
# --------------------

# Line plot showing monthly income evolution
plot_data = df.valor_arrecadado.resample('M').sum().reset_index()
plt.figure(figsize=(18,7))
sns.lineplot(x="data", y="valor_arrecadado", data=plot_data)
#plt.show()

# Data preparation to plot monthly income evolution by product
df_prod = pd.DataFrame(columns=['data','id_produto','valor_arrecadado'])
prod_list = df.id_produto.unique()

# Loop for build 'df_prod', which contains the monthly income evolution by product
for id_prod in prod_list:
    q = df.loc[df['id_produto'] == id_prod]
    q_resampled = q.valor_arrecadado.resample('M').sum().reset_index()
    q_resampled.insert(loc=1,column='id_produto',value=id_prod)
    df_prod = pd.concat([df_prod,q_resampled])

# Line plot showing monthly income evolution by product (all products)
plt.figure(figsize=(18,7))
sns.lineplot(x='data', y='valor_arrecadado', hue='id_produto', palette=sns.color_palette("Set1",n_colors=len(df_prod.id_produto.unique())), data=df_prod, legend=False)
#plt.show()

# --------------
# Extra Insights
# --------------

# Table with the top 15 best selling products
best_sellers = df_prod.groupby(['id_produto']).mean().reset_index()
df_prod_prices = product_averages.valor
best_sellers['valor'] = list(df_prod_prices)
best_sellers_sorted = best_sellers.sort_values(by='qtd_vendida', ascending=False)

# Top 10 best sellers product in H2 of 2017
df_prod2 = df_prod.set_index(['data'])
df_prod2_h2 = df_prod2['2017-07-01':'2017-12-31'].groupby('id_produto').sum().sort_values(by='qtd_vendida', ascending=False)

# Analysis over best seller product regarding stock consistency - Item 4
df_best_seller = df.loc[df.id_produto == 2]
df_best_seller.qtd_estoque.isna().sum()

# Comparison between 2016 and 2017 daily average of stock quantity 
df_best_seller['2016-01-01':'2016-12-31'].qtd_estoque.mean()
df_best_seller['2017-01-01':'2017-12-31'].qtd_estoque.mean()

# Getting interval to demonstrate inconsistency
df_best_seller['2016-01-20':'2016-01-23']

# ITEM 5 (fail)

"""# Function to predict daily sales of a specified product in a specified period
def predict_daily_sales(id_produto=2, period=None):
    # Stablishing the period default value
    if period is None : period = [dt.date(2018,1,1) + dt.timedelta(days=x) for x in range(1,4)]
    
    # Building product dataset, filtering original data set by 'id_produto' and dropping irrelevant columns
    prod_list = df.loc[df['id_produto'] == 2]['qtd_vendida'].reset_index()

    # Data Augmentation - adding relevant features to help prediction
    prod_list['ano'] = [d.year for d in prod_list.data]
    prod_list['mes'] = [d.month for d in prod_list.data]
    prod_list['dia'] = [d.day for d in prod_list.data]
    prod_list['mes_dia']= [(x[1][0].astype(str) + x[1][1].astype(str)) for x in prod_list[['mes','dia']].iterrows()]
    prod_list['mes_dia'] = pd.to_numeric(prod_list['mes_dia'])
    prod_list.drop('data', axis=1, inplace=True)

    # Spliting data
    X = prod_list[['ano','mes','dia', 'mes_dia']]
    y = prod_list['qtd_vendida']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Applying Linear Regression model
    lr = LinearRegression(normalize=False).fit(X_train,y_train)
    



    # Plotting ACF (AutoCorrelation Function) and PACF (Partial AutoCorrelaction Function) to estimate parameters 'p' and 'q'
    plt.figure()
    plt.subplot(211)
    plot_acf(prod_list.head(300), ax=plt.gca())
    plt.subplot(212)
    plot_pacf(prod_list.head(300), ax=plt.gca())
    plt.ylim(-0.2,1)
    plt.show()
    
    # Setting 'p','q' values
    p = 2; q = 8

    # Fit ARIMA model
    model = ARIMA(prod_list, order=(0,0,1))
    model_fit = model.fit(disp=0)
    print(model_fit.summary())"""