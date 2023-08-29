import ttkbootstrap as ttk
import tkinter as tk
import os
import sys
from tkinter import filedialog
from tkinter import messagebox
import moviepy.editor as mp
from proglog import ProgressBarLogger


# noinspection PyBroadException
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Logger Class to update progress bar widget
class MyBarLogger(ProgressBarLogger):

    def bars_callback(self, bar, attr, value, old_value=None):
        # Every time the logger progress is updated, this function is called
        percentage = (value / self.bars[bar]['total']) * 100
        update_progress_bar(percentage)


# Logger object
logger = MyBarLogger()


# Functions

# Function for Selecting Output Directory
def browseOutput():
    output_location.set(filedialog.askdirectory())
    convert_button.config(state="enabled")
    convert_button.config(cursor="hand2")


# Function to Convert Video to Audio
def convert():
    global convertTo, source, file

    # check whether input file is selected or not
    if inputFile.get() == "Select Input File":
        messagebox.showerror("Error", "Please select a file to convert")
    # check whether conversion type is selected or not
    elif conversion_type.get() == "":
        messagebox.showerror("Error", "Please select a conversion type")
    else:
        # fetch file path from input
        source = mp.VideoFileClip(inputFile.get())

        # check which conversion type is selected
        if conversion_type.get() == "1":
            convertTo = ".mp3"
        elif conversion_type.get() == "2":
            convertTo = ".wav"
        elif conversion_type.get() == "3":
            convertTo = ".ogg"
    # handle exceptions while conversion, if any.
    try:
        # fetch file name from file path
        filename = os.path.basename(inputFile.get())
        file = os.path.splitext(filename)[0]

        # check if file already exists or not
        if os.path.isfile(output_location.get() + "/" + file + convertTo):

            # ask user whether to replace the file or not
            choice = messagebox.askyesno("File Exists", "File already exists. Do you want to replace it?")

            # if user selects yes, then replace the file
            if choice:
                reset_button.config(state="disabled")  # disable reset button
                # window.config(cursor="wait")
                savefile()
                # window.config(cursor="arrow")
                reset_button.config(state="enabled")  # enable reset button

            # if user selects no, then don't replace the file
            else:
                messagebox.showinfo("Success", "File not saved")
                reset_progress_bar()

        # if file doesn't exist, then save the file
        else:
            reset_button.config(state="disabled")  # disable reset button
            # window.config(cursor="wait")
            savefile()
            # window.config(cursor="arrow")
            reset_button.config(state="enabled")  # enable reset button

    # handle exceptions if any occurs
    except Exception as e:
        messagebox.showerror("Error", str(e))
        reset_progress_bar()


# Function to Reset the Application
def reset():
    inputFile.set("Select Input File")
    output_location.set("Select Output Location")
    conversion_type.set("")
    convert_button.config(state="disabled")
    convert_button.config(cursor="arrow")
    reset_progress_bar()


# Function to perform conversion and save the file
def savefile():
    window.update_idletasks()
    window.config(cursor="wait")

    progress_bar.pack(padx=10, pady=5, fill=tk.X, expand=True)
    source.audio.write_audiofile(output_location.get() + "/" + file + convertTo, logger=logger)
    conversion_state.set("Completed")
    window.config(cursor="arrow")
    messagebox.showinfo("Success", "File saved successfully")
    reset_progress_bar()


# Function to update progress bar widget and progress percentage according to progress of conversion
def update_progress_bar(percentage):
    conversion_state.set("Converting:")
    progress_bar['value'] = percentage
    prog_percent.set(str(int(percentage)) + "%")
    window.update_idletasks()


# Function to reset progress bar widget and progress percentage
def reset_progress_bar():
    progress_bar.pack_forget()
    progress_bar['value'] = 0
    prog_percent.set("")
    conversion_state.set("")
    window.update_idletasks()


# About and Help Functions
def about():
    messagebox.showinfo("About", "Jingles: Video to Audio Converter\n"
                                 "Version: 1.0\n\n"
                                 "Developed by: Vishal Pandey\n\n"
                                 "Github: pandeyvishal28\n"
                                 "Email: vp6680599@gmail.com")


def Help():
    messagebox.showinfo("Help", "1. Select a video file to convert.\n"
                                "2. Select the output location.\n"
                                "3. Select the conversion type.\n"
                                "4. Click on convert button to convert the video file to audio file.\n"
                                "5. Click on reset button to reset the application.\n\n"
                                "Note: The converted file will be saved in the output location you have selected.")


