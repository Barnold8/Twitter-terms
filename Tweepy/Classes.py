import tweepy as twp
import json
from tkinter import *
from tkinter.ttk import Progressbar
import threading
import time
import random                       #All of the imports that make the program possible.
from random import randint
import tkinter.messagebox           #Importing modules means that in the background all the code that is from these modules is pasted into this file so the code can be used
# import math
import pyfiglet
import sys

get_stream = False      #This boolean variable was probably needed for logic at runtime, but cannot be found later on in the program

objects = [] #This keeps track of all the window objects during runtime
stream_data = {}  # Used for a workaround to get data for the hangman game. Im not sure how tweepy handles its data properly so on stream.start, the data is fed into here
special_checker = ["!", '"', "'", "£", "%", "&", "*", "(", ")", "-", "_", "=", "+", "`", "¬", "''", "|", "\\", ",", "<",
                   ".", ">", ";", ":", "@", "#", "~", "{", "}", "[",
                   "]", " ", "?", "/", "§", "¨", "©", "ª", "¯", "°", "±", "²", "³",         #This is an array of all the special characters that I could find. This is for logic, so when a user is inputting text they cant input any of these
                   "»", "«", "¼", "½", "¾", "¿", "ƒ", "ˆ",
                   "ˇ", "˘", "˙", "˛", "˜", "˝", "–", "—", "‘", "’", "‚", "“", "”", "„", "†", "‡", "•", "…", "‰", "‹",
                   "›", "€", "™", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "😭", "💕"]

API_KEY = ""
API_SECRET_KEY = ""  # API KEYS
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""  # AUTHORISATION KEYS

auth = twp.OAuthHandler(API_KEY, API_SECRET_KEY)            #Authorise this program with twitter
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

DAT = ""  #This string variable was probably needed for logic at runtime, but cannot be found later on in the program
counter = 0 #This integer variable was probably needed for logic at runtime, but cannot be found later on in the program

