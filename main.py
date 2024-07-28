import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import PIL
import PIL.Image
import os
from dotenv import load_dotenv
import google.generativeai as genai

#Here we creating the main window.
class MainWindow(tk.Tk):
    def __init__(self, title, size1, size2):
        super().__init__()
        self.title(title)
        self.geometry(f"{size1[0]}x{size1[1]}")
        self.minsize(size2[0], size2[1])
        self.Xmathematics = Xmathematics(self, "Open file for Xmathematics", "Show solution of Xmathematics")
        self.Users = Users(self, "Open file for player1", "Open file for player2")
        self.icon = tk.PhotoImage(file = "Pei.png")
        self.iconphoto(True, self.icon)
        self.mainloop()

#Here we creating the error windo in case an image was not choosed.
class CheckBox(tk.Tk):
    def __init__(self, title, size1, size2):
        super().__init__()
        self.title(title)
        self.geometry(f"{size1[0]}x{size1[1]}")
        self.minsize(size2[0], size2[1])
        label = tk.Label(self, text = "You didnt choose a file!")
        label.pack()
        self.icon = tk.PhotoImage(file = "Pei.png")
        self.iconphoto(True, self.icon)
        self.mainloop()

#Here we creating the "Xmathematics" that show the user what is the correct and efficent way to solve a problem.
class Xmathematics(ttk.Frame):
    def __init__(self, parent, Xmathematics_button_open, Xmathematics_button_solve):
        super().__init__(parent)

        self.Xmathematics_show_image = None

        Xmathematics_button_open = ttk.Button(self, text = Xmathematics_button_open, command = self.open_Xmathemtics)
        Xmathematics_button_open.pack(fill = "both")
        Xmathematics_button_solve = ttk.Button(self, text = Xmathematics_button_solve, command = self.solve_the_problem)
        Xmathematics_button_solve.pack(fill = "both")
        self.place(relx = 0, rely = 0, relwidth = 0.3, relheight = 1)

    #This function opens the file for Xmathematics.
    def open_Xmathemtics(self):
        global img
        global filename
        filetype = [("jpg files", "*.jpg")]
        filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = filetype)
        img = Image.open(filename)
        img = img.resize((300,300))
        img = ImageTk.PhotoImage(img)
        Xmathemtics_show_image = ttk.Label(self, image = img)
        Xmathemtics_show_image.pack()
        self.Xmathematics_show_image = img

    #This function is solving the math problem by Xmathematics.
    def solve_the_problem(self):
        global img
        global filename
        if (self.Xmathematics_show_image is not None):
            load_dotenv()
            img = PIL.Image.open(filename)
            genai.configure(api_key=os.getenv("gemini_api_key"))
            generation_config = {
                "temperature": 0,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
            model = genai.GenerativeModel(model_name = "gemini-1.5-pro", generation_config = generation_config)
            prompt = "Find the problem in the image and solve correctely and efficiently. Please write an explantion for every stage."
            response = model.generate_content([prompt, img])
            XmathematicsAssessment = tk.Tk()
            XmathematicsAssessment.title("Xmathematics")
            output = tk.Text(XmathematicsAssessment)
            output.pack(expand = True, fill = "both")
            output.insert("1.0", response.text)
            self.mainloop()
        else:
            CheckBox("Error", (200,100), (200,100))

#This class opens and evaluates the solutions for user1 and for user2.
class Users(ttk.Frame):
    def __init__(self, parent, button_text_user1, button_text_user2):
        super().__init__(parent)

        self.User1_Show_Image = None
        self.User2_Show_Image = None

        open_file = ttk.Button(self, text = button_text_user1, command = self.Open_User_1)
        open_file.pack(fill = "both")
        open_file = ttk.Button(self, text = button_text_user2, command = self.Open_User_2)
        open_file.pack(fill = "both")
        Assess_Answer = ttk.Button(self, text = "Which player has the correct answer?", command = self.Answer_Evaluation)
        Assess_Answer.pack(fill = "both")
        Assess_Solution = ttk.Button(self, text = "Which player has the correct solution?", command = self.Solution_Evaluation)
        Assess_Solution.pack(fill = "both")

        self.place(relx = 0.3, rely = 0, relwidth = 0.7, relheight = 1)
    
    def Open_User_1(self):
        global img1
        global filename1
        filetype = [("jpg files", "*.jpg")]
        filename1 = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = filetype)
        img1 = Image.open(filename1)
        img1 = img1.resize((300,300))
        img1 = ImageTk.PhotoImage(img1)
        User1_Solution = ttk.Label(self, text = "Player1 solution", font = ('Times New Roman', 15, 'bold'))
        User1_Solution.pack()
        User1_Show_Image = ttk.Label(self, image = img1)
        User1_Show_Image.pack()
        self.User1_Show_Image = img1

    def Open_User_2(self):
        global img2
        global filename2
        filetype = [("jpg files", "*.jpg")]
        filename2 = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = filetype)
        img2 = Image.open(filename2)
        img2 = img2.resize((300,300))
        img2 = ImageTk.PhotoImage(img2)
        User2_Solution = ttk.Label(self, text = "Player2 solution", font = ('Times New Roman', 15, 'bold'))
        User2_Solution.pack()
        User2_Show_Image = ttk.Label(self, image = img2)
        User2_Show_Image.pack()
        self.User2_Show_Image = img2
    
    def Answer_Evaluation(self):
        global img1
        global img2
        global filename1
        global filename2
        if((self.User1_Show_Image and self.User2_Show_Image) is not None):
            load_dotenv()
            img1 = PIL.Image.open(filename1)
            img2 = PIL.Image.open(filename2)
            genai.configure(api_key=os.getenv("gemini_api_key"))
            generation_config = {
                "temperature": 0,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
            model = genai.GenerativeModel(model_name = "gemini-1.5-pro", generation_config = generation_config)
            prompt = "Please check which player has the correct answer for the problem marked in rectangular. Answer by writing only the player."

            response = model.generate_content([prompt, img1, img2])
            XmathematicsAssessment = tk.Tk()
            XmathematicsAssessment.title("Xmathematics")
            output = tk.Text(XmathematicsAssessment)
            output.pack(expand = True, fill = "both")
            output.insert("1.0", response.text)
            self.mainloop()
        else:
            CheckBox("Error", (200,100), (200,100))

    def Solution_Evaluation(self):
        global img1
        global img2
        global filename1
        global filename2
        if((self.User1_Show_Image and self.User2_Show_Image) is not None):
            load_dotenv()
            img1 = PIL.Image.open(filename1)
            img2 = PIL.Image.open(filename2)
            genai.configure(api_key=os.getenv("gemini_api_key"))
            generation_config = {
                "temperature": 0,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
            model = genai.GenerativeModel(model_name = "gemini-1.5-pro", generation_config = generation_config)
            prompt = "Please check which player has the correct solution for the problem. Write down your explantion to each step for the correct solution. Do not write anything about the worng solution"

            response = model.generate_content([prompt, img1, img2])
            XmathematicsAssessment = tk.Tk()
            XmathematicsAssessment.title("Xmathematics")
            output = tk.Text(XmathematicsAssessment)
            output.pack(expand = True, fill = "both")
            output.insert("1.0", response.text)
            self.mainloop()
        else:
            CheckBox("Error", (200,100), (200,100))

#The main window.
MainWindow("Xmathematics", (1200,600), (1200,600))
