# imports
import json
from customtkinter import *
import customtkinter as ctk
from PIL import Image

# initialize window
root = CTk()
root.geometry("1920x950")
root.title('GPA Calculator')
root.state('zoomed')
ctk.set_default_color_theme("dark-blue.json")

# add seperators
separator = ctk.CTkFrame(root, width=2)
separator.place(relx=0, rely=0.15, relwidth=1, relheight=0.005)
separator2 = ctk.CTkFrame(root, width=2)
separator2.place(relx= 0.5, rely = 0.15, relwidth=0.003, relheight=1)
separator3 = ctk.CTkFrame(root, width=2)
separator3.place(relx=0, rely=0.75, relwidth=0.5, relheight=0.005)
separator2 = ctk.CTkFrame(root, width=2)
separator2.place(relx= 0.25, rely = 0.75, relwidth=0.003, relheight=0.25)

# clear json file
with open('enteredInfo.json', 'w') as f:
        f.truncate(0)
        json.dump([], f)

# initialize entered information
classInfo = {"classType": "None", "grade": ""}
v = StringVar(root)

# called when a radiobutton is selected
def sel():
    # display selection to the user
    selection = "You selected " + str(v.get()) + "."
    selLabel.configure(text=selection, text_color = "Black")
    # update dictionary to contain class type
    if v.get() == "Non-rigor":
        classInfo["classType"] = "Non-rigor"
    elif v.get() == "AP":
        classInfo["classType"] = "AP"
    elif v.get() == "DE":
        classInfo["classType"] = "DE"
    else:
        classInfo["classType"] = "None"

# called when "Add a class" button is clicked
def addClass():
    # checks whether a valid grade has been entered
    classInfo["grade"] = gradeEntry.get()
    validGrades = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                  '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                  '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                  '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
                  '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
                  '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                  '60', '61', '62', '63', '64', '65', '66', '67', '68', '69',
                  '70', '71', '72', '73', '74', '75', '76', '77', '78', '79',
                  '80', '81', '82', '83', '84', '85', '86', '87', '88', '89',
                  '90', '91', '92', '93', '94', '95', '96', '97', '98', '99',
                  '100']
    
    # Validate class type
    if classInfo["classType"] == "None":
        selLabel.configure(text= "Please select a class type.", text_color = "Red")
        
    # Validate class grade
    elif classInfo['grade'] not in validGrades:
        gradeErrorLabel.configure(text= "Please enter a valid grade.")

    # if all info is entered correctly
    else:
        gradeErrorLabel.configure(text= "")
        # add new class info into file
        with open('enteredInfo.json', 'r') as f:
            currentClasses = json.load(f)
            currentClasses.append(classInfo)
        # update file
        with open('enteredInfo.json', 'w') as f:
            f.truncate(0)
            json.dump(currentClasses, f)

        # reset buttons/error labels
        nonrigorRB.deselect()
        apRB.deselect()
        deRB.deselect()
        gradeEntry.delete(0, len(gradeEntry.get()))
        selLabel.configure(text="")

        # read file with current classes
        with open('enteredInfo.json', 'r') as f:
            currentClasses = json.load(f)

        # displays entered classes to user
        currentClassesStr = []
        c = 1
        x = 0.1
        y = 0.045 * c
        second_column = False
        for i in currentClasses:
            # create label text in a string
            currentClassesStr.append("     " + i["classType"] + " class, " + i["grade"] + "%")
        
        for text in currentClassesStr:
            if c > 20:
                if second_column == False:
                    x = 0.6
                    c = c-20
                    y = y = 0.045 * c
                    second_column = True
                else:
                    with open('enteredInfo.json', 'w') as f:
                        currentClasses = json.load(f)
                    currentClasses.pop()
                    json.dump(currentClasses, f)
                    gradeErrorLabel.configure(text="Class limit reached.")
                    break
            else:
                y = 0.045 * c
            label = ctk.CTkLabel(master=classesFrame, text=text, font=("Gill Sans", 15), bg_color=("transparent"), anchor="w", text_color="Black")
            label.place(relx=x, rely=y)
            c += 1
            classesFrame.update()

        classInfo["classType"] = "None"
        update_GPA()

def update_GPA():
    uwGPA = 0
    wGPA = 0
    with open('enteredInfo.json', 'r') as f:
        currentClasses = json.load(f)
    for i in currentClasses:
        if int(i["grade"]) > 89:
            uwGPA += 4
            wGPA += 4
            if i["classType"] != "Non-rigor":
                wGPA += 1
        elif int(i["grade"]) > 79:
            uwGPA += 3
            wGPA += 3
            if i["classType"] != "Non-rigor":
                wGPA += 1
        elif int(i["grade"]) > 69:
            uwGPA += 2
            wGPA += 2
            if i["classType"] != "Non-rigor":
                wGPA += 1
        else:
            uwGPA += 0
            wGPA += 0
    if len(currentClasses) == 0:
        uwGPA = "N/A"
        wGPA = "N/A"
    else:
        uwGPA = round(uwGPA / len(currentClasses), 2)
        wGPA = round(wGPA / len(currentClasses), 2)
    uwgpaLabel.configure(text=uwGPA)
    wgpaLabel.configure(text=wGPA)