class Window(Tk): #This class inherits from the Tk class
    # this is the default window class
    def __init__(self, title="Default", geom="250x250+500+600", data="Default", is_menu=True, canvas=False):            #Any window that is created will have the following data at runtime. Parameters that have = are predefined, the parameter here is the constructor
        super().__init__()   #Super  makes it so the inheritance goes through                                           #This means that we can default states for our objects

        try:
            del objects[len(objects) - 1]           #This code deletes the last window that existed, this keeps our object list at the length of 1. Saves on memory and processing
        except Exception as e:                         #The try and except is here for the time that no previous windows existed (when the program runs for the first time)
            print("Error returned by program {}".format(e))

        self.resizable(0, 0)    #This makes it so the window cannot be resized
        self.title(title)       #The title that is passed through the constructor is the title for the window
        self.geometry(geom)     #the geometry that is passed through the constructor is the geometry for the window
        self.overrideredirect(1) #This removes the title bar by default
        self.running = False        #This sets the running variable to a false state, this is to stop logic for the shape on the splash screen to stop, saves on processing


        self.data = data  # This is to track the last window opened. When the user clicks "back" on the help screen, it will take them to the window they were just on

        if is_menu:         #This checks the parameter for the object is_menu. This determines if the window has a menu strip or not, this is useful for informative windows
            self.menu = Menu(self) #starts the menu object

            self.config(bg="black", menu=self.menu) #configures the background and menu

            # File MENU-----------------------------
            fileMenu = Menu(self.menu, tearoff=False)
            self.menu.add_cascade(label="Main", menu=fileMenu)

            # File menu commands ----------------------------------
            fileMenu.add_command(label="Main Menu", command=self.Main_Menu_Start)
            fileMenu.add_command(label="Hangman", command=self.Hangman)
            fileMenu.add_command(label="Tweet search", command=self.Tweet_Search)
            fileMenu.add_command(label="Help", command=self.Help)
            fileMenu.add_command(label="Exit", command=self.exit)

            # Edit MENU------------------------------------
            editMenu = Menu(self.menu, tearoff=False)
            self.menu.add_cascade(label="Settings", menu=editMenu)
            editMenu.add_command(label="Title Bar", command=self.title_bar)
            editMenu.add_command(label="Change Background", command=self.change_bg)

            self.bind("<Button-3>", self.alt_menu)      #Binds the window frame to check for right clicks. When the right click has been detected, it runs the self.alt_menu function

        self.tracker = 0

    # -----------------  CODE HERE HAS BEEN TURNED INTO COMMENTS, THIS IS SO I CAN KEEP THE CODE FOR AN EXAMPLE AS WHAT I HAD BEFORE I CHANGED TO A MENU STRIP.-----------------------------------
    # self.b_text = StringVar()
    # self.b_text.set("Drag-able")
    # self.title_change = Button(self,width=10,textvariable=self.b_text,command=self.title_bar)
    # self.title_change.pack()
    # self.title_change.place(relx=b_locx,rely=b_locy)
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def title_bar(self):
        self.tracker += 1
        # print(self.tracker)

        if self.tracker >= 2:
            self.tracker = 0                    #This function iterates one variable, if the variable is 2 or more, get rid of the title bar and set the variable back to 0, (this is so we can use the function indefinitely) else, bring the title bar back
            self.overrideredirect(1)

            # self.b_text.set("Drag-able")
        elif self.tracker == 1:
            self.overrideredirect(0)
            # self.b_text.set("Default")

    # Main Windows-----------------------------------
    def Help(self):

        help_x_axis = 0.38
        try:
            ms_info.destroy()

        except Exception as e:
            print(f"Dev thought error: ms_info doesnt exist yet\n\nError return: {e}")          #These try and excepts attempt to destroy the specific help windows when the main help window is called
                                                                                                #This is because each specific help window has a back button that takes the user back to the main help window
        try:                                                                                    #So when this happens, the specific help window will be destroyed
            ts_info.destroy()
        except Exception as e:
            print(f"Dev thought error: ts_info doesnt exist yet\n\nError return: {e}")

        try:
            hm_info.destroy()
        except Exception as e:
            print(f"Dev thought error: hm_info doesnt exist yet\n\nError return: {e}")



        def ret():
            help_window.destroy()

            if past_window == "Main_Menu":
                Main_Menu(self)

            elif past_window == "Hang_Man":         #this function returns the user to the window they were on before the main help window
                Hangman_start(self)                 #This is done by grabbing the data from the data variable found in the window constructor

            elif past_window == "Tweet_Search":
                self.Tweet_Search()

                # WINDOW COMMANDS - HELP

        def Menu_strip_info():                  #This function brings up the specific help window for the menu strip

            def maininfo():
                tkinter.messagebox.showinfo(master=ms_info,title="Main",message="The main menu option brings you back to the main menu\n\nThe hangman "
                                                   "option lets you play hangman, the word is decided by twitter!\n\n"
                                                   "The tweet search option lets you find a recent tweet and write the information"                                 #Tkinter info alert 
                                                   " from said tweet to a file!\n\n"                                                                                
                                                    "The help option brings you to the selection screen that let's you find the information that you need!\n\n"
                                                   "The exit option lets you close the window.NOTE: The program is still running in the background and will have "
                                                   "to be terminate by task manager (Working on a fix)")


            def settings_info():
                tkinter.messagebox.showinfo(master=ms_info,title="Settings",message="The title bar option allows you to bring the top part of the window back, or it lets you take it away."
                                                                                    "The use of this is so you can drag the window around, this works for all windows\n\nThe change background option allows you to " #Tkinter info alert 
                                                                                    "change the colour of the background. NOTE: the background for things like text boxes will stay the default colour (black)")

            global ms_info #This global is here so the main help window can attempt to destroy it
            ms_info = Window(geom="300x300+600+400", title="Menu strip info")            #Window object
            help_window.destroy() #destroys the main help window

            title= Label(ms_info, width=20, text="Menu Strip Help", font=("Times new roman", 20), fg="white",bg="black")            #Label object
            title.pack()

            main_help = Button(ms_info, text="Main", width=10, command=maininfo)
            main_help.pack()
            main_help.place(relx=help_x_axis,rely=0.25)

            settings_help = Button(ms_info, text="Settings", width=10, command=settings_info)
            settings_help.pack()
            settings_help.place(relx=help_x_axis, rely=0.55)

            Back = Button(ms_info, width=10, text="<<<< Back", command=self.Help)
            Back.pack()
            Back.place(relx=0.65,rely=0.85)
            ms_info.mainloop()


        def Tweet_search_info():         #This function brings up the specific help window for the tweet search window
            global ts_info #This global is here so the main help window can attempt to destroy it
            ts_info = Window(geom="300x300+600+400", title="Twitter search info")
            help_window.destroy() #destroys the main help window


            title = Label(ts_info, width=20, text="Tweet Search Help", font=("Times new roman", 20), fg="white",
                          bg="black")
            title.pack()


            def radio_button():

                x = Window(is_menu=False, geom="700x500+500+100")

                x.config(bg="black")

                canvas = Canvas(master=x, width=700,height=700,bg="black",highlightthickness=0)
                canvas.pack()
                info_img = PhotoImage(master=x,file="External/Radio_Button2.png")
                canvas.create_image(350,250,image=info_img)

                e = Button(x, width=30, text="Click this to exit help screen", command= lambda: x.destroy())
                e.pack()
                e.place(relx=0.6,rely=0.9)


                x.mainloop()

            radio_buttons = Button(ts_info, command=radio_button, text="Info", width=10)
            radio_buttons.pack()
            radio_buttons.place(relx=0.4,rely=0.35)


            Back = Button(ts_info, width=10, text="<<<< Back", command=self.Help)
            Back.pack()
            Back.place(relx=0.65, rely=0.85)
            ts_info.mainloop()

        def Hangman_info():          #This function brings up the specific help window for the menu strip
            global hm_info #This global is here so the main help window can attempt to destroy it

            def rules_info ():
                tkinter.messagebox.showinfo(master=hm_info,title="Rules",message="\nFor the menu\n\n\n"
                                                                                 "You must input a word that is either 2 or more characters long\n\n"
                                                                                 "No special characters like '!','&','@' are allowed\n\n"
                                                                                 "You cannot have more than one word"
                                                                                 "\n\n"
                                                                                 "\n\nFor the game\n\n"
                                                                                 "For each guess, correct or incorrect, you will lose a life. Keep in mind, the man is hanging there\n\n"
                                                                                 "You can only have one letter responses\n\n"
                                                                                 "You cannot have special characters as a guess\n\n"
                                                                                 "\n\n"
                                                                                 "                                  NOTE:\n\n\n"
                                                                                 "This game is incredibly buggy so if the game isnt working, feel free to click the hangman button on the menu strip"
                                                                                 "\n\n\nAbove all else,\n\n"
                                                                                 "Have fun!")

            def hm_menu():
                x = Window(is_menu=False, geom="700x500+500+100", title="Hangman info")

                x.config(bg="black")

                canvas = Canvas(master=x, width=700, height=700, bg="black", highlightthickness=0)
                canvas.pack()
                info_img = PhotoImage(master=x, file="External/Hangman_menu.png")
                canvas.create_image(350, 250, image=info_img)

                e = Button(x, width=30, text="Click this to exit help screen", command=lambda: x.destroy())
                e.pack()
                e.place(relx=0.6, rely=0.9)

                x.mainloop()



                Back = Button(x, width=10, text="<<<< Back", command=self.Help)
                Back.pack()
                Back.place(relx=0.65, rely=0.85)


            def hm_game():
                x = Window(is_menu=False, geom="700x500+500+100",title="Hangman info")

                x.config(bg="black")

                canvas = Canvas(master=x, width=700, height=700, bg="black", highlightthickness=0)          #This canvas is here so I can place images upon it
                canvas.pack()
                info_img = PhotoImage(master=x, file="External/Hangman_Game.png")               #I can use this image on the canvas object to avoid a lot of programming of text and/or shapes
                canvas.create_image(350, 250, image=info_img)

                e = Button(x, width=30, text="Click this to exit help screen", command=lambda: x.destroy())         #This button has a lambda function, this allows me to give the button a function without having to write and actual function for it
                e.pack()
                e.place(relx=0.6, rely=0.9)

                x.mainloop()

                Back = Button(x, width=10, text="<<<< Back", command=self.Help)
                Back.pack()
                Back.place(relx=0.65, rely=0.85)

            hm_info = Window(geom="300x300+600+400",title="Hangman info")    #Window object
            help_window.destroy() #destroys the main help window

            title = Label(hm_info, width=20, text="Hangman Help", font=("Times new roman", 20), fg="white",
                          bg="black")
            title.pack()

            rules = Button(hm_info,width=10,text="Rules", command=rules_info)
            rules.pack()
            rules.place(relx=help_x_axis,rely=0.2)

            menu_info = Button(hm_info, width=10, text="Menu", command=hm_menu)
            menu_info.pack()
            menu_info.place(relx=help_x_axis, rely=0.4)

            game_info = Button(hm_info, width=10, text="Game", command=hm_game)
            game_info.pack()
            game_info.place(relx=help_x_axis, rely=0.6)


            Back = Button(hm_info, width=10, text="<<<< Back", command=self.Help)
            Back.pack()
            Back.place(relx=0.65, rely=0.85)
            hm_info.mainloop()

        help_window = Window(geom="300x250+400+400", title= "Help")
        objects.append(help_window)
        past_window = self.data

        try:
            self.destroy()
        except Exception as e:
            print(e)


        help_window.overrideredirect(1)

        return_b = Button(help_window, width=10, text="<<< Back", command=ret)
        return_b.pack()
        return_b.place(relx=0.7, rely=0.85)

        #What to help with | Menu Strip -Button (bring up new window with buttons, each buttons speaks about a specific component of the menu strip in detail) | Tweet search -Button (bring up new window with buttons, each buttons speaks about a specific component of Tweet search in detail | Hangman  -Button (bring up new window with buttons, each buttons speaks about a specific component of the Hangman game in detail))

        Menu_strip_info_button = Button(help_window, width=10, text="Menu Strip", command=Menu_strip_info)
        Menu_strip_info_button.pack()
        Menu_strip_info_button.place(relx=0.4,rely=0.25)

        Tweet_search_info_Button = Button(help_window, width=10, text="Tweet search", command=Tweet_search_info)                    #These are all the buttons for the main help window
        Tweet_search_info_Button.pack()
        Tweet_search_info_Button.place(relx=0.4,rely=0.45)


        Hangman_info_Button = Button(help_window, width=10, text="Hangman", command=Hangman_info)
        Hangman_info_Button.pack()
        Hangman_info_Button.place(relx=0.4,rely=0.65)

        help_title = Label(help_window, width=10,text="Help Window",font=("Times new roman",20),fg="white",bg="black")
        help_title.pack()
        help_title.place(relx=0.25,rely=0.0)


        help_window.mainloop()

    def Hangman(self):
        Hangman_start(self)

    def Tweet_Search(self):                     #These functions call their sub function which creates the corresponding window object
        Tweet_Search_Start(self)

    def Main_Menu_Start(self):
        self.destroy()
        Main_Menu(self)

    # ---------------------------------------------------------

    def alt_menu(self, event):              #This is the function that is called when the right click is detected, the event parameter is the information about the concurrent event caught
        self.menu.post(event.x_root, event.y_root)      #This puts a menu at the x and y position of the event

    def exit(self):
        self.destroy()              #The window is destroyed here
        sys.exit()              #sys.exit is attempted here to force stop the program but it doesnt do anything

    def change_bg(self):            #This function allows the user to change the background colour

        hex_part_array = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]           #These are all parts of hex from 0-F
        colour = "#"    #This is the start of the colour, this variable has hex_part_array parts added onto it for the final colour

        for add in range(6):        #For the length of a hex number
            colour += hex_part_array[randint(0, len(hex_part_array) - 1)]       #Add a random hex digit to it

        self.config(bg=colour)      #Configure the current window background to the made colour
        print(colour)


