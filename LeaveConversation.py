
import DateExtractor
import Conversation
import datetime
import warnings
warnings.filterwarnings("ignore")

class LeaveConversation:
    leave_types = ['sick leave', 'privillage leave', 'maternity leave', 'paternity leave', 'bereavement leave']
    Emp_id = 1029
    Emp_Name = 'Manjunath'
    leave_type = None
    From_date = None
    To_date = None
    Number_of_days=None

    #Prints the summary of conversation
    def Summary(leave_type,From_Date,To_Date):
        s= Conversation.Conversations.boot_conversations[4]
        From_Date,To_Date=LeaveConversation.convert_string_date(From_Date,To_Date)
        LeaveConversation.Number_of_days=str(To_Date-From_Date)
        # s=Conversation.Conversations.boot_conversations[4]+\
        #   'Emp ID:'+str(LeaveConversation.Emp_id)+'Emp Name:'+LeaveConversation.Emp_Name
        # +'Leave Type:'+str(LeaveConversation.leave_type)+'From Date:'+str(LeaveConversation.From_date)
        # +'To Date:'+str(LeaveConversation.To_date)+'Number of Days:'+str(LeaveConversation.Number_of_days)
        # print(s)
        return str(s)

    #Converts the string "2018/12/06" to date format 2018/12/06
    def convert_string_date(*dates):
        format_str = '%Y-%m-%d'  # The format
        return [(datetime.datetime.strptime(date, format_str)).date() for date in dates]

    #Extracts the type of leave employee is planning to take from the query
    def extract_leave_type(text):
        leave_type = [type for type in LeaveConversation.leave_types if type in text.lower() ]
        if len(leave_type)==0:
            leave_type=None
        return leave_type

    #Given text to the function extracts only the date entities from the text
    def extract_date(text):
        dates=DateExtractor.DateExtractor.parse_date(text)
        return dates

    #This function is used to set the From date and To date to the variable mentioned
    def set_dates(dates):
        if dates!=None and len(dates)==2:
            LeaveConversation.From_date=dates[0]
            LeaveConversation.To_date=dates[1]
            return LeaveConversation.From_date,LeaveConversation.To_date
        elif dates!=None and len(dates)==1:
            LeaveConversation.From_date = dates[0]
            return LeaveConversation.From_date

    #If in the query if the use has only mentioned the leave type then this function executes to get From date and To date
    def only_leave_entity(self):
        print(Conversation.Conversations.boot_conversations[2])
        text2 = input()
        dates = LeaveConversation.extract_date(text2)
        LeaveConversation.set_dates(dates)
        while LeaveConversation.From_date == None and LeaveConversation.To_date == None:
            print(Conversation.Conversations.boot_conversations[2])
            text = input()
            dates = LeaveConversation.extract_date(text)
            LeaveConversation.set_dates(dates)
        if LeaveConversation.From_date != None and LeaveConversation.To_date == None:
            print(Conversation.Conversations.boot_conversations[3])
            text = input()
            text = LeaveConversation.From_date + " to " + text
            dates = LeaveConversation.extract_date(text)
            LeaveConversation.set_dates(dates)

        # If in the query if the use has only mentioned the leave type from date and not mentioned to date
        # then this function executes to get To date
    def only_leave_and_from_entity(self):
        print(6)
        return Conversation.Conversations.boot_conversations[3]
        text2 = input()
        dates = LeaveConversation.extract_date(text2)
        LeaveConversation.set_dates(dates)
        while LeaveConversation.From_date != None and LeaveConversation.To_date == None:
            return Conversation.Conversations.boot_conversations[3]
            #text = input()
            print(7)
            text = LeaveConversation.From_date + " to " + text2
            dates = LeaveConversation.extract_date(text)
            #dates = LeaveConversation.extract_date(text)
            print(dates)
            LeaveConversation.set_dates(dates)
        if LeaveConversation.From_date != None and LeaveConversation.To_date != None:
            # print(Conversation.Conversations.boot_conversations[3])
            # text = input()
            # text = LeaveConversation.From_date + " to " + text
            # dates = LeaveConversation.extract_date(text)
            LeaveConversation.set_dates(dates)

    #If in the Query there is only from date and start date then it promts the user to enter the type of leave he wants
    def Only_dates_entity(self):
        return Conversation.Conversations.boot_conversations[0]
        text=input()
        if len(LeaveConversation.extract_leave_type(text))==1:
            LeaveConversation.leave_type=LeaveConversation.extract_leave_type(text)
        else:
            return Conversation.Conversations.boot_conversations[0]
            text = input()
            LeaveConversation.extract_leave_type(text)

    #Once everything is ready it will ask the user whether you want to change some entities.
    def Confirm_Change(self):
        print(Conversation.Conversations.boot_conversations[5])
        text = input()
        if text.lower() == 'confirm':
            return Conversation.Conversations.boot_conversations[7]
            exit()
        elif text.lower() == 'change':
            return Conversation.Conversations.boot_conversations[6]
            LeaveConversation.leave_type = None
            LeaveConversation.From_date = None
            LeaveConversation.To_date = None
            LeaveConversation.Number_of_days = None

    def main(text1):
        text1 = text1
        LeaveConversation.leave_type = LeaveConversation.extract_leave_type(text1)
        dates = LeaveConversation.extract_date(text1)
        LeaveConversation.set_dates(dates)
        print(LeaveConversation.leave_type,LeaveConversation.From_date,LeaveConversation.To_date)
        if LeaveConversation.leave_type == None and LeaveConversation.From_date == None and LeaveConversation.To_date == None:
            return Conversation.Conversations.boot_conversations[0]


        # Only leave type mentioned
        elif LeaveConversation.leave_type != None and LeaveConversation.From_date == None and LeaveConversation.To_date == None:
            LeaveConversation.only_leave_entity(2)
            LeaveConversation.Summary(LeaveConversation.leave_type, LeaveConversation.From_date,
                                      LeaveConversation.To_date)
            LeaveConversation.Confirm_Change(4)
            print('3')
            # exit()

        elif LeaveConversation.leave_type == None and LeaveConversation.From_date != None and LeaveConversation.To_date != None:
            LeaveConversation.Only_dates_entity(3)
            LeaveConversation.Summary(LeaveConversation.leave_type, LeaveConversation.From_date,
                                      LeaveConversation.To_date)
            LeaveConversation.Confirm_Change(4)
            print(4)
            # exit()

        elif LeaveConversation.leave_type == None and LeaveConversation.From_date != None and LeaveConversation.To_date == None:
            return Conversation.Conversations.boot_conversations[0]

            #LeaveConversation.extract_leave_type()
            # LeaveConversation.Summary(LeaveConversation.leave_type, LeaveConversation.From_date,
            #                           LeaveConversation.To_date)
            # LeaveConversation.Confirm_Change(4)
            print(5)
            # exit()

        elif LeaveConversation.leave_type != None and LeaveConversation.From_date != None and LeaveConversation.To_date == None:
            # print(Conversation.Conversations.boot_conversations[3])
            LeaveConversation.only_leave_and_from_entity(4)
            LeaveConversation.Summary(LeaveConversation.leave_type, LeaveConversation.From_date,
                                      LeaveConversation.To_date)
            LeaveConversation.Confirm_Change(4)

        # All entities conversation done
        elif LeaveConversation.leave_type != None and LeaveConversation.From_date != None and LeaveConversation.To_date != None:
            LeaveConversation.Summary(LeaveConversation.leave_type, LeaveConversation.From_date,
                                      LeaveConversation.To_date)
            LeaveConversation.Confirm_Change(4)
        else:
            print("In else block of Leave conversation")

