from tkinter import *
from tkinter import messagebox
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

flash_card_df = pd.read_csv('data/french_words.csv')
flash_dict_list = flash_card_df.to_dict(orient='records')
# french_word_list = df.French.to_list()
# flash_dict = {row.French: row.English for (index, row) in df.iterrows()}

try:
    know_card_df = pd.read_csv('data/know_card.csv')
    know_card_dict_list = know_card_df.to_dict(orient='records')
except FileNotFoundError:
    know_card_dict_list = []
else:
    for card_dict in know_card_dict_list:
        flash_dict_list.remove(card_dict)

current_card_dict = {}
c = 0

def know_card():
    flash_dict_list.remove(current_card_dict)
    know_card_dict_list.append(current_card_dict)
    df = pd.DataFrame(know_card_dict_list)
    # print(flash_dict_list)
    df.to_csv('data/know_card.csv', index=False)
    next_card()


def next_card():
    global current_card_dict
    global flip_timer
    window.after_cancel(flip_timer)
    print(f'Still have {len(flash_dict_list)} to learn.')
    if len(flash_dict_list) == 0:
        messagebox.showinfo(title='cong!!', message='You Finish!!')
        return
    current_card_dict = random.choice(flash_dict_list)
    canvas.itemconfig(canvas_img, image=card_front_img)
    canvas.itemconfig(canvas_text_title, text="French", fill='black')
    canvas.itemconfig(canvas_text_word, text=current_card_dict['French'], fill='black')
    flip_timer = window.after(3000, ans_card, 0)


def ans_card(c):
    global flip_timer
    if c % 2 == 0:
        canvas.itemconfig(canvas_img, image=card_back_img)
        canvas.itemconfig(canvas_text_title, text="English", fill='white')
        canvas.itemconfig(canvas_text_word, text=current_card_dict['English'], fill='white')
    else:
        canvas.itemconfig(canvas_img, image=card_front_img)
        canvas.itemconfig(canvas_text_title, text="French", fill='black')
        canvas.itemconfig(canvas_text_word, text=current_card_dict['French'], fill='black')
    c += 1
    flip_timer = window.after(3000, ans_card, c)


# ----------------------------------
window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, ans_card)

# Canvas
canvas = Canvas(width=800, height=525)
card_front_img = PhotoImage(file='images/card_front.png')
card_back_img = PhotoImage(file='images/card_back.png')
canvas_img = canvas.create_image(400, 262, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

canvas_text_title = canvas.create_text(400, 150, text='', font=("Ariel", 40, 'italic'))
canvas_text_word = canvas.create_text(400, 262, text='', font=("Ariel", 60, 'bold'))
canvas.grid(row=0, column=0, columnspan=2)

# Button
right_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR,
                      command=know_card)
right_button.grid(row=1, column=1, )

wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR,
                      command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()
