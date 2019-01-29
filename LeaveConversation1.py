import DateExtractor
import Conversation
import datetime
import Variables
import warnings
warnings.filterwarnings("ignore")

class LeaveConversation1:

    #Extracts the type of leave employee is planning to take from the query
    def extract_leave_type(text):
        leave_type = [type for type in Variables.leave_types if type in text.lower() ]
        if len(leave_type)==0:
            leave_type=None
        else:
            leave_type=leave_type[0]
        return leave_type

    # Given text to the function extracts only the date entities from the text
    def extract_date(text):
        dates = DateExtractor.DateExtractor.parse_date(text)
        return dates

    # Converts the string "2018/12/06" to date format 2018/12/06
    def convert_string_date(*dates):
        format_str = '%Y-%m-%d'  # The format
        return [(datetime.datetime.strptime(date, format_str)).date() for date in dates]

    # This function is used to set the From date and To date to the variable mentioned
    def set_dates(dates):
        if dates != None and len(dates) == 2:
            Variables.From_date = dates[0]
            Variables.To_date = dates[1]

        elif dates != None and len(dates) == 1:
            Variables.From_date = dates[0]


    # Prints the summary of conversation
    def Summary(s):
        s = Conversation.Conversations.boot_conversations[4]
        dates= LeaveConversation1.convert_string_date(Variables.From_date, Variables.To_date)
        Variables.Number_of_days = str(dates[1] - dates[0])
        s = str(Conversation.Conversations.boot_conversations[4]+"\n"+
                "Emp Name:"+Variables.Emp_Name +"\n"+
                "Leave Type:"+ Variables.leave_type +"\n"+
                "From Date:"+Variables.From_date +"\n"+
                "To Date:"+Variables.To_date+"\n"+
                "Number Of Days:"+Variables.Number_of_days+"\n"+
                Conversation.Conversations.boot_conversations[5])
        print(s)
        #LeaveConversation1.flush(1)
        return s

    def flush(self):
        print("In flush")
        Variables.label = None
        Variables.Emp_id = 1029
        Variables.Emp_Name = 'Manjunath'
        Variables.leave_type = None
        Variables.From_date = None
        Variables.To_date = None
        Variables.Number_of_days = None
        # Variables.W2V_model = None
        # Variables.index2word_set = None
        # Variables.model_LG = None

    def check_entites(self):
        print(Variables.leave_type,Variables.From_date,Variables.To_date)
        if Variables.leave_type == None and Variables.From_date == None and Variables.To_date == None:
            return Conversation.Conversations.boot_conversations[0]

        elif Variables.leave_type == None and Variables.From_date != None and Variables.To_date == None:
            return Conversation.Conversations.boot_conversations[0]

        elif Variables.leave_type == None and Variables.From_date != None and Variables.To_date != None:
            return Conversation.Conversations.boot_conversations[0]

        elif Variables.leave_type != None and Variables.From_date == None and Variables.To_date == None:
            return Conversation.Conversations.boot_conversations[2]

        elif Variables.leave_type != None and Variables.From_date != None and Variables.To_date == None:
            return Conversation.Conversations.boot_conversations[3]

        elif Variables.leave_type != None and Variables.From_date != None and Variables.To_date != None:
            return LeaveConversation1.Summary(2)


        else:
            print("In else block of Leave conversation")
            return "Done"
    def set_entities(text):
        if  Variables.leave_type ==None and Variables.From_date == None and Variables.To_date == None:
            Variables.leave_type=LeaveConversation1.extract_leave_type(text)
            dates = LeaveConversation1.extract_date(text)
            LeaveConversation1.set_dates(dates)
            print(Variables.leave_type,Variables.From_date,Variables.To_date)

        elif Variables.leave_type == None and Variables.From_date != None and Variables.To_date != None:
            Variables.leave_type=LeaveConversation1.extract_leave_type(text)

        elif Variables.leave_type == None and Variables.From_date != None and Variables.To_date == None:
            Variables.leave_type=LeaveConversation1.extract_leave_type(text)

        elif Variables.leave_type !=None and Variables.From_date == None and Variables.To_date == None:
            dates=LeaveConversation1.extract_date(text)
            LeaveConversation1.set_dates(dates)

        elif Variables.leave_type != None and Variables.From_date != None and Variables.To_date == None:
            dates=LeaveConversation1.extract_date(text)
            Variables.To_date=dates[0]
            #LeaveConversation1.set_dates(dates)


    # Once everything is ready it will ask the user whether you want to change some entities.
    def Confirm_Change(text):
        #print(Conversation.Conversations.boot_conversations[5])
        if text.lower() == 'confirm':
            LeaveConversation1.flush(1)
            print("in confirm")
            return Conversation.Conversations.boot_conversations[7]
        elif text.lower() == 'change':
            LeaveConversation1.flush(1)
            return Conversation.Conversations.boot_conversations[6]
        else:
            return 1
    def main(text):
        if LeaveConversation1.Confirm_Change(text)==1:
            LeaveConversation1.set_entities(text)
            print(4)
            return LeaveConversation1.check_entites(text)
        else:
            print("in else")
            return LeaveConversation1.Confirm_Change(text)
