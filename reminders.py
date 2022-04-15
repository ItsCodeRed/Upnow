import datetime
from tkinter import font
import tkinter as tk
import subprocess

#all non interuptable programs
nonInteruptablePrograms = ["RocketLeague.exe", "Bandicam.exe", "SteamVR.exe", "LeagueOfLegends.exe", "Minecraft.exe", "Rust.exe", "Warzone.exe"]

# creates the main tkinter instance
root = tk.Tk()
root.title("Upnow")

# width and height of the window
height = 500
width = 850

# setting up the fonts that I use later
normFont = font.Font(family = "Kabel", size = 12)
boldFont = font.Font(family = "Kabel", size = 24, weight = "bold")
mainFont = font.Font(family = "Kabel", size = 36, weight = "bold")

# creates a start size for the window
canvas = tk.Canvas(root, name = "upnow", width = width, height = height)
canvas.pack()

# creates a nice dark blue background
background = tk.Frame(root, bg = '#223544')
background.place(relwidth = 1, relheight = 1)

# a lighter blue area, for all the settings
settingsFrame = tk.Frame(root, bg = '#bbcedd')
settingsFrame.place(relx = 0.0625, rely = 0.1, relwidth = 0.875, relheight = 0.35)

# another frame for the messages
messageFrame = tk.Frame(root, bg = '#bbcedd')
messageFrame.place(relx = 0.0625, rely = 0.55, relwidth = 0.875, relheight = 0.35)

# message window that actually tells you to stand
messageVar = tk.StringVar()
message = tk.Label(messageFrame, bg = '#3c566a', fg = '#ffffff', font = boldFont, textvariable=messageVar)

# list of the future times
futureVar = tk.StringVar()
futureTimes = tk.Label(messageFrame, bg = '#3c566a', fg = '#ffffff', font = normFont, textvariable=futureVar)

mainlLabel = tk.Label(settingsFrame, text = "Upnow™", bg = '#3c566a', fg = '#ffffff', font = mainFont, anchor = "n")
mainlLabel.place(relx = 0.32, rely = 0.05, relwidth = 0.36, relheight = 0.9)

# set button that, when clicked, will save any settings selected
setButton = tk.Button(settingsFrame, text = "Apply", bg = '#3c566a', fg = '#ffffff', font = boldFont, command = lambda:
        saveSettings())
setButton.place(relx = 0.33, rely = 0.56, relwidth = 0.34, relheight = 0.36)

# dropdown with all the settings for the interval between reminders
intervalDropdown = tk.Listbox(settingsFrame,
        height = 8, width = 10, bg = '#3c566a', fg = '#ffffff', font = normFont, highlightcolor = '#3c566a')
intervalDropdown.insert(1, "15 minutes")
intervalDropdown.insert(2, "30 minutes")
intervalDropdown.insert(3, "45 minutes")
intervalDropdown.insert(4, "1 hour")
intervalDropdown.insert(5, "1 hour and 30 minutes")
intervalDropdown.insert(6, "2 hours")
intervalDropdown.place(relx = 0.01, rely = 0.2, relwidth = 0.3, relheight = 0.75)

# the label for the previously mentioned dropdown
intervalLabel = tk.Label(settingsFrame, text = "Time between stands:", bg = '#3c566a', fg = '#ffffff', font = normFont)
intervalLabel.place(relx = 0.01, rely = 0.05, relwidth = 0.3, relheight = 0.15)

# the dropdown for how long you want to stand each time
standTimeDropdown = tk.Listbox(settingsFrame,
        height = 8, width = 10, bg = '#3c566a', fg = '#ffffff', font = normFont, highlightcolor = '#3c566a')
standTimeDropdown.insert(1, "10 seconds")
standTimeDropdown.insert(2, "30 seconds")
standTimeDropdown.insert(3, "1 minute")
standTimeDropdown.insert(4, "2 minutes")
standTimeDropdown.insert(5, "3 minutes")
standTimeDropdown.insert(6, "5 minutes")
standTimeDropdown.place(relx = 0.69, rely = 0.2, relwidth = 0.3, relheight = 0.75)

# label for the dropdown
standTimeLabel = tk.Label(settingsFrame, text = "Standing time:", bg = '#3c566a', fg = '#ffffff', font = normFont)
standTimeLabel.place(relx = 0.69, rely = 0.05, relwidth = 0.3, relheight = 0.15)

class upNow: # the main class. Contains some variables and functions used through out the program
    # all the main variables used:
    interval = 60
    upTime = 60
    time = datetime.datetime.now()
    reminded = False
    endTime = 0
    upTimes = \
        [time + datetime.timedelta(minutes = interval),
         time + datetime.timedelta(minutes = interval * 2),
         time + datetime.timedelta(minutes = interval * 3),
         time + datetime.timedelta(minutes = interval * 4),
         time + datetime.timedelta(minutes = interval * 5),
         time + datetime.timedelta(minutes = interval * 6)
         ]


    def changeTimes(): # changes the future times
        upNow.upTimes = \
            [upNow.time + datetime.timedelta(minutes=upNow.interval),
             upNow.time + datetime.timedelta(minutes=upNow.interval * 2),
             upNow.time + datetime.timedelta(minutes=upNow.interval * 3),
             upNow.time + datetime.timedelta(minutes=upNow.interval * 4),
             upNow.time + datetime.timedelta(minutes=upNow.interval * 5),
             upNow.time + datetime.timedelta(minutes=upNow.interval * 6)
             ]
        setMessages()

