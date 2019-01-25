import warnings
warnings.filterwarnings("ignore")

import DateExtractor
import pandas as pd
import Conversation
import re

from datetime import datetime, timedelta
class HolidayConversation:
    dates=[]
    #read a csv file
    def read_csv(file_name):
        data=pd.read_csv(file_name,index_col=False)
        data.set_index('Day', inplace=True)
        #print(data.head())
        return data

    # Converts the string "2018/12/06" to date format 2018/12/06
    def convert_string_date(*dates):
        format_str = '%Y-%m-%d'  # The format
        return [(datetime.datetime.strptime(date, format_str)).date() for date in dates]

    # Given text to the function extracts only the date entities from the text
    def extract_date(text):
        dates = DateExtractor.DateExtractor.parse_date(text)
        return dates

    #single day query execution
    def single_day(date,data):
        message=data[data.Date == date[0]]['Holiday'].item()
        #print("oooo")
        if message=="Yes":
            message=message+Conversation.Conversations.boot_conversations[9] %(date[0])
        else:
            message = message +Conversation.Conversations.boot_conversations[10] % (date[0])
        return message
        #this function works for Present running month
    # def this_month(date):
    #     date_end = datetime.strptime(date[0], "%Y-%m-%d")  # string to date
    #     date_start = str(date_end - timedelta(days=30))[:10]  # date - days
    #     dates.clear()
    #     date_end=str(date_end)[:10]
    #     dates.insert(0,date_start)
    #     dates.insert(1,date_end)
    #     return dates

    #This year
    def this_year(dates):
        date_end = datetime.strptime(dates[0], "%Y-%m-%d")  # string to date
        date_start = str(date_end - timedelta(days=365))[:10]  # date - days
        dates.clear()
        date_end=str(date_end)[:10]
        dates.insert(0,date_start)
        dates.insert(1,date_end)

        return dates

    #Next month
    def next_month(dates):
        date_end = datetime.strptime(dates[0], "%Y-%m-%d")  # string to date
        date_start = str(date_end + timedelta(days=30))[:10]  # date - days
        dates.clear()
        date_end=str(date_end)[:10]
        dates.insert(0,date_end)
        dates.insert(1,date_start)

        return dates

    def week(dates):
        date_end = datetime.strptime(dates[0], "%Y-%m-%d")  # string to date
        date_start = str(date_end + timedelta(days=7))[:10]  # date - days
        dates.clear()
        date_end = str(date_end)[:10]
        dates.insert(0, date_end)
        dates.insert(1, date_start)

        return dates

    def list_or_num(text,dates,data):
        if bool(re.search('list|which', text.lower())) == True:
            return HolidayConversation.list_holidays(dates,data)
        elif bool(re.search('no|number|no.|many', text.lower())) == True:
            return HolidayConversation.number_of_holidays(dates,data)
        else:
            return HolidayConversation.list_holidays(dates,data)

    # List holidays in month of year
    def list_holidays(dates,data):
        holidays=data[(data['Date'] > dates[0]) & (data['Date'] < dates[1]) &
                    (data['Holiday'] == 'Yes') &
                    (data['Description'] != 'Week End')][['Date', 'Description']]
        if holidays.empty:
            return Conversation.Conversations.boot_conversations[11]% (dates[0], dates[1])

        else:

            #return Conversation.Conversations.boot_conversations[12] % (dates[0], dates[1])+holidays
            return holidays
    #Number of holidays between given dates
    def number_of_holidays(dates,data):
        number_of_holidays=len(data[(data['Date'] > dates[0]) & (data['Date'] < dates[1]) &
                    (data['Holiday'] == 'Yes') &
                    (data['Description'] != 'Week End')][['Date', 'Description']]
                   )
        #This is for passivewise message
        if len(dates)==1:
            if number_of_holidays==0:
                message=Conversation.Conversations.boot_conversations[13]
            elif number_of_holidays==1:
                message=Conversation.Conversations.boot_conversations[14] %(number_of_holidays)
            else:
                message = Conversation.Conversations.boot_conversations[15] % (number_of_holidays)
            return message
        else:
            if number_of_holidays==0:
                message=Conversation.Conversations.boot_conversations[16] %(dates[0],dates[1])
            elif number_of_holidays==1:
                message=Conversation.Conversations.boot_conversations[17] %(number_of_holidays,dates[0],dates[1])
            else:
                message = Conversation.Conversations.boot_conversations[18] % (number_of_holidays,dates[0],dates[1])
            return message
    #Function to categarise the query to either single day of range query
    def categarise_query(text,dates,data):
        try:
            if len(dates) == 1:
                if bool(re.search('year', text.lower())) == True:
                    dates = HolidayConversation.this_year(dates)
                    #print(dates)
                    #print(Conversation.Conversations.boot_conversations[8])
                    return HolidayConversation.list_or_num(text,dates,data)
                elif bool(re.search('january|february|march|april|may|june|july|august|september|october|november|december|'
                                  'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|month', text.lower())) == True:

                    if bool(re.search('[0-31]', text.lower())) == True:
                        return HolidayConversation.single_day(dates, data)
                    else:
                        dates = HolidayConversation.next_month(dates)
                        #print(dates)
                        return HolidayConversation.list_or_num(text,dates,data)
                elif bool(re.search('sunday|monday|tuesday|wednesday|thursday|friday|saturday|'
                                    'sun|mon|tue|wed|thur|fri|sat',text.lower()))==True:
                    return HolidayConversation.single_day(dates,data)

                elif bool(re.search('week', text.lower())) == True:
                    dates = HolidayConversation.week(dates)
                    #print(dates)
                    return HolidayConversation.list_or_num(text,dates,data)

                else:
                    #print(5)
                    return HolidayConversation.single_day(dates,data)
                    #return HolidayConversation.list_or_num(text)

            elif len(dates) == 2:
                #print(6)
                return HolidayConversation.list_or_num(text,dates,data)

        except TypeError:
            return Conversation.Conversations.boot_conversations[19]

    def main(text):
        # Read the database file of holidays
        data = HolidayConversation.read_csv('/home/manjunathh/chatbot/HolidaysData.csv')
        dates=HolidayConversation.extract_date(text)
        #print(dates)
        return HolidayConversation.categarise_query(text,dates,data)


