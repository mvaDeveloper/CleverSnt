import tkinter as tk
from tkinter import ttk


def title_label(window, text, x, y):
    label = tk.Label(
        window,
        bg="#f0eae1",
        text=text,
        font="/fonts/7454.ttf 13"
    )
    set_place(label, x, y)


def set_place(component, x, y):
    component.place(x=x, y=y)
    return component


def input_owners(window, text, component, x, y):
    label = tk.Label(
        window,
        bg="#f0eae1",
        text=text,
        font="/fonts/7454.ttf 11"
    )
    set_place(label, x, y)
    set_place(component, x + 130, y)
    return component


def input_payments(window, text, component, x, y):
    label = tk.Label(
        window,
        bg="#f0eae1",
        text=text,
        font="/fonts/7454.ttf 11"
    )
    set_place(label, x-131, y)
    set_place(component, x + 30, y)
    return component


def button(window, text, command, width, x, y):
    component = tk.Button(
        window,
        text=text,
        command=command,
        width=width,
        height=2,
        background="#0099ff",
        font="/fonts/7454.ttf 11"
    )
    set_place(component, x, y)


def button_menu(window, text, command, value, x, y):
    component = tk.Button(
        window,
        text=text,
        width=25,
        height=6,
        background="#0099ff",
        activebackground='#3399ff',
        font="/fonts/7454.ttf 11"
    )
    component.bind('<Button-1>', lambda event: command(value))
    set_place(component, x, y)


def button_main_menu(window, text, command, image):
    component = tk.Button(
        window,
        text=text,
        command=command,
        bg='#3399ff',
        bd=0,
        compound=tk.TOP,
        activebackground='#3399ff',
        image=image
    )
    component.pack(side=tk.BOTTOM)


def tree(window, columns):
    component = ttk.Treeview(
            window,
            columns=columns,
            heigh=32,
            show='headings'
        )
    return component
