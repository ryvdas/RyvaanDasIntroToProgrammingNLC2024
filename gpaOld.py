# imports
import json
from tkinter import *

# initialize window
root = Tk()
root.geometry("750x1000")
root.title('GPA Calculator')

# clear enteredInfo file from possible previous use
with open('enteredInfo.json', 'w') as info_file:
    info = []
    info_file.truncate()
    json.dump(info, info_file)

# store empty enteredInfo file in info variable
with open('enteredInfo.json', 'r') as info_file:
    info = json.load(info_file)

# run when add a class button is clicked
def enterClass():

    # initialize new entering window
    enterWindow = Tk()
    enterWindow.geometry("500x500")
    enterWindow.title('Add a class')

    # initialize currently entered class info
    classInfo = {"classType": "None", "grade": ""}
    Label(enterWindow, text="").pack()
    Label(enterWindow, text="Choose Class Type:").pack()

    def sel():
        selection = "You selected " + str(v.get()) + "."
        label.config(text=selection)
        if v.get() == "non-rigor":
            classInfo["classType"] = "non-rigor"
        elif v.get() == "AP":
            classInfo["classType"] = "AP"
        elif v.get() == "DE":
            classInfo["classType"] = "DE"
        else:
            classInfo["classType"] = "None"

    def is_valid_grade(s):
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
        
        if (len(s) >= 0) and (len(s) <= 3):
            if s in validGrades:
                return True
            else:
                return False
        else:
            return False
    
    def is_valid_class(s):
        if s == "None":
            return False
        else:
            return True
        
    def retrieve_grade():
        inputValue = gradeTextBox.get("1.0", "end-1c")
        validGrade = is_valid_grade(inputValue)
        validClass = is_valid_class(classInfo['classType'])
        if not validClass:
            errorLabel.config(text="Please choose a class type")
        elif not validGrade:
            errorLabel.config(text="Please an integer from 0 and 100 in the text box")
        else:
            errorLabel.config(text="")
            classInfo["grade"] = inputValue
            enterWindow.destroy()
            info.append(classInfo)
            with open("enteredInfo.json", 'w') as info_file:
                info_file.truncate()
                json.dump(info, info_file)
            enteredClassesStr = ""
            if len(info) > 0:
                for i in info:
                    enteredClassesStr = enteredClassesStr + "Class Type: " + i["classType"] + ', Grade: ' + i["grade"] + "\n"
    
            enteredClassesLabel.config(text=enteredClassesStr)

    v = StringVar(enterWindow)
    nonrigorRB = Radiobutton(enterWindow, text="Non-rigor", variable=v, value="non-rigor", command = sel).pack()
    apRB = Radiobutton(enterWindow, text="AP", variable=v, value="AP", command = sel).pack()
    deRB = Radiobutton(enterWindow, text="Dual Enrollment", variable=v, value="DE", command = sel).pack()

    label = Label(enterWindow)
    label.pack()

    Label(enterWindow, text="").pack()
    Label(enterWindow, text="What grade did you earn?").pack()
    gradeTextBox = Text(enterWindow, height=1, width = 3)
    gradeTextBox.pack()
    gradeButton = Button(enterWindow, text="Enter", command=retrieve_grade).pack()

    errorLabel = Label(enterWindow)
    errorLabel.pack()
    enterWindow.mainloop()

def calcGPA():
    with open('enteredInfo.json', 'r') as info_file:
        classes = json.load(info_file)
    if len(classes) == 0:
        mainErrorLabel.config(text="Please add a class")
    else:
        unGPAList = []
        for i in classes:
            currentClass = i
            enteredGrade = int(currentClass["grade"])
            if not (enteredGrade>=70): # 0-69
                classGPA = 0.0
            elif not (enteredGrade>=80): # 70-79
                classGPA = 2.0
            elif not (enteredGrade>=90): # 80-89
                classGPA = 3.0
            else: # 90-100
                classGPA = 4.0
            unGPAList.append(classGPA)
        unGPASum = 0
        for i in unGPAList:
            unGPASum += i
        unGPA = unGPASum/len(unGPAList)
        wGPAList = []
        for i in classes:
            currentClass = i
            if currentClass["classType"] == "non-rigor":
                bonus = 0.0
            else:
                bonus = 1.0
            enteredGrade = int(currentClass["grade"])
            if not (enteredGrade>=70): # 0-69
                classGPA = 0.0
            elif not (enteredGrade>=80): # 70-70
                classGPA = 2.0
            elif not (enteredGrade>=90): # 80-89
                classGPA = 3.0
            else: # 90-100
                classGPA = 4.0
            if classGPA >= 2.0:
                classGPA += bonus
            wGPAList.append(classGPA)
        wGPASum = 0
        for i in wGPAList:
            wGPASum += i
        wGPA = wGPASum/len(wGPAList)
        unGPALabel.config(text=str("Unweighted GPA: " + str(unGPA)))
        wGPALabel.config(text=str("Weighted GPA: " + str(wGPA)))

Label(root,text="").pack()
Label(root, text="Welcome to the GPA Calculator!").pack()
Label(root,text="").pack()
Label(root, text="Click the button below to add a class.").pack()
Label(root,text="").pack()
Button(root, text="Add a class", command = enterClass).pack()
Label(root,text="").pack()
Label(root,text="").pack()
Label(root,text="Entered Classes:").pack()
enteredClassesLabel = Label(root)
enteredClassesLabel.pack()

calculateButton = Button(root, text="Calculate", command=calcGPA).pack()
mainErrorLabel = Label(root,text="")
mainErrorLabel.pack()
unGPALabel = Label(root)
unGPALabel.pack()
unGPALabel.config(text="Unweighted GPA: NA")

wGPALabel = Label(root)
wGPALabel.pack()
wGPALabel.config(text="Weighted GPA: NA")

root.mainloop()