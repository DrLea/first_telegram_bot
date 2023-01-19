import telebot
from telebot import types
import datetime
import signal




print("Server was launched at " + str(datetime.datetime.now()))

bot = telebot.TeleBot("")
users = []
list = []
weekday = ["monday", "tuesday", "wednesday", "thursday", "friday"]
takeRoom = False
d1,d2,d3,d4,d5 = False,False,False,False,False

class User:
    def __init__(self, username, name, id):
        self.schedule = {"monday": "", "tuesday": "", "wednesday": "", "thursday": "", "friday": ""}
        self.username = username
        self.name = name
        self.chat = id

    room = 0

    def discribe(self):

        if self.username:
            return (str(self.username) + " - " + str(self.name) + "  room: " + str(self.room) + "\n")
        else:
            return ("No(ID) - " + str(self.name) + "  room: " + str(self.room) + "\n")


def handler(signum, frame):
    print("Server was interupted at " + str(datetime.datetime.now()))


    exit(0)

signal.signal(signal.SIGINT, handler)

def find(s):
    for user in users:
        if user.chat == s:
            return user
    return 0

def reg(message):
    global takeRoom

    if find(message.chat.id):
        takeRoom = True
        bot.send_message(message.chat.id, "Input your room number (300<x<500):")
    else:
        users.append(User(message.from_user.username, message.from_user.first_name, message.chat.id))
        list.append(message.chat.id)
        bot.send_message(message.chat.id, "Input your room number (300<x<500):")
        takeRoom = True

def validator(s):
    if len(s)==5:
        return ((s[0]+s[1]).isnumeric()) and s[2]==":" and ((s[3]+s[4]).isnumeric()) and int(s[0]+s[1])>=6 and int(s[0]+s[1])<20 and int(s[3]+s[4])>=0 and int(s[0]+s[1])<60


def timer(a):
    t = 0
    if len(a)==5:
        t = int(a[0]+a[1])*60 + int(a[3] + a[4])
    return t

def coPass(a, b):
    txt = "\n"
    for user in users:
        c = timer(user.schedule[weekday[datetime.datetime.today().weekday()]]) - timer(a)
        if c>=-30 and c<=30 and user.chat != b:
            txt += user.name + " @" + (user.username if user.username else "") + " room: " + str(user.room) + f" ({user.schedule[weekday[datetime.datetime.today().weekday()]]})" + "\n"
    return txt





@bot.message_handler(commands = ["start"])
def start(message):
    if((message.chat.id in list)):
        text = f"Good day <b>{message.from_user.first_name}</b> \nYou are already user of DormDrive\nEnter /help to get more info\n"
        bot.send_message(message.chat.id, text, parse_mode="html")
    else:
        text = f"Good day <b>{message.from_user.first_name}</b> \nWelcome to DormDrive\n"
        bot.send_message(message.chat.id, text, parse_mode="html")
        reg(message)




@bot.message_handler(commands= ["help"])
def helper(message):
    text = ""
    text = text + "ID: " + str(message.chat.id) + "\n"
    if find(message.chat.id):
        text = text + "Room #" + str(find(message.chat.id).room) + "\n"
    text = text + "Name: " + str(message.from_user.first_name) + " - " + str(message.from_user.username) + "\n\n"
    text = text + "Enter /update to refresh your information\n"
    text = text + "Enter /find to find the coPassengers\n"
    text = text + "Enter /timetable to change it"

    bot.send_message(message.chat.id, text, parse_mode="html")

@bot.message_handler(commands= ["update"])
def update(message):
    reg( message)

@bot.message_handler(commands = ["timetable"])
def timetable(message):
    if not(find(message.chat.id)):
        bot.send_message(message.chat.id, "\n/start first\n")
        return
    markup = types.ReplyKeyboardMarkup(row_width=3)
    if find(message.chat.id):
        mon = types.KeyboardButton("Monday" + "\n" + str(find(message.chat.id).schedule["monday"]))
        tue = types.KeyboardButton("Tuesday" + "\n" + str(find(message.chat.id).schedule["tuesday"]))
        wed = types.KeyboardButton("Wednesday" + "\n" + str(find(message.chat.id).schedule["wednesday"]))
        thu = types.KeyboardButton("Thursday" + "\n" + str(find(message.chat.id).schedule["thursday"]))
        fri = types.KeyboardButton("Friday" + "\n" + str(find(message.chat.id).schedule["friday"]))
    else:
        mon = types.KeyboardButton("Monday")
        tue = types.KeyboardButton("Tuesday")
        wed = types.KeyboardButton("Wednesday")
        thu = types.KeyboardButton("Thursday")
        fri = types.KeyboardButton("Friday")
    markup.add(mon,tue,wed,thu,fri)
    bot.send_message(message.chat.id,"\nwhich day to change\n" , reply_markup=markup)







