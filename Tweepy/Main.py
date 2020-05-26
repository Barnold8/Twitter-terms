import Classes # This imports the file that holds all the class data and logic



if __name__ == "__main__":      #If this is the main file, run the code below

    #test = ["Python","C++"]

    f = Classes.Window_Handler("Splash_screen","250x250+500+200","Splash",False) # create the window handler object, the parameters in order go, title, geometry, data, and if it as a menu strip or not
    f.mainloop()    #keeps the window loop going


