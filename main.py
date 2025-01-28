from tkinter import *
import json
import random
import os

# Const
H1_FONT = ("Arial", 24, "bold")
REGULAR_FONT = ("Arial", 16)
BUTTON_FONT = ("Arial", 18, "bold")
TEXT_FONT = ("Arial", 24, "bold")
PRIMARY_COLOR = "#0081ff"
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 300
MAX_LINE_LENGTH = 80
SCROLL_DELAY = 10000 
text_idx = random.randint(0, 1)

window = Tk()
window.title("Typing Speed Test")
window.minsize(720, 720)
window.config(padx=20, pady=20)

# ------------------------------ Utility Functions -----------------------------#
def count_down(count):
    count_sec = count % 60
    if count_sec == 0:
        count_sec = f"{count}"
    elif count_sec < 10:
        count_sec = f"0{count_sec}"
    timer_text.config(text=f"{count_sec}s")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else :
        wpm = check_words()
        type_input.destroy()
        if wpm < 40 :
            result_label.config(text="POOR", fg="RED")
            score_label.config(text=f"Your speed type is {wpm} WPM \nYou need to practice more!")
        else :
            result_label.config(text="GREAT", fg="GREEN")
            score_label.config(text=f"Your speed type is {wpm} WPM \nThat's great, You can upgrade your typing skill by practice")
        

def show_input():
    type_input.focus()
    type_input.grid(row=4, column=0)

def start_timer():
    show_input()
    timer = 60
    start_button.destroy()
    count_down(timer)
    auto_scroll()

def read_text():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'data.json')
    with open(file_path, 'r') as datafile:
        data = json.load(datafile)
        text = data['texts'][text_idx]
        return wrap_text(text, MAX_LINE_LENGTH)

def wrap_text(text, max_length):
    words = text.split()
    wrapped_lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += (word + " ")
        else:
            wrapped_lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        wrapped_lines.append(current_line.strip())

    return "\n".join(wrapped_lines)

def auto_scroll():
    canvas.yview_scroll(1, "units")
    if canvas.yview()[1] < 1.0:
        window.after(SCROLL_DELAY, auto_scroll)

def check_words():
    word_counter = 0
    my_words = type_input.get().split(" ")
    text_words = read_text().replace("\n", " ").split(" ")
    for i in range(len(my_words)) :
        if my_words[i] == text_words[i] :
            word_counter += 1
    
    return word_counter
        

# ------------------------------ UI -----------------------------#
# Set elemen
title_label = Label(window, text="Typing Speed Test", font=H1_FONT, justify=CENTER)
timer_text = Label(window, text="60s", font=REGULAR_FONT)

frame = Frame(window)
frame.grid(row=2, column=0, columnspan=4, pady=10)

canvas = Canvas(frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="GRAY")
scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
scrollable_frame = Frame(canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

example_text = f"\n{read_text()}"
text_label = Label(scrollable_frame, text=example_text, font=TEXT_FONT, justify=CENTER, wraplength=CANVAS_WIDTH-20, bg="GRAY", fg="White")
text_label.pack()

canvas.grid(row=0, column=0, sticky="news")
scrollbar.grid(row=0, column=1, sticky="ns")

start_button = Button(window, text="START", command=start_timer, font=BUTTON_FONT, fg="WHITE", bg=PRIMARY_COLOR, border=None, highlightthickness=0)
type_input = Entry(window, width=60, font=REGULAR_FONT)

score_label = Label(window, text="", font=REGULAR_FONT)
result_label = Label(window, text="", font=TEXT_FONT)
copyright_label = Label(window, text="© Iksan Risandy", font=REGULAR_FONT)

# Placing elemen
title_label.grid(row=0, column=0, columnspan=4)
timer_text.grid(row=1, column=0, columnspan=4)
frame.grid(row=2, column=0, columnspan=4, pady=10)
start_button.grid(row=3, column=0, columnspan=4, pady=10)
result_label.grid(row=5, column=0, columnspan=4, pady=25)
score_label.grid(row=6, column=0, columnspan=4, pady=10)
copyright_label.grid(row=7, column=0, columnspan=4, pady=10)



window.mainloop()
