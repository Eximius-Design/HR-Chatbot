import datetime


class Conversations:
    boot_conversations = [
    "Which type of leave do you want to apply? \n 1.Sick Leave \n  2.Privilege Leave \n  3.Maternity Leave \n  4.Paternity Leave \n  5.Bereavement Leave",
    'Let me assist you with sick leave . You can type cancel to exit this conversation at any time. From which date to which date you need sick leave?',
    'Please enter Start date and End date of your leave',
    'Please enter End date',
    'Ok Got it.Here is summary of Conversation',
    '1.Confirm 2.Modify',
    'You can re-enter the details from beginning',
    'Ok Your leave is being processed. You can check approval status at www.eximiusdesign.com/leave_status',
    '<li>Here is the list of holidays</li>',
        ". %s is a holiday",
        ". %s is not a holiday",
        'There are no holidays from %s to %s',
        'Here is the list of holidays ',
        "There is no holiday",
        "There is/are only %s holiday/holidays",
        "Totally there are %s holidays between %s and %s",
        "There are no holidays from %s to %s",
        "There is only %s holiday from %s to %s",#d
        "Totally there are %s holidays %s to %s",
    "Sorry I didn't understand this!",
    "Got it. Have a good day!!!",
    "How can I help you?"]

    labels=["Holiday","Leave","Welcome","GoodBye","FAQ"]
    Thanks_replays=["It is my pleasure.","I am glad to do that.","You're very welcome.","Don't mention it.",
                    "No Problem.","Anytime.","Sure."]

    def Hi_Replay(self):
        currentTime = datetime.datetime.now()
        if currentTime.hour < 12:
            return 'Good morning Manju. '+Conversations.boot_conversations[-1]
        elif 12 <= currentTime.hour < 18:
            return 'Good Afternoon Manju. ' + Conversations.boot_conversations[-1]
        else:
            return 'Good Evening Manju. ' + Conversations.boot_conversations[-1]

#These are used for regular flask app which uses html to display messages
# boot_conversations = [
#     "Which type of leave do you want to apply?<br> 1.Sick Leave<br> 2.Privillage Leave<br> 3.Maternity Leave <br> 4.Paternity Leave <br> 5.Bereavement Leave",
#     'Let me assist you with sick leave . You can type cancel to exit this conversation at any time. From which date to which date you need sick leave?',
#     'Please enter the From date and to date',
#     'Please enter to date',
#     'Ok Got it.Here is summary of Conversation',
#     '1.Confirm 2.Change',
#     'You can re-enter the datails from begining',
#     'Ok Your leave is being processed. You can check approval status at www.eximiusdesign.com/leave_status',
#     'Here is the list of holidays',
#         ". %s is a holiday",
#         ". %s is not a holiday",
#         'There are no holidays from %s to %s',
#         'Here is the list of holidays ',
#         "There is no holiday",
#         "There is only %s holiday",
#         "Totally there are %s holidays",
#         "There are no holidays from %s to %s",
#         "There is only %s holiday from %s to %s",
#         "Totally there are %s holidays %s to %s",
#     "Sorry I didn't understand this!",
#     "Got it. We'll meet again"]
