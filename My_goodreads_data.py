# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 12:47:07 2023

@author: vidal
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



#import csv file
url = 'https://raw.githubusercontent.com/nefvid/my_goodreads_data/main/goodreads_library_export.csv'
goodreads_data = pd.read_csv(url)
goodreads_data.info()
print(goodreads_data.head(5))


#remove unnecessary columns
goodreads_data.drop(['Book Id', 'Author l-f', 'ISBN', 'ISBN13', 'Publisher', 
                     'Binding', 'Original Publication Year', 'Bookshelves with positions', 
                     'My Review', 'Spoiler', 'Private Notes', 'Owned Copies'], 
                    axis = 1, inplace=True)
goodreads_data.info()
print(goodreads_data.head())


#convert the "date read" and "date added" columns to actual dates
goodreads_data['Date Read'] = pd.to_datetime(goodreads_data['Date Read'])
goodreads_data['Date Added'] = pd.to_datetime(goodreads_data['Date Added'])


#add a column for the year read
goodreads_data['Year Read'] = goodreads_data['Date Read'].dt.strftime('%Y')



#convert number of pages to an integer (replace NaN values because float NaN cannot be converted)
goodreads_data['Number of Pages'] = goodreads_data['Number of Pages'].fillna(0)
goodreads_data['Number of Pages'] = goodreads_data['Number of Pages'].astype(int)


#some visuals
books_by_year = goodreads_data.groupby('Year Read').size()
display(books_by_year)

books_by_year.plot(kind='barh', color='m')
plt.xlabel('Books')
plt.title('Number of books read by year')
plt.show()


pages_by_year = goodreads_data.groupby(['Year Read'])['Number of Pages'].sum()
display(pages_by_year)

pages_by_year.plot(kind='barh', color='m')
plt.xlabel('Pages')
plt.title('Number of pages read by year')
plt.show()


goodreads_data.plot(kind='scatter',x='Date Read',y='Date Added', alpha=0.5)
plt.show()


#create a sub-dataframe of books read in 2020
books_read_2020 = goodreads_data[(goodreads_data['Year Read']=='2020')]
print(books_read_2020)


#some stats for 2020
average_page_count = books_read_2020['Number of Pages'].mean()
least_pages = books_read_2020['Number of Pages'].min()
most_pages = books_read_2020['Number of Pages'].max()
total_page_count = books_read_2020['Number of Pages'].sum()
print(average_page_count)
print(least_pages)
print(most_pages)
print(total_page_count)

average_rating = books_read_2020['My Rating'].mean()
print(average_rating)

one_star_books = books_read_2020['My Rating'].value_counts()[1]
print(one_star_books)



fig, ax = plt.subplots()
ax.scatter(books_read_2020['Date Read'], books_read_2020['Year Published'])
plt.xticks(rotation = 45)
plt.grid(axis='x')
plt.xlabel('Month Read')
plt.ylabel('Year Published')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
plt.show()
