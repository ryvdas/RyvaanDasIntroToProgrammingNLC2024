from customtkinter import *
import customtkinter as ctk
from PIL import Image


root = CTk()
root.geometry("520x608")

ctk.set_default_color_theme("/Users/ryvaan/Ryvaan/Programming/Python/Programs/FBLA2024/theme.json")
my_image = ctk.CTkImage(light_image=Image.open("/Users/ryvaan/Ryvaan/Programming/Python/Programs/FBLA2024/GPAGuruLogo.png"),
                                  size=(100, 100))

image_label = ctk.CTkLabel(root, image=my_image, text="")  # display image with a CTkLabel
image_label.place(relx=0.1, rely=0.1)
#def sel():
#    print('ran')
#    print(entry.get())
#    print(dropdown.get())
#    length = len(entry.get())
#    entry.delete(0, length)
#
#    dropdown.set("Enter the class type")

#entry = ctk.CTkEntry(root)
#entry.place(relx=0.5, rely=0.5)
#enterButton = ctk.CTkButton(root, text="Enter", command=sel).place(relx=0.5, rely=0.7)

#dropdown = ctk.CTkOptionMenu(root, values=['a', 'b', 'c'])
#dropdown.place(relx=0.5, rely=0.6)
#dropdown.set("Enter the class type")

my_image = ctk.CTkImage(light_image=Image.open("/Users/ryvaan/Ryvaan/Programming/Python/Programs/FBLA2024/GPA_Genie_Assets/2.png"),
                                  size=(40, 40))
def createHelp():
    helpWindow = CTkToplevel(root)
    helpWindow.geometry("500x500")
    helpWindow.title('GPA Genie Help')

    ctk.CTkLabel(helpWindow, )
helpButton = ctk.CTkButton(master=root, image=my_image,text="", width=40, height=40, bg_color="#ebebeb", fg_color="#ebebeb", command=createHelp, hover_color="#ebebeb")
helpButton.place(relx=0.5, rely=0.8)

root.mainloop()