import customtkinter as ctk
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

money = 1000
result_label = None

symbols = ["✿", "✈", "❤", "♕", "☭", "➆", "✚"]

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def firstMenu():
    clear_window()
    frame = ctk.CTkFrame(root)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    label = ctk.CTkLabel(frame, text='Домашнее меню', font=("Arial", 20))
    label.pack(pady=10)

    button = ctk.CTkButton(frame, text='Однорукий бандит', command=oneHandThief)
    button.pack(pady=20)

def oneHandThief():
    clear_window()
    global money, result_label

    frame = ctk.CTkFrame(root)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    label = ctk.CTkLabel(frame, text='Однорукий бандит', font=("Arial", 20))
    label.pack(pady=10)

    labelmoney = ctk.CTkLabel(frame, text=f"Баланс: {money}", font=("Arial", 16))
    labelmoney.pack(pady=10)

    labelprice = ctk.CTkLabel(frame, text=f"Ставка: 250", font=("Arial", 16))
    labelprice.pack(pady=10)

    button_home = ctk.CTkButton(frame, text='Вернуться домой', command=firstMenu)
    button_home.pack(pady=10)

    button_spin = ctk.CTkButton(frame, text='Крутануть автомат',
                                command=lambda: game(labelmoney))
    button_spin.pack(pady=10)

    result_label = ctk.CTkLabel(frame, text="", font=("Arial", 30))
    result_label.pack(pady=20)

def game(labelmoney):
    global money, result_label
    if money < 250:
        clear_window()
        label_info = ctk.CTkLabel(root, text="У вас недостаточно средств для игры", font=("Arial", 30))
        label_info.pack(pady=20)
        donat_button = ctk.CTkButton(root, text='Пополнить баланс', command=donat)
        donat_button.pack(pady=10)

    else:
        firstValue = random.choice(symbols)
        secondValue = random.choice(symbols)
        thirdValue = random.choice(symbols)

        if firstValue == secondValue == thirdValue:
            money += 1000
        elif firstValue == secondValue or secondValue == thirdValue or firstValue == thirdValue:
            money += 350
        else:
            money -= 250

        labelmoney.configure(text=f"Баланс: {money}")

        result_label.configure(text=f"{firstValue} {secondValue} {thirdValue}")

import webbrowser

def donat():
    webbrowser.open("https://www.donationalerts.com/")


if __name__ == '__main__':
    root = ctk.CTk()
    root.title("Игровой автомат")
    root.geometry('800x600')

    firstMenu()
    root.mainloop()
