from model import Predictor
from tkinter import *
from PIL import Image, ImageDraw


class Paint:
    DEFAULT_PEN_SIZE = 20
    DEFAULT_COLOR = 'white'

    model: Predictor

    def __init__(self):
        self.root = Tk()
        self.root.title("Prediction")
        self.root.geometry('600x600')
        self.root.resizable(width=False, height=False)

        self.model = Predictor('mnist_98.joblib')

        self.label = Label(text="", font=('Arial', 21))
        self.label.place(relx=0.5, rely=0.1, anchor='center')

        self.canvas = Canvas(self.root, bg='black', width=280, height=280)
        self.canvas.pack(expand=True)

        self.clear_button = Button(self.root, text='Clear field', command=self.clear_canvas)
        self.clear_button.pack(side=LEFT, padx=10, pady=10)

        self.guess_button = Button(self.root, text='Guess the number', command=self.guess_number)
        self.guess_button.pack(side=LEFT, padx=10, pady=10)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.DEFAULT_PEN_SIZE
        self.color = self.DEFAULT_COLOR


        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def paint(self, event):
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=self.line_width, fill=self.color,
                                    capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y


    def reset(self, event):
        self.old_x, self.old_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.label.config(text='')

    def guess_number(self):
        self.canvas.update()
        x = self.canvas.winfo_x()
        y = self.canvas.winfo_y()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()


        image = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(image)

        for item in self.canvas.find_all():
            coords = self.canvas.coords(item)
            if self.canvas.type(item) == "line":
                draw.line(coords, fill=self.color, width=self.line_width)

        image = image.resize((28, 28))

        self.label.config(text=self.model.guess_number_by_tree(image), font=('Arial', 21))


if __name__ == '__main__':
    Paint()