class Window_Handler(Window):           #This is the window handler class, it inherits from the window class and it is the first class to be called at runtime

    def __init__(self, title, geom, data, is_menu): #These are the parameters for the window handler class, they HAVE to have data
        super().__init__(title=title, geom=geom, data=data, is_menu=is_menu)        #the data is then fed into the super parameters which makes them the default for the window
        self.canv = Canvas(self, width=250, height=250, bg="black", bd=0, highlightthickness=0, relief='ridge') #this canvas allows for the use of the shape that you see on the splash screen
        self.x = 15     #Default x position for shape
        self.y = 15     #Default y position for shape
        self.running = True     #sets running to true so the shape can move
        self.rect = self.canv.create_rectangle(randint(25, 100), randint(25, 100), 35, 25,
                                               outline="#05f", fill="#05f")     #   creates the shape


        self.lab = Label(self, width=10, bg="black", fg="white", text="Loading...")
        self.lab.pack()
        self.lab.place(relx=0.37, rely=0.25)

        self.canv.pack()
        self.progress = Progressbar(self, orient=HORIZONTAL, length=100, mode='determinate', cursor='circle') #creates a progress bar object

        def progress_process(self):             #This is the function that handles the progress bar's loading process
            global thread_1, thread_2, thread_3

            def threaded():         #This function is designed to be put onto a thread, this is so the loading bar and the shape can be active in parallel
                self.progress.place(relx=0.32, rely=0.4)        #placement for the loading bar
                percent = 0
                while percent != 100:           #Run the code until the integer of the progress bar is less than 100
                    self.progress['value'] = percent #change the value of the progress bar by the percent variable
                    time.sleep(0.15)        #wait a fifteenth of a second
                    percent += 5        #every loop of this, add 5 to percent variable
                    print(percent)


                self.running = False
                self.progress.destroy()         #destroy the progress bar
                self.destroy()  #then destroy the window

                print("progress thread ended")
                thread_2._stop() #End the thread 2 thread

            def motion():

                colours = ["#FFFFFF", "#DF6060", "#DF6060", "#EF902F", "#FF8100", "#4D2F10", "#DFD825", "#FFF500",
                           "#E5E06D",
                           "#24FF00", "#7CD06E", "#20AB09", "#00FF60", "#45DF7F", "#0E893D", "#00491C", "#00FFFD",          #The hex values for the shape that moves
                           "#4CC2C1",
                           "#43095D", "#FF00F6", "#EE6BC2", "#AB1558", "#00FFB6", "#47D5AC"]

                while self.running:
                    try:
                        coordinates = self.canv.coords(self.rect)
                        if coordinates[0] >= 220:
                            self.x = -20

                        elif coordinates[1] >= 230:
                            self.y = -20                            #Simple collision detection for the sides of the winfow

                        elif coordinates[0] <= 0:                   #it checks the x and y position of the shape and checks if they are out of the boundaries of the window
                            self.x = 20

                        elif coordinates[1] <= 0:
                            self.y = 20

                        time.sleep(0.05)                #This is to stop the shape moving as rapid as possible
                        self.canv.move(self.rect, self.x, self.y)           #move the shape to the current coords based on the collision detection
                        self.canv.itemconfig(self.rect, fill=colours[randint(0, len(colours))], outline="black") #change the shapes colour each loop, the colour is chosen randomly out of the colours array
                        # print(coordinates[0], coordinates[1])


                    except Exception as e:
                        print("Window closed, error message: {}".format(e))
                print("motion thread ended")
            try:
                thread_3._stop()                #Attempt to stop thread_3
            except Exception as e:
                print(f"Thread_3 does not exist {e}")

            def main_menu():
                global running
                Main_Menu(self)
                try:
                    thread_1._stop()            #Stop thread 1
                except Exception as e:
                    print(e)

            thread_1 = threading.Thread(target=main_menu).start()       #Put the main menu onto a thread
            thread_2 = threading.Thread(target=threaded).start()
            thread_3 = threading.Thread(target=motion).start()              #Allow the motion to run parallel to other processes

        progress_process(self) #call the progress process, this function has the threaded process in it too