@bot.message_handler(commands = ["find"])
def findCo(message):
    global weekday
    if find(message.chat.id):
        if find(message.chat.id).schedule[weekday[datetime.datetime.today().weekday()]] != "":
            bot.send_message(message.chat.id, f"\n<b>{weekday[datetime.datetime.today().weekday()]}"
                                          f"</b>, your classes start at {find(message.chat.id).schedule[weekday[datetime.datetime.today().weekday()]]}\n",
                         parse_mode="html")
            bot.send_message(message.chat.id,f"Your possible co-passangers are:"
                                             f"\n{coPass(find(message.chat.id).schedule[weekday[datetime.datetime.today().weekday()]], message.chat.id)}\n")
        else:
            bot.send_message(message.chat.id, "\nFill /timetable first\n")
    else:
        bot.send_message(message.chat.id, "\n/start first\n")

@bot.message_handler(commands = ["sudo"])
def sudo(message):
    if message.chat.id == 290462342:
        counter = 1
        for user in users:
           bot.send_message(message.chat.id, "\nuser " + str(counter) + " : \n" + user.discribe()) 
           counter+=1
    else: 
        bot.send_message(message.chat.id, "\nyou are not admin\n")


@bot.message_handler(content_types="text")
def say(message):
    global takeRoom
    global d1,d2,d3,d4,d5
    if takeRoom:
        if message.text.isnumeric():

            if int(message.text)>=300 and int(message.text)<500:
                if find(message.chat.id):
                    find(message.chat.id).room = int(message.text)
                    takeRoom = False
                    bot.send_message(message.chat.id, "Room number was updated\nEnter /help to get more info\n", parse_mode="html")
                else:
                    bot.send_message(message.chat.id, "\nERROR\n",parse_mode="html")

            else:
                bot.send_message(message.chat.id, "\nYour room # (300<x<500)Only is valid: \n")

        else:
            bot.send_message(message.chat.id, "\nYour room # (300<x<500)Only is valid: \n", parse_mode="html")

    elif str(message.text).split()[0] == "Monday":
        d1 = True
        bot.send_message(message.chat.id, "\nInput first class start time in (hh:mm) format\n")
    elif str(message.text).split()[0] == "Tuesday":
        d2 = True
        bot.send_message(message.chat.id, "\nInput first class start time in (hh:mm) format\n")
    elif str(message.text).split()[0] == "Wednesday":
        d3 = True
        bot.send_message(message.chat.id, "\nInput first class start time in (hh:mm) format\n")
    elif str(message.text).split()[0] == "Thursday":
        d4 = True
        bot.send_message(message.chat.id, "\nInput first class start time in (hh:mm) format\n")
    elif str(message.text).split()[0] == "Friday":
        d5 = True
        bot.send_message(message.chat.id, "\nInput first class start time in (hh:mm) format\n")

    elif d1 and find(message.chat.id):
        if validator(message.text):
            find(message.chat.id).schedule["monday"] = message.text
            d1 = False
            bot.send_message(message.chat.id, "\nTime changed /timetable\n")
        else:
            bot.send_message(message.chat.id, "\nInvalid input\nInput time in (hh:mm) format (06:00<x<20:59): \n")
    elif d2 and find(message.chat.id):
        if validator(message.text):
            find(message.chat.id).schedule["tuesday"] = message.text
            d2 = False
            bot.send_message(message.chat.id, "\nTime changed /timetable\n")
        else:
            bot.send_message(message.chat.id, "\nInvalid input\nInput time in (hh:mm) format (06:00<x<20:59): \n")
    elif d3 and find(message.chat.id):
        if validator(message.text):
            find(message.chat.id).schedule["wednesday"] = message.text
            d3 = False
            bot.send_message(message.chat.id, "\nTime changed /timetable\n")
        else:
            bot.send_message(message.chat.id, "\nInvalid input\nInput time in (hh:mm) format (06:00<x<20:59): \n")
    elif d4 and find(message.chat.id):
        if validator(message.text):
            find(message.chat.id).schedule["thursday"] = message.text
            d4 = False
            bot.send_message(message.chat.id, "\nTime changed /timetable\n")
        else:
            bot.send_message(message.chat.id, "\nInvalid input\nInput time in (hh:mm) format (06:00<x<20:59): \n")
    elif d5 and find(message.chat.id):
        if validator(message.text):
            find(message.chat.id).schedule["friday"] = message.text
            d5 = False
            bot.send_message(message.chat.id, "\nTime changed /timetable\n")
        else:
            bot.send_message(message.chat.id, "\nInvalid input\nInput time in (hh:mm) format (06:00<x<20:59): \n")

    else:
        bot.send_message(message.chat.id, "\nEnter /help to get more info\n", parse_mode="html")


bot.polling(none_stop=True)