def loop(): # sets current time, and checks if it's time to stand
    upNow.time = datetime.datetime.now()
    checkForStand()
    root.after(50, loop)

def checkForStand():
    endTime = upNow.upTimes[0] + datetime.timedelta(seconds=upNow.upTime) # sets the time that you should stop standing
    if is_time_between(upNow.upTimes[0], endTime, upNow.time) and not nonInteruptablesOpen(): # if the time is between the end time and the time we should stand
        if not upNow.reminded: # actually reminds the user
            upNow.reminded = True
            time = endTime.strftime("%I:%M:%S %p")
            messageVar.set("Time to get up!\nYou can sit down at\n" + str(time))
        # brings the window to the front
        root.attributes("-topmost", True)
        root.state('zoomed')
    elif upNow.time >= endTime:     # checks if the time for standing is done
        upNow.reminded = False
        upNow.changeTimes()

def is_time_between(begin_time, end_time, check_time=None): # checks if a time is between to other times
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def nonInteruptablesOpen():
    for program in nonInteruptablePrograms:
        if (processExists(program)):
            return True
    return False

def saveSettings(): # runs when the user presses the apply button
    if (len(intervalDropdown.curselection()) == 1):
        upNow.interval = toTime(intervalDropdown.get(intervalDropdown.curselection()[0]), "minutes")
        upNow.changeTimes()
    if (len(standTimeDropdown.curselection()) == 1):
        upNow.upTime = toTime(standTimeDropdown.get(standTimeDropdown.curselection()[0]), "seconds")
        upNow.changeTimes()\

def processExists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # check in last line for process name
    last_line = subprocess.check_output(call).strip()
    # because Fail message could be translated
    return (len(last_line) > 100)

def toTime(timeInWords, units): # converts the time into units that we can use to calculate the future times
    timeInUnits = 0
    lastSpace = 0
    num = 0
    sentence = ["", "", "", "", "", "", "", ""]
    for i, c in enumerate(timeInWords): # runs through all the letters in the option we selected
        if c == ' ': # if it's a space, we save the previous letter up to the last space into an array
            sentence[num] = timeInWords[lastSpace:i]
            lastSpace = i + 1
            num = num + 1
        if i == len(timeInWords) - 1: # if this is the last index, we also treat it like a space
            sentence[num] = timeInWords[lastSpace:i + 1]
            lastSpace = i
            num = num + 1

    # runs through all the words we gathered
    for var in sentence:
        # if we find the word "seconds", then we go to the previous word (a number) and convert it into seconds
        if var == "seconds":
            timeInUnits = timeInUnits + int(sentence[sentence.index(var) - 1])
        # if we find the word "minute" or "minutes", then we go to the previous word (a number) and convert it into minutes
        if var == "minute" or var == "minutes":
            if units == "seconds":
                timeInUnits = timeInUnits + int(sentence[sentence.index(var) - 1]) * 60
            if units == "minutes":
                timeInUnits = timeInUnits + int(sentence[sentence.index(var) - 1])
        # if we find the word "hour" or "hours", then we go to the previous word (a number) and convert it into hours
        if var == "hour" or var == "hours":
            timeInUnits = timeInUnits + int(sentence[sentence.index(var) - 1]) * 60

    return timeInUnits # returns our new-found units

def setMessages(): # sets the message boxes to useful info
    nextTimes = [0,0,0,0,0,0]
    for i in range(0, 6): # runs through all the future times, and converts them into AM/PM and without the date
        nextTimes[i] = upNow.upTimes[i].strftime("%I:%M:%S %p")
    if upNow.upTime >= 60: # converts the time we should stand back into something readable
        if upNow.upTime / 60 == 1:
            standTime = str(int(upNow.upTime / 60)) + " minute"
        else:
            standTime = str(int(upNow.upTime / 60)) + " minutes"
    else:
        standTime = str(upNow.upTime) + " seconds"
    # sets all the messages accordingly
    futureVar.set("You will be reminded to\nstand for " + str(standTime) +
                  " at\n" + str(nextTimes[0]) + ",\n" + str(nextTimes[1]) + ",\n"
                  + str(nextTimes[2]) + ",\n" + str(nextTimes[3]) + ",\n"
                  + str(nextTimes[4]) + ",\n and " + str(nextTimes[5]) + ".")
    messageVar.set("Next reminder at:\n" + str(nextTimes[0]))
    message.place(relx=0.32, rely=0.05, relwidth=0.67, relheight=0.9)
    futureTimes.place(relx=0.01, rely=0.05, relwidth=0.3, relheight=0.9)

setMessages() # sets the messages initially

root.after(50, loop) # gives our loop some time to loop while the tkinter main loop goes
root.mainloop() # runs the tkinter main loop