class StdListener(twp.StreamListener):          #This is the class that listens out for the tweets on the twitter stream

    def __init__(self, time_limit):         #The time limit parameter allows us to choose how long the listener is active for
        super(StdListener, self).__init__()     #Inherit the stream listener class into this one
        self.start_time = time.time()       #start time of the stream
        self.limit = time_limit                #limit of the stream time

    def on_data(self, raw_data):            #When data is detected function

        if time.time() - self.start_time < self.limit:      #Check if the time limit has been exceeded
            self.process_data(raw_data)     #Process the data
            return True
        else:
            return False        #End function

    def process_data(self, raw_data):
        global stream_data
        # print(type(raw_data))                 #This function processes the data

        x = raw_data        #The data from the listener is stored here

        # parsed = json.loads(x)
        # parsed_ = json.dumps(parsed, indent=4,sort_keys=True)

        parsed_ = json.loads(
            x)  # TYPE OF THIS VARIABLE IS DICT, this means we can go through the data via "keys". Keys have the data we need attached to them
        # print(type(parsed_))

        # file = open("TEST4.json","w")
        # file.write(str(parsed_))
        # file.close()
        # print(newdict)
        stream_data = parsed_       #the processed data is stored here

    def on_error(self, status_code):
        if status_code == 420:  # This function stops us from getting banned because the stream will still continue even if an error occurs, this if statement stops that
            return False


class StdStream: #This class allows me to start the stream based on our auth and listener object
    def __init__(self, listener):
        self.stream = twp.Stream(auth=auth, listener=listener)

    def start(self, keys):      #With this function we can filter what tweets we get based on keywords
        self.stream.filter(track=keys)


def Main_Menu(self):
    new = Window(geom="400x400+500+500", data="Main_Menu", canvas=True, title="Main Menu")

    objects.append(new) #append the window to the objects array
    debug_objects() #call the debug objects funtion

    while self.running: #while running is true, hide the main menu, then after that, show it
        new.attributes('-alpha', 0.0)

    new.attributes('-alpha', 1.0, '-topmost', 1) #show window
    custom = pyfiglet.Figlet(font="5lineoblique") #Main menu font

    ascii_menu = Label(new, width=50, height=30, text=custom.renderText("Main Menu"), fg="#00CCAA", bg="#000000") # Title label, uses PyFiglet module to create special text
    ascii_menu.pack()
    ascii_menu.place(relx=0.05, rely=-0.3)

    info = Label(new, text="Use the menu strips seen above to use this software!", width=40, fg="white", bg="black",
                 font=10)
    info.pack()
    info.place(relx=0.05, rely=0.7)

    # All the corresponding commented out code was functional to a certain degree. It had too much of an impact on performance and had to be cut for processing power
    # canvas = Canvas(new, width=400, height=400, bg="black", highlightthickness=0, relief='ridge')
    # canvas.pack()

    # canvas.create_text(200, 100, fill=main_menu_color, font="Calibri 50 italic bold",
    #                 text="Main Menu")

    # canvas.create_text(200, 200, fill=main_menu_color, font="Calibri 15 bold",
    #                 text="To use this software, \nplease use the toolbar seen above.")

    # canvas.create_text(200, 300, fill=main_menu_color, font="Calibri 10 bold",
    #                  text="P.S, the change background setting doesnt work with the main menu :)")
    # img = PhotoImage(master=new, file="rsz_twitter-xxl.png")

    # image1 = canvas.create_image(10, 10, image=img)
    # image2 = canvas.create_image(randint(100, 350), randint(100, 350), image=img)
    # image3 = canvas.create_image(randint(100, 350), randint(100, 350), image=img)
    # image4 = canvas.create_image(randint(100, 350), randint(100, 350), image=img)

    # def motion_tweet():
    # global color1, color2, color3
    # x1speed = randint(-10, 10)
    # x2speed = randint(-10, 10)
    # x3speed = randint(-10, 10)
    # x4speed = randint(-10, 10)
    # y1speed = randint(-10, 10)
    # y2speed = randint(-10, 10)
    # y3speed = randint(-10, 10)
    # y4speed = randint(-10, 10)

    # print(coordinates1,coordinates2,coordinates3,coordinates4)
    # error_count1 = 0
    # error_count2 = 0
    # while running:
    # try:
    # coordinates1 = canvas.coords(image1)
    # coordinates2 = canvas.coords(image2)
    # coordinates3 = canvas.coords(image3)
    # coordinates4 = canvas.coords(image4)
    # except Exception as e:
    # error_count1 += 1
    # if error_count1 <= 1:

    # print("Error detected as {}\n\n True error: Window ended".format(e))
    # else:
    # pass
    # try:

    # if coordinates1[0] >= 400:
    #    x1speed = randint(-10, -1)

    # elif coordinates1[0] <= 0:
    #   x1speed = randint(1, 10)

    # elif coordinates1[1] >= 400:
    #   y1speed = randint(-10, -1)

    # elif coordinates1[1] <= 0:
    #  y1speed = randint(1, 10)

    # if coordinates2[0] >= 400:
    #   x2speed = randint(-10, -1)

    # elif coordinates2[0] <= 0:
    #   x2speed = randint(1, 10)

    # elif coordinates2[1] >= 400:
    #   y2speed = randint(-10, -1)

    # elif coordinates2[1] <= 0:
    #   y2speed = randint(1, 10)

    # if coordinates3[0] >= 400:
    #   x3speed = randint(-10, -1)

    # elif coordinates3[0] <= 0:
    #   x3speed = randint(1, 10)

    # elif coordinates3[1] >= 400:
    #   y3speed = randint(-10, -1)

    # elif coordinates3[1] <= 0:
    #   y3speed = randint(1, 10)

    # if coordinates4[0] >= 400:
    #   x4speed = randint(-10, -1)

    # elif coordinates4[0] <= 0:
    #   x4speed = randint(1, 10)

    # elif coordinates4[1] >= 400:
    #   y4speed = randint(-10, -1)

    # elif coordinates4[1] <= 0:
    #   y4speed = randint(1, 10)

    # canvas.move(image1, x1speed, y1speed)
    # canvas.move(image2, x2speed, y2speed)
    # canvas.move(image3, x3speed, y3speed)
    # canvas.move(image4, x4speed, y4speed)

    # time.sleep(0.01)

    # This code was going to be used for making the main menu colour change nicely in a RGB like fashion. However, the math.sin function doesn't seem to like me.
    # col1 = map(math.sin(color1), -1,1, 0, 255)
    # col2 = map(math.sin(color2), -1, 1, 0, 255)
    # col3 = map(math.sin(color3), -1, 1, 0, 255)

    # color1 += 0.05
    # color2 += 0.03
    # color3 += 0.1
    # To see sin and map being used to create a rainbow effect, click here --> https://editor.p5js.org/142359/sketches/jc_v3Xvy
    # print(color1,color2,color3)

    # except Exception as e:
    # error_count2 += 1
    # if error_count2 <= 1:
    #   print("Real cause for error, abrupt thread end. Program return error {}".format(e))
    # else:
    #  pass

    # threading.Thread(target=motion_tweet).start()

    new.mainloop()