def helpButtonPressed():
    
    helpWindow = CTk()
    helpWindow.geometry("960x600")
    helpWindow.title("GPA Genie Help")

    ctk.CTkLabel(helpWindow, text="GPA Genie Help", font=("Gill Sans", 30), text_color="#4a64a1").pack(pady=20)
    ctk.CTkLabel(helpWindow, text="How to Use GPA Genie:", font=("Gill Sans", 20), text_color="#4a64a1").place(relx=0.1, rely=0.1)
    ctk.CTkLabel(helpWindow, text="  -  To add a class, fill out the information requested on the left side of the screen.", font=("Gill Sans", 15)).place(relx=0.05, rely=0.2)
    ctk.CTkLabel(helpWindow, text="  -  Select the class type using the corresponding button shown. Honors, advanced, accelerated, and on-level courses all count as non-rigor courses.", font=("Gill Sans", 15)).place(relx=0.05, rely=0.30)
    ctk.CTkLabel(helpWindow, text="  -  In the text box below that, enter the grade you earned for that class. The grade must be an integer (not a decimal) from 1-100. If you earned", font=("Gill Sans", 15)).place(relx=0.05, rely=0.4)
    ctk.CTkLabel(helpWindow, text="     more than a 100 in the class, enter 100.", font=("Gill Sans", 15)).place(relx=0.05, rely=0.45)
    ctk.CTkLabel(helpWindow, text="  -  Once you have selected a class type and a valid grade, click the 'Add a Class' button", font=("Gill Sans", 15)).place(relx=0.05, rely=0.55)
    ctk.CTkLabel(helpWindow, text="  -  Your entered class will now show up on the right side of the screen in the 'Entered Classes' section", font=("Gill Sans", 15)).place(relx=0.05, rely=0.65)
    ctk.CTkLabel(helpWindow, text="  -  Both the unweighted GPA and weighted GPA will now update based on your entered classes", font=("Gill Sans", 15)).place(relx=0.05, rely=0.75)
    ctk.CTkLabel(helpWindow, text="  -  You can continue to add classes until you reach the limit (40 classes)", font=("Gill Sans", 15)).place(relx=0.05, rely=0.85)

    helpWindow.mainloop()

ctk.CTkLabel(root,text="").pack()
ctk.CTkLabel(root, text="GPA Calculator", font=("Gill Sans", 30), text_color="#4a64a1").pack()
ctk.CTkLabel(root, text="Click the help button on the right for more details.", font=("Gill Sans", 15)).pack()
ctk.CTkLabel(root, text="Enter your classes below:", font=("Gill Sans", 30)).place(relx=0.14, rely=0.19)
ctk.CTkLabel(root, text="Choose the class rigor:", font=("Gill Sans", 15)).place(relx=0.195, rely=0.26)

help_image = ctk.CTkImage(light_image=Image.open("/Users/ryvaan/Ryvaan/Programming/Python/Programs/FBLA2024/2.png"),
                                  size=(40, 40))
logo_image = ctk.CTkImage(light_image=Image.open("/Users/ryvaan/Ryvaan/Programming/Python/Programs/FBLA2024/1.png"),
                                  size=(249, 108))
logo = ctk.CTkLabel(root, image=logo_image, text="")
logo.place(x = 5, relx = 0.0026, rely = 0.00463)

helpButton = ctk.CTkButton(master=root, image=help_image,text="", width=40, height=40, bg_color="#ebebeb", fg_color="#ebebeb", command=helpButtonPressed, hover_color="#ebebeb",)
helpButton.place(relx = 0.93, rely = 0.04)

nonrigorRB = ctk.CTkRadioButton(root, text="Non-rigor", variable=v, value="Non-rigor", command = sel, font=("Gill Sans", 15))
nonrigorRB.place(relx= 0.21, rely = 0.31)
apRB = ctk.CTkRadioButton(root, text="AP", variable=v, value="AP", command = sel, font=("Gill Sans", 15))
apRB.place(relx= 0.21, rely = 0.345)
deRB = ctk.CTkRadioButton(root, text="Dual Enrollment", variable=v, value="DE", command = sel, font=("Gill Sans", 15))
deRB.place(relx= 0.21, rely = 0.38)
selLabel = ctk.CTkLabel(root, text="", font=("Gill Sans", 15))
selLabel.place(relx = 0.25, rely = 0.46, anchor = CENTER)
ctk.CTkLabel(root, text="Enter Class Grade:", font=("Gill Sans", 15)).place(relx=0.205, rely = 0.51)
gradeEntry = ctk.CTkEntry(root, width=100, height=20, font=("Gill Sans", 15))
gradeEntry.place(relx= 0.214, rely = 0.56)
gradeErrorLabel = ctk.CTkLabel(root, text="", text_color="Red", font=("Gill Sans", 15))
gradeErrorLabel.place(relx = 0.195, rely = 0.6)
addClassButton = ctk.CTkButton(root, text="Add Class", command=addClass, font=("Gill Sans", 15))
addClassButton.place(relx=0.201, rely = 0.65)
ctk.CTkLabel(root, text="Entered Classes:", font=("Gill Sans", 30)).place(relx=0.68, rely=0.19)
classesFrame = ctk.CTkFrame(root, fg_color="transparent")
classesFrame.place(relx = 0.503, rely = 0.3, relwidth = 0.5, relheight = 0.7)
ctk.CTkLabel(root, text="Unweighted GPA:", font=("Gill Sans", 25)).place(relx = 0.06, rely = 0.78)
ctk.CTkLabel(root, text="Weighted GPA:", font=("Gill Sans", 25)).place(relx = 0.318, rely = 0.78)
uwgpaLabel = ctk.CTkLabel(root, text="N/A", font=("Gill Sans", 30), anchor=CENTER)
uwgpaLabel.place(relx = 0.11, rely = 0.85)
wgpaLabel = ctk.CTkLabel(root, text="N/A", font=("Gill Sans", 30), anchor=CENTER)
wgpaLabel.place(relx = 0.36, rely = 0.85)

classesFrame.mainloop()
root.mainloop()