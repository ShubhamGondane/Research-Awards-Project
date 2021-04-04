import pandas as pd

df = pd.read_csv('/Users/shubhamgondane/volunteer_work/data/article_journals_data/cleaned/Journal of Educational and Behavioral Statistics.csv')

df1 = df[df.DOI.apply(lambda x: len(str(x))>15)]
df1 = df1.drop('Unnamed: 0', axis=1)

df2 = df[df.DOI.apply(lambda x: len(str(x))<=15)]
df2 = df2.drop('Unnamed: 0', axis=1)
df1.to_csv('/Users/shubhamgondane/volunteer_work/data/article_journals_data/cleaned/Journal of Educational and Behavioral Statistics_1.csv')
df2.to_csv('/Users/shubhamgondane/volunteer_work/data/article_journals_data/cleaned/Journal of Educational and Behavioral Statistics_2.csv')