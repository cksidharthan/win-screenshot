import tkinter as tk
import pyscreenshot as ImageGrab
from PIL import Image
import win32clipboard
from io import BytesIO
import defaults

x1, y1, x2, y2 = 0, 0, 0, 0

# Create Tkinter root
root = tk.Tk()
root.title("Screen Clipper")

# Canvas
canvas = tk.Canvas(root, width = 540, height = 250, bg="lightblue")
canvas.pack()

label = tk.Label(root, text = "Enter left, top, right, bottom values", bg="lightblue", font=('helvetica', 10))
canvas.create_window(130, 40, window=label)

label1 = tk.Label(root, text="", bg="lightblue", font=('helvetica', 10))
label2 = tk.Label(root, text="", bg="lightblue", font=('helvetica', 10))
label3 = tk.Label(root, text="", bg="lightblue", font=('helvetica', 10))

# Gets the default values from defaults.py
def get_default_values():
    x1 = str(defaults.default_x1).strip()
    x2 = str(defaults.default_x2).strip()
    y1 = str(defaults.default_y1).strip()
    y2 = str(defaults.default_y2).strip()
    return x1, x2, y1, y2

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def prepre_to_copy_clipboard():
    filepath = 'clip.png'
    image = Image.open(filepath)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)

def clip_screen(x1, x2, y1, y2):
    im = ImageGrab.grab(bbox=tuple(map(int, (x1, x2, y1, y2))))
    im.save('clip.png')
    # im.show()
    prepre_to_copy_clipboard()

# Get co ordinates from user
user_x1 = tk.Entry (root) 
canvas.create_window(130, 70, window=user_x1)
user_x2 = tk.Entry (root) 
canvas.create_window(130, 100, window=user_x2)
user_y1 = tk.Entry (root) 
canvas.create_window(130, 130, window=user_y1)
user_y2 = tk.Entry (root) 
canvas.create_window(130, 160, window=user_y2)

# To take clip based on user specified values
def user_clip():
    root.withdraw()
    x1 = user_x1.get().strip()
    x2 = user_x2.get().strip()
    y1 = user_y1.get().strip()
    y2 = user_y2.get().strip()
    try:
        label1.configure(text="Clipping ...")
        clip_screen(x1, x2, y1, y2)
        label1.configure(text='Image copied to clipboard')
    except Exception as e:
        print(e) 
        label1.configure(text='Error Occured. Check the co ordinates')
    root.deiconify()
    canvas.create_window(130, 240, window=label1)

# Clip with valules from defaults.py
def default_clip():
    root.withdraw()
    x1, x2, y1, y2 = get_default_values()
    try:
        label2.configure(text="Clipping ...")
        clip_screen(x1, x2, y1, y2)
        label2.configure(text='Image copied to clipboard')
    except Exception as e:
        print(e)
        label2.configure(text='Error Occured. Check the co ordinates')
    root.deiconify()
    canvas.create_window(390, 150, window=label2)

user_clip_button = tk.Button(text='Clip', command=user_clip, bg="purple", fg = "white")
canvas.create_window(130, 210, window=user_clip_button)

x1, x2, y1, y2 = get_default_values()
default_string = f'Current Default Values are  {x1}, {x2}, {y1}, {y2} '

label3 = tk.Label(root, text= default_string, bg="lightblue", font=('helvetica', 10))
canvas.create_window(390, 50, window=label3)

default_clip_button = tk.Button(text='Clip with Defaults', command=default_clip, bg="purple", fg="white")
canvas.create_window(390, 100, window=default_clip_button)


root.mainloop()