import os
from tkinter import Frame, Tk, Label, Button, Canvas, filedialog, StringVar, BOTH, TOP, W, E, N, S, NW
from PIL import Image, ImageTk
from search import perform_search


class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class ImageView:
    def __init__(self, parent):
        self.frame = parent

        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.canvas = Canvas(parent, bd=0, highlightthickness=0)
        # Set dummy image when the image view is loaded
        self.image = Image.new("RGB", (500, 500), "gray")
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW, tags="IMG")
        self.canvas.pack(side=TOP, fill=BOTH, expand=1)
        # Add listener that is called in case the window is resized
        parent.bind("<Configure>", self.resize)

    def resize(self, event):
        # Resize current image in the image canvas that it fits in the window and maintains its aspect ratio
        wpercent = (event.width / float(self.image.size[0]))
        hsize = int((float(self.image.size[1]) * float(wpercent)))
        size = (event.width, hsize)
        resized = self.image.resize(size, Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(resized)
        # Delete old image from the canvas
        self.canvas.delete("IMG")
        # And add the resized image to the canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW, tags="IMG")

    def show_image(self, image_id):
        # Construct image path
        directory = "PlantCLEF2016Test"
        image_name = ("%i.jpg" % image_id)
        image_path = os.path.join(directory, image_name)
        # Open selected image file
        self.image = Image.open(image_path)

        # Retrieve the current window size
        size = Size(self.frame.winfo_width(), self.frame.winfo_height())

        # Resize image
        self.resize(size)


class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")

        self.parent = parent

        # Create variable to track changes to the selected image id
        self.image_id = StringVar()
        self.image_view = None

        self.setup_ui()
        self.center_window()

    def center_window(self):
        w = 500
        h = 500

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry("%dx%d+%d+%d" % (w, h, x, y))

    def setup_ui(self):
        self.parent.title("Find similar pictures")
        self.pack(fill=BOTH, expand=1)

        label = Label(self, text="Select an image file to find its most similar image")
        label.pack()

        file_dialog_button = Button(self, text="Open Image file", command=self.on_open, pady=15)
        file_dialog_button.pack()

        self.image_view = ImageView(self)

        image_id_label = Label(self, textvariable=self.image_id, pady=15)
        image_id_label.pack()

    def on_open(self):
        options = {
            'defaultextension': '.jpg',
            'filetypes': [('jpeg files', '.jpg')],
            'initialdir': './PlantCLEF2016Test/'
        }

        filename = filedialog.askopenfilename(**options)

        if filename != "":
            image_id = perform_search(filename)

            self.image_id.set("Image ID: %s" % image_id)
            self.image_view.show_image(image_id)
        else:
            self.image_id.set("")


def main():
    root = Tk()
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