def Hangman_start(self):
    global lives
    lives = 10 #This is the lives of the player
    new = Window(data="Hang_Man", geom="300x400+500+500",title="Hangman")
    word_for_game = []  #The word for the actual hangman game will be stored in here

    objects.append(new)


    def grab_data():

        data = [] # array that holds all twitter text

        def word_process():
            global nested_load
            # print(data[0])
            #checker = False

            text_data_structure = ["Q", "W", "E", "R", "T", "Y", "U",
                                   "I", "O",
                                   "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z", "X", "C", "V", "B", "N", "M", "q",
                                   "w", "e", "r",                                                                               #All the allowed characters
                                   "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x",
                                   "c", "v", "b",
                                   "n", "m"]
            global x

            try:
                x = random.choice(data)     #Get text from X, this is from the data array which is appended by the loop at the bottom of this function
            except Exception as e:
                tkinter.messagebox.showwarning("ERROR", "The twitter api returned no tweet!\nGoing back to start")
                self.destroy()
                Hangman_start(self)

            x = x.split(' ')        #Split that text into its individual words. These words are seperated by the space
            print(x)
            x.pop()
            for words in x:  #For the words that exist in x
                new_word = list(words) #create new array that holds the words
                for letters in words: #For the letters in these words
                    if letters not in text_data_structure or letters in special_checker: #if the letters are not valid or if they are in the special characters array, dont allow it
                        print("Letter not found {}".format(letters))
                        try:
                            del x[x.index(words)]
                        except Exception as e:
                            print(e)
                    else:
                        pass
            print("NEW ARRAY {}".format(x))
            word_for_game.append(x[randint(0, len(x)) - 1]) #Grab a random word from that array to make the hangman word
            for length in range(len(word_for_game)):        #for all the words in the words_for_game variable,lower their characters
                word_for_game[length].lower()
            print(word_for_game)


        listener = StdListener(time_amount.get()) #Get the int from the scroller, this is the time passed into the constructor

        stream = StdStream(listener)    #Use listener in the stream

        stream.start(tweet_finder.get())    #start the stream with the word entered by the user

        for key in stream_data.keys():
            if key == "text":                   #For all the keys in the dict of stream_data, only grab the text fields
                data.append(stream_data[key])
            else:
                print("No text found")
        # print(data)


        try:
            loading.destroy()
            progressbar.destroy()
            word_process()          #Try all these things, they are probably going to cause errors some where, so catch them
            grabber_thread._stop()
        except Exception as e:
            print(e)

    def loading_method():
        global loading, progressbar,nested_load

        grab_button.destroy()
        disclaimer.destroy()            #Destroy the things from the hangman menu

        progressbar = Progressbar(new, orient=HORIZONTAL, length=100, mode="determinate")
        progressbar.pack()
        progressbar.place(relx=0.328, rely=0.55)
        nested_load = threading.Thread(target=load).start()
        loading = Label(new, width=10, text="Loading...\n\n Please wait", fg="#FFFFFF", bg="#000000")           #Make a loading bar like from the splash screen
        loading.pack()
        loading.place(relx=0.38, rely=0.35)
        try:
            loading_thread._stop()
        except Exception as e:
            print(e)
    def grab_data_thread():
        global player_array, grabber_thread, loading_thread, hangman_canvas, number1_int, number2_int, num1
        player_array = []       #This is the array that will store all the correct letters from the player
        special = list(tweet_finder.get())      #This is the players input from the game screen
        start = False


        hangman_canvas = Canvas(master=new,width=200,height=200,bg="black",highlightthickness=0)
        hangman_canvas.pack()
        hangman_canvas.place(relx=0.45,rely=0.35)                                                   #This is the canvas that holds the hangman

        # L = Left | T = Top | R = Right | D = Down

                                        #L #T #R  #D
        hangman_canvas.create_rectangle(80,70,140,10,fill="red") #HEAD
        hangman_canvas.create_rectangle(100, 70, 120, 120, fill="white") #BODY
        hangman_canvas.create_rectangle(70,80, 150, 90, fill="white") #ARMS
        hangman_canvas.create_rectangle(70,110, 150, 120, fill="white") #LEGS

        number1_int = StringVar(master=new)
        number1_int.set(0)
                                                                    #These are string variables for the numbers that are going to be used for the label at the bottom of the screen for the hangman game screen.
        number2_int = StringVar(master=new)
        number2_int.set(0)

        number1 = Label(new, textvariable= number1_int, bg="black",fg="white")
        number1.pack()

        number2 = Label(new, textvariable= number2_int, bg="black",fg="white")
        number2.pack()

        number1.place(relx=0.25,rely=0.8)
        number2.place(relx=0.68,rely=0.8)


        num1 = 0        #This number is set to change for each correct guess by the player so it is initialised here so it can appear on the game menu and not when the player clicks the button to input their letter


        correct = Label(new, text=" letters correct out of ", bg="black",fg="white")
        correct.pack()
        correct.place(relx=0.3,rely=0.8)


        print(special)
        if len(tweet_finder.get()) < 1:                                 #This checks if the player hasnt inputted anything
            tkinter.messagebox.showwarning(master=new, title="ERROR",
                                           message="No keyword was entered!\nPlease enter a keyword.")

        elif len(tweet_finder.get()) >= 1:              #This checks if the player inputs anything in the entry box
            for i in range(len(special)):               #For the length of the word
                if special[i] in special_checker or " " in special :        #If the word has letters that arent valid an error is returned to the player
                    tkinter.messagebox.showwarning(master=new, title="ERROR",
                                                   message="An invalid character(s) was inputted\nPlease input a valid character(s)\n\nText given: {}".format(
                                                       tweet_finder.get()))
                    tweet_finder.delete(0, END) #The entry box is cleared
                    start = False #And the game isnt started
                    break
                else:
                    start = True    #Else the game is started
            if start:
                grabber_thread = threading.Thread(target=grab_data).start()         #If the game is started, run these threads
                loading_thread = threading.Thread(target=loading_method).start()                            #These threads grab the data from twitter and run the loading bar
            else:
                pass

    def hangman():      #This function is what checks the players input at the game screen
        global end_word, counter, player_array, lives, special, player_guess, num1, number1, number2



        colours = ["#0300A7","#221EFF","#4845FE","#6765FD","#A4A3FC","#FFFFFF","#FD8D8D","#FF6363","#FF3535","#FF0000"]         #These are all colours for the hangmans head, right is most red, left is most blue.

        colour = colours[lives-1]       #The colour variable is for the head of the hangman, the colour is always the lives amount - 1 so we dont go out of the index range of the array

        if lives <= 1:  #This checks if the player is out of lives or not
            c = Canvas(new, width=1000, height=1000, bg="black", highlightthickness=0)
            c.pack()
            hangman_canvas.destroy()
            title.destroy()
            player_input.destroy()
            player_entry.destroy()

            lose = Label(new, text="YOU\nLOSE!!!", font=("Courier", 44), width=20, fg="white", bg="black")
            lose.pack()
            lose.place(relx=-0.6,rely=0.2)

            info = Label(new, text="Please use the menu strip to\nnavigate the software.", font=("Courier", int(44/4)), width=30, fg="white", bg="black")
            info.pack()
            info.place(relx=0.055, rely=0.7)
        else:
            pass

        try:
            end_word = list(word_for_game[0])  #The end word variable contains the word that the player has to guess. This is split up into its letters
            for i in range(len(end_word)):
                end_word[i] = end_word[i].lower() #Iterate through all the letters in this word and lower them all
            if counter >= 1:
                pass
            else:
                player_array = [''] * len(end_word) # The player array has blank strings, the amount of these is the amount of letters of the word that the player has to guess. This is so the words can match up

                print("Player array length = {}".format(len(player_array)))
                print("End word array length = {}".format(len(end_word)))
        except Exception as e:
            tkinter.messagebox.showwarning(master=new, title="ERROR", message="Program return Error {}".format(e))

        number2_int.set(len(end_word))  #Set the variable that determines the length of the word to the player to the actual length of the word
        counter += 1

        print("Player has to guess {}".format(word_for_game))

        try:
            player_guess = player_entry.get()
            player_guess = player_guess.lower() # Im not sure if player_guess = player_entry.get().lower() works, so i have used this method instead
            special = list(player_guess)
        except Exception as e:
            print(e)

        try:
            if len(player_entry.get()) < 1:     #If the player doesnt input anything, show an error
                tkinter.messagebox.showwarning(master=new, title="ERROR",
                                               message="No keyword was entered!\nPlease enter a keyword.")

            elif len(player_entry.get()) == 1:          #If the players input is equal to 1 do the following:
                for i in range(len(special)):           #For the loop at the length of the length of the users input
                    if special[i] in special_checker:      #If the users input is in the special characters
                        tkinter.messagebox.showwarning(master=new, title="ERROR",           #return error to player
                                                       message="An invalid character(s) was inputted\nPlease input a valid character(s)\n\nText given: {}".format(
                                                           player_entry.get()))
                        player_entry.delete(0, END) #Clear entry box


                    else:
                        loop_checker = True #Loop checker is true
                        for i in range(len(end_word)):      #For the length of the word that the player has to guess
                            if player_guess == end_word[i]: #If the players letter is in the end word at the same indes
                                if player_guess in player_array: #Check if it has already been guessed

                                    print("Letter already guessed")
                                    break

                                else:

                                    # Have player guess be same location as word to guess array location
                                    try:
                                        for j in range(len(end_word)):#For the length of the end word
                                            if player_guess == end_word[j]:     #If the player guess is at the index of the end word of the loop
                                                player_array[j] = player_guess #that same index for the player array is the same letter
                                                print(player_array)
                                                num1 += 1 #Increment the number that says how many letters you have corredt
                                                number1_int.set(num1) #set that number

                                    except:
                                        try:
                                            player_array[0] = player_guess
                                        except Exception as e:
                                            print("FINAL ERROR")

                            else:

                                print("Word to guess {}".format(end_word))
                                if loop_checker:
                                    lives -= 1 #if the guess isnt in the end word, remove a life
                                    loop_checker = False #Ths variable is to stop multiple lives being taken off for one guess. This would happen due to the loops being used for checking.
                                    print("Lives = {}".format(lives))

                                #print("Player array = ", player_array)




            elif len(player_entry.get()) >= 2: #If the players guess is 2 or more characters
                tkinter.messagebox.showwarning(master=new, title="ERROR",           #Return this error to the player
                                               message="Only 1 letter per guess is allowed 😭")
                player_entry.delete(0, END)

        except Exception as e:
            print(e)

        if player_array == end_word: #If the player array and the end word array are equal
            hangman_canvas.destroy()
            title.destroy()                 #Remove the objects <---
            player_input.destroy()
            player_entry.destroy()

            c = Canvas(new, width=1000,height=1000, bg="black", highlightthickness=0)
            c.pack()

            win = Label(new, text="YOU\nWIN!!!", font=("Courier", 44), width=20, fg="white", bg="black")
            win.pack()
            win.place(relx=-0.6,rely=0.2)#Show that a win has occurred

            info = Label(new, text="Please use the menu strip to\nnavigate the software.", font=("Courier", int(44/4)), width=30, fg="white", bg="black")
            info.pack()
            info.place(relx=0.055, rely=0.7)




            print("WIN")

        try:
            hangman_canvas.create_rectangle(80,70,140,10,fill=colour) #HEAD
        except Exception as e:
            print(e)
    def load():
        global data_thread, load_thread, loader, player_entry, player_input
        determined_time = 0 # This is a variable that was going to be used for something but was scrapped later on

        if time_amount.get() <= 5:
            determined_time = 0.25

        elif time_amount.get() >= 10 | time_amount.get() <= 14:
            determined_time = 1
        elif time_amount.get() >= 15 & time_amount.get() < 20:
            determined_time = 5
        else:
            determined_time = (25 / 4) + 2

        time_amount.destroy()
        tweet_finder.destroy()
        time_amount_detail.destroy()
        try:
            progressbar['value'] = 25
            time.sleep(determined_time)
            new.update_idletasks()
            progressbar['value'] = 50
            time.sleep(determined_time)
            new.update_idletasks()
            progressbar['value'] = 75       #This code is what makes the loading bar happen when the player enters their word for the start of the hangman game
            time.sleep(determined_time)
            new.update_idletasks()
            progressbar['value'] = 100
            new.geometry("320x320")
            title.place(relx=0.2, rely=0.0)

            player_entry = Entry(new, width=10)
            player_entry.pack()

            player_input = Button(new, command=hangman, text="Input Letter")
            player_input.pack()

            player_entry.place(relx=0.2, rely=0.45)
            player_input.place(relx=0.19, rely=0.6)


            data_thread._stop()
            load_thread._stop()
            loader._stop()          #Stop the threads


        except Exception as e:
            print(
                "True error: Progess bar deleted before progress process finished\n\n Program return error: {}".format(
                    e))

    try:
        nested_load._stop() #Stop the thread
    except Exception as e:
        print(e)

    title = Label(new, width=10, height=2, text="Hangman", bg="#000000", fg="#FFFFFF", font="Times 25 bold")
    title.pack()
    title.place(relx=0.15, rely=-0.0)

    disclaimer = Label(new,
                       text="It is advised to go for a shorter time\n\nThe real time can vary depending on the twitter API, \na shorter time can provide good results but\na longer time may return more accurate readings",
                       width=40, fg="white", bg="black")
    disclaimer.pack()
    disclaimer.place(relx=0.005, rely=0.65)

    time_amount_detail = Label(new, width=15, height=2, text="Time to process:", bg="#000000", fg="#FFFFFF")
    time_amount_detail.pack()
    time_amount_detail.place(relx=0.6, rely=0.2)

    time_amount = Scale(new, from_=1, to=25, bg="black", fg="white")
    time_amount.pack()                                                                                              #All this code is for the things that the player sees on the hangman menu
    time_amount.place(relx=0.7, rely=0.3)

    tweet_finder = Entry(new, width=10)
    tweet_finder.pack()
    grab_button = Button(new, width=13, text="Enter search term", command=grab_data_thread)
    grab_button.pack()

    tweet_finder.place(relx=0.19, rely=0.35)
    grab_button.place(relx=0.1312, rely=0.45)

    self.destroy()
    debug_objects()
    new.mainloop()


