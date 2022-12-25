from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image, ImageOps
import numpy as np
from keras import utils as np_utils
from tkinter import filedialog as fd
import time
import os

model = load_model('MNIST_digits_CNN_model.h5')
def predict_digit(img):
    #resize image to 28×28 pixels
    img = img.resize((28,28))
    #convert rgb to grayscale
    img = img.convert('L')
    img = ImageOps.invert(img)
    img = np.array(img)
    #reshaping to support our model input and normalizing
    img = img.reshape(1,28,28,1)
    img = img/255.0
    #predicting the class
    res = model.predict([img])[0]
    return np.argmax(res), max(res)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0
        self.title("MNIST - CNN")
        self.resizable(width=False, height=False)
        # Creating elements
        self.canvas = tk.Canvas(self, width=500, height=500, bg = "white", cursor="man")
        self.label = tk.Label(self, text="En attente...", font=("Courier", 18))
        self.classify_btn = tk.Button(self, text = "Analyser", command = self.classify_handwriting)
        self.button_import = tk.Button(self, text = "Importer chiffre", command = self.open)  
        self.button_clear = tk.Button(self, text = "Supprimer", command = self.clear_all)
        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=1, column=0,pady=2, padx=2)
        self.button_import.grid(row=2, column=0, pady=5)
        self.classify_btn.grid(row=3, column=0, pady=5)
        self.button_clear.grid(row=4, column=0, pady=5)
        self.canvas.bind("<B1-Motion>", self.draw_lines)
 
        positionRight = int(self.winfo_screenwidth()/2 - 500/2)
        positionDown = int(self.winfo_screenheight()/2 - 680/2)
 
        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))

        self.attributes("-topmost", 1)

    def open(self):
        self.canvas.delete("all")
        self.label.configure(text="En attente...", fg="black")
        filename = fd.askopenfilename()
        img = Image.open(filename)
        digit, acc = predict_digit(img)
        self.label.configure(text='Import : '+str(digit)+' - '+ str(int(acc*100))+'% de précision', fg= "red")

    def clear_all(self):
        try:
            os.remove("file_name.ps")
            os.remove("number.png")
            self.label.configure(text="En attente...", fg="black")
            self.canvas.delete("all")
        except IOError:
            self.label.configure(text="En attente...", fg="black")
            self.canvas.delete("all")

    def classify_handwriting(self):
        self.canvas.postscript(file="file_name.ps", colormode='color')
        psimage = Image.open('file_name.ps')
        psimage.save('number.png')
        im = Image.open('number.png')
        digit, acc = predict_digit(im)
        self.label.configure(text= 'Draw : '+str(digit)+' - '+ str(int(acc*100))+'% de précision', fg= "blue")
    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=10
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')

app = App()
mainloop()