if __name__ == '__main__':
    # Window
    window = ttk.Window(themename="dark_custom", title="Jingles: Video to Audio Converter")
    window.geometry("800x600+540+200")
    # window.resizable(False, False)

    # Icon for window
    icon = tk.PhotoImage(file=resource_path(r"assets/icon.png"))
    window.iconphoto(False, icon)

    # image for browse button
    browse = tk.PhotoImage(file=resource_path(r"assets/browse.png"))

    # Title image
    title_img = tk.PhotoImage(file=resource_path(r"assets/Jingles.png"))

    # Main Window Widgets

    # Menu Bar
    menubar = ttk.Menu(window)
    window.config(menu=menubar)

    # Themes menu
    themes_menu = ttk.Menu(menubar)
    menubar.add_cascade(label="Themes", menu=themes_menu)

    style = ttk.Style()

    themes_menu.add_command(label="Dark", command=lambda: ttk.Style.theme_use(style, themename="dark_custom"))
    themes_menu.add_command(label="Light", command=lambda: ttk.Style.theme_use(style, themename="united"))
    themes_menu.add_command(label="Vapor", command=lambda: ttk.Style.theme_use(style, themename="vapor"))

    # About menu
    about_menu = ttk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="About", command=about)

    # Help menu
    help_menu = ttk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", command=Help)

    # Heading Of Application
    title = ttk.Label(text="Jingles", font=("lucida calligraphy", 20, "bold"))
    title.pack(pady=10)
    title.config(image=title_img)

    # Frame for Taking Input File and Conversion Type
    input_frame = ttk.LabelFrame(window, text="Input", width=600, height=200)
    input_frame.pack(pady=10)

    # Frame for browsing input file
    input_loc_frame = ttk.Frame(input_frame, width=500, height=100)
    input_loc_frame.pack(pady=10, padx=10)

    # Label and Entry for Input File
    input_label = ttk.Label(input_loc_frame, text="Input File :", width=15)
    input_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

    inputFile = tk.StringVar(value="Select Input File")
    input_entry = ttk.Entry(input_loc_frame, width=50, textvariable=inputFile)
    input_entry.grid(row=0, column=1, padx=10, pady=10)

    # Browse Button for Input File
    filedialog_button = ttk.Button(input_loc_frame, text="Browse", cursor="hand2",
                                   command=lambda: inputFile.set(filedialog.askopenfilename()))
    filedialog_button.grid(row=0, column=2, padx=10, pady=10)
    # noinspection PyArgumentList
    filedialog_button.config(image=browse, bootstyle="link")

    # Frame for Taking Conversion type
    conversion_frame = ttk.Frame(input_frame, width=500, height=200)
    conversion_frame.pack(pady=10)

    # Convert To Label
    conversion_label = ttk.Label(conversion_frame, text="Convert To: ")
    conversion_label.pack(padx=10, pady=10, side=tk.LEFT)

    conversion_type = tk.StringVar()

    # Dictionary for Conversion Types
    conversion_values = {"MP3": 1, "WAV": 2, "OGG": 3}

    # Label and Radio Buttons for Conversion Type
    for (text, value) in conversion_values.items():
        ttk.Radiobutton(conversion_frame, text=text, value=value, variable=conversion_type, cursor="hand2").pack(padx=10,
                                                                                                                 pady=10,
                                                                                                                 side=tk.LEFT)
    # Frame for Output
    output_frame = ttk.LabelFrame(window, text="Output", width=600, height=200)
    output_frame.pack(pady=10)

    # Frame for browsing output location
    loc_sel_frame = ttk.Frame(output_frame, width=500, height=100)
    loc_sel_frame.pack(pady=10, padx=10)

    # Label and Entry for Output Location
    output_label = ttk.Label(loc_sel_frame, text="File Location :", width=15)
    output_label.pack(padx=10, pady=10, side=tk.LEFT)

    output_location = tk.StringVar(value="Select Output Location")
    output_entry = ttk.Entry(loc_sel_frame, width=50, textvariable=output_location)
    output_entry.pack(padx=10, pady=10, side=tk.LEFT)

    # Browse Button for Output Location
    output_browse_button = ttk.Button(loc_sel_frame, text="Browse", cursor="hand2", command=browseOutput)
    output_browse_button.pack(padx=10, pady=10, side=tk.LEFT)
    # noinspection PyArgumentList
    output_browse_button.config(image=browse, bootstyle="link")

    # Frame for Progress Bar
    progress_bar_frame = ttk.Frame(output_frame, width=500, height=20)
    progress_bar_frame.pack(pady=5)

    progress_bar = ttk.Progressbar(progress_bar_frame, orient=tk.HORIZONTAL, length=600, mode="determinate", maximum=100,
                                   value=0, takefocus=True)
    # noinspection PyArgumentList
    progress_bar.config(bootstyle="success-striped")

    # Frame for Progress Percentage
    progress_frame = ttk.Frame(output_frame, width=500, height=20)
    progress_frame.pack(pady=5)

    # conversion state label ( converting or completed  )
    conversion_state = tk.StringVar(value=" ")
    progress_label = ttk.Label(progress_frame, width=15, textvariable=conversion_state)
    progress_label.pack(padx=2, pady=5, side=tk.LEFT)

    # progress percentage label
    prog_percent = tk.StringVar(value="")
    progress_percentage = ttk.Label(progress_frame, textvariable=prog_percent, width=5)
    progress_percentage.pack(padx=2, pady=5, side=tk.LEFT)

    # Frame for Buttons
    button_frame = ttk.Frame(output_frame, width=500, height=20)
    button_frame.pack(pady=2)

    # Convert Button
    convert_button = ttk.Button(button_frame, text="Convert", width=15, state="disabled", command=convert)
    convert_button.pack(padx=10, pady=10, side=tk.LEFT)
    # noinspection PyArgumentList
    convert_button.config(bootstyle="outline")

    # Reset Button
    reset_button = ttk.Button(button_frame, text="Reset", width=15, state="disabled", command=reset)
    reset_button.pack(padx=10, pady=10)
    # noinspection PyArgumentList
    reset_button.config(bootstyle="outline")

    # Initialize the window
    window.mainloop()