def Tweet_Search_Start(self):
    new = Window(data="Tweet_Search", geom="435x450+500+200",title="Tweet searcher")
    objects.append(new)
    try:
        self.destroy()
    except Exception as e:
        print(e)
    User_input = Entry(new, width=10)           #This is the entry box that holds the users input for the search term that is used later in grab data function
    User_input.pack()

    #RADIO BUTTON INTS, these are to track the current state of choice for the user on the data they want to grab from the twitter API
    Info_RB_INT = IntVar(master=new)
    Info_RB_INT.set(1)

    Person_info_INT = IntVar(master=new)
    Person_info_INT.set(1)

    Tweet_Data_INT = IntVar(master=new)
    Tweet_Data_INT.set(1)

    title = Label(new, width=30,text="Tweet searcher", font=("Times new roman",30), bg="black",fg="white")
    title.pack()
    title.place(relx=-0.25,rely=0.005)

    def Grab_data(info_data = 1 , tweet_check= 1, twitter_person=1, debug = False):         #The parameters here are important, the ones that are == 1 are that by default because this is their off state. Those variables are connected to radio buttons
        global location                                                                     #The integers of these radio buttons determine the data that comes through and gets written to a file
        inp = User_input.get()          #When the user clicks the button, this variable will be made, this gets the data from the entry box




        if inp == "":
            tkinter.messagebox.showwarning(master=new,title= "ERROR", message="Information is needed in the entry field to continue")           #This checks if the input by the user has no data in it
            User_input.delete(END,0)

        else:
            listener = StdListener(1) #This is the tweet listener with the overridden time of 1 second
            strings = []    #This array holds the data that has already come through twitter and has gone through the filtering process
            tweets = []     #This array holds the data that comes from twitter
            end_string = "" #This is what will be written to the file. Every strings item is added onto this which gives us the text for the file
            stream = StdStream(listener)#This is the stream object
            stream.start(keys=inp) #The search term keys are based on the user input (inp variable)

            if debug:
                print(json.dumps(stream_data, indent=4, sort_keys=True))    #This is for debugging, it lets me see all the data that comes through the stream

            else:
                tweets.append(stream_data)      #Append what is caught by the stream object into the tweets array

                info_data = Info_RB_INT.get()
                tweet_check = Tweet_Data_INT.get()                  #Get the radio buttons INTs
                twitter_person = Person_info_INT.get()
                print(f"Info data: {info_data}")

                                                                                                #THE FOLLOWING CODE IS ALL THE FILTERING DATA. Tweets[0] is there because a thread messes with the data so I am just relying on the first tweet caught rather than the first tweet being an mash up of multiple tweets
                try:
                    if info_data == 2:


                        print(tweets[0])
                        if tweets[0]['user']['location'] == None:
                                location = "The user has their location set to private. Sorry \n"
                                print(tweets[0])
                        else:
                                location = f"The users location is {tweets[0]['user']['location']}"

                        info_str = "                                        The following data is more technical information about the tweet\n\n" \
                                           f"This tweet was created at: {tweets[0]['created_at']}\n\n" \
                                           f" This user's twitter ID is: {tweets[0]['id']}\n\n" \
                                           f" The source of the tweet is: {tweets[0]['source']}. It is very possible that the link work on non mobile devices\n\n" \
                                           f" The user's location {location}\n\n"\

                        strings.append(info_str)

                    if tweet_check == 2:

                        link_true = f"Attached link: {tweets[0]['user']['url']}\n\n"
                        link_false = "The tweet has no attached link :(\n\n"
                        tweet_str =  "                                      The following data is for the tweet\n\n"\
                                f"The tweet says: {tweets[0]['text']}\n\n" \
                                f"{link_true if tweets[0]['user']['url'] != None else link_false  }\n\n"\
                                f"This tweet has {tweets[0]['quote_count']} qoutes\n\n" \
                                f"This tweet has {tweets[0]['reply_count']} replies\n\n" \
                                f"This tweet has {tweets[0]['favorite_count']} likes\n\n" \
                                f"This tweet has {tweets[0]['retweet_count']} retweets \n\n" \
                                f"The people that have been mentioned are: {json.dumps(tweets[0]['entities']['user_mentions'],indent=4,sort_keys=True)}" if len(tweets[0]['entities']['user_mentions']) >=1 else "Nobody was mentioned in this tweet\n\n"\
                                f"The links included in this tweet are : {tweets[0]['entities']['urls']}\n\n" if len (tweets[0]['entities']['urls']) >=1 else "No links were found in this tweet\n\n"

                        strings.append(tweet_str)

                    if twitter_person == 2:
                        if tweets[0]['user']['verified']:
                            verified = f"{tweets[0]['user']['name']} is verified!"
                        else:
                            verified = f"{tweets[0]['user']['name']} is not verified!"

                        p_bg =tweets[0]['user']['profile_background_image_url'] if tweets[0]['user']['profile_background_image_url'] != '' else "No background image was found for this profile"

                        default = "This is a default profile " if tweets[0]['user']['default_profile'] == False else "This profile is not a default profile" + "This user has a default profile picture" if tweets[0]['user']['default_profile_image'] else f"The users profile picture can be found here >>>   {tweets[0]['user']['profile_image_url']}   <<<\n\n"

                        person_str = "                                      The following data is about the user\n\n" \
                                f"The person who tweeted is: {tweets[0]['user']['name']}\n\n"\
                                f"Their screen name is {tweets[0]['user']['screen_name']}\n\n"\
                                f"{verified}\n\n"\
                                f"{tweets[0]['user']['name']}'s follow count is: {tweets[0]['user']['followers_count']}\n\n"\
                                f"{tweets[0]['user']['name']}'s is following {tweets[0]['user']['friends_count']} people\n\n"\
                                f"{tweets[0]['user']['name']} has liked {tweets[0]['user']['favourites_count']} tweets\n\n"\
                                f"{tweets[0]['user']['name']} has posted {tweets[0]['user']['statuses_count']} tweets\n\n"\
                                f"The users profile picture can be found here  >>>   {tweets[0]['user']['profile_image_url']}   <<<\n\n"\
                                f"{p_bg}\n\n"\
                                f"{default}\n\n"\
                                f"{tweets[0]['user']['name']} joined twitter at: {tweets[0]['user']['created_at']}"

                        strings.append(person_str)






                    for i in range(len(strings)):           #For all the items in the strings array
                        if i <= 0:                      #If theres only one string no new line is needed
                            end_string += strings[i]
                        else:
                            end_string += strings[i] if type(strings[i]) == str else str(strings[i]) + "\n"         #else add it on

                    print(end_string)
                    with open("External/Twitter_data.txt", "w", encoding="utf-8") as f:     #The encoding is set to utf-8 to avoid character encoding errors
                        f.write(end_string)

                except Exception as e:
                    print(f"An error occurred while processing the twitter data :( \n\n\nERROR AT:{e}\n\n LINE OF ERROR {sys.exc_info()[-1].tb_lineno}")        #This error exception catches the error and the line it is at, it allows for easier debugging
    #RADIO_SELECTION

    Tweet_sive = Button(new, width=10, command=Grab_data,text="Write to file")
    Tweet_sive.pack()

    Info_RB1 = Radiobutton(new, text= "Include info",width = 20,variable=Info_RB_INT, bg="#BD0000",fg="white",value=2,activebackground="#C04E4E",selectcolor="#000000")
    Info_RB1.pack()
    Info_RB2 = Radiobutton(new, text= "Dont include info",width = 20,variable=Info_RB_INT, value=1, bg="#BD0000",fg="white",activebackground="#C04E4E",selectcolor="#000000")
    Info_RB2.pack()
                                                                                                                                                                                                    #Radio buttons
    TweetData_RB1 = Radiobutton(new, text= "Include tweet & data",width = 20,variable=Tweet_Data_INT, bg="#BD0000",fg="white",value=2,activebackground="#C04E4E",selectcolor="#000000")
    TweetData_RB1.pack()
    TweetData_RB2 = Radiobutton(new, text= "Dont include tweet & data",width = 20,variable=Tweet_Data_INT, value=1, bg="#BD0000",fg="white",activebackground="#C04E4E",selectcolor="#000000")
    TweetData_RB2.pack()

    PersonInfo_RB1 = Radiobutton(new, text= "Include perosnal data",width = 20,variable=Person_info_INT, bg="#BD0000",fg="white",value=2,activebackground="#C04E4E",selectcolor="#000000")
    PersonInfo_RB1.pack()
    PersonInfo_RB2 = Radiobutton(new, text= "Dont include personal data",width = 20,variable=Person_info_INT, value=1, bg="#BD0000",fg="white",activebackground="#C04E4E",selectcolor="#000000")
    PersonInfo_RB2.pack()

    l_side_x = 0.075
    r_side_x = 0.54
                            #These are the axis's for the radio buttons, it allows for easy management of the spacing of the radio buttons
    set_1_y = 0.25
    set_2_y = 0.35
    set_3_y = 0.45

    info_label = Label(new, text="Enter your twitter search term!",width=25,font=("Times new roman",15),fg="white",bg="black")
    info_label.pack()
    info_label.place(relx=0.2,rely=0.6)


    Info_RB1.place(relx=l_side_x, rely=set_1_y)
    Info_RB2.place(relx=r_side_x,rely=set_1_y)

    TweetData_RB1.place(relx=l_side_x, rely=set_2_y)
    TweetData_RB2.place(relx=r_side_x,rely=set_2_y)
    TweetData_RB2.place(relx=r_side_x,rely=set_2_y)

    PersonInfo_RB1.place(relx=l_side_x, rely=set_3_y)
    PersonInfo_RB2.place(relx=r_side_x,rely=set_3_y)

    Tweet_sive.place(relx=0.54,rely=0.75)
    User_input.place(relx=0.315, rely=0.76)


    #x = Button(new, width=10, command= lambda:print(Info_RB_INT.get()))
    #x.pack()
    debug_objects()
    new.mainloop()


def debug_objects():
    print(objects)          #This prints all the objects in the program at any given time
