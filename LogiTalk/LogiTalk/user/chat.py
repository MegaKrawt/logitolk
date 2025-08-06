import time

import customtkinter
from PIL import Image

import login
if login.seve_info is None:
    exit()

import socket

IP_serwer = '26.123.126.212'

kliet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kliet_socket.connect((IP_serwer, 55555))
kliet_socket.send(login.seve_info[0].encode())
name=kliet_socket.recv(1024).decode()
kliet_socket.setblocking(False)


window = customtkinter.CTk()
window.geometry('700x700')

menu_progres = 0
def auto_size():
    global menu_progres
    if menu_is_open:
        if menu_progres < 200:
            menu_progres += 10
        else: pass
        name_labl.configure(text=name)
        name_labl.pack(pady=(65, 0))
        rename_entry.pack(pady=5)
        rename_button.pack(pady=(0, 15))
        ls_botton.pack(pady=0)


    else:
        if menu_progres > 0:
            menu_progres -= 10
        else:
            name_labl.pack_forget()
            rename_button.pack_forget()
            rename_entry.pack_forget()
            ls_botton.pack_forget()
    frame1.configure(width=menu_progres + 60, height=window.winfo_height())
    frame2.configure(height=window.winfo_height()-75, width=window.winfo_width() - (menu_progres + 60 + 10) - 5)
    frame2.place(x=menu_progres + 60 + 10, y=5)

    input_box.configure(height=60, width=frame2.winfo_width()-60)
    input_box.place(x=frame2.winfo_x(), y=frame2.winfo_height()+10)
    enter_button.place(x=input_box.winfo_x()+input_box.winfo_width(), y=input_box.winfo_y())

    frame1.after(10, auto_size)

menu_is_open = False
def open_menu():
    global menu_is_open
    menu_is_open = not menu_is_open

def enter():
    if input_box.get() != '':
        kliet_socket.send(input_box.get().encode())
        input_box.delete(0, 'end')

def rswmsg():
    try:
        msg = kliet_socket.recv(1024).decode()
        frame2.configure(state='normal')
        frame2.insert('end', text=msg)
        frame2.configure(state='disable')
    except: pass
    frame2.after(10, rswmsg)

def rename():
    global kliet_socket, name
    kliet_options_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    kliet_options_socket.connect((IP_serwer, 12345))
    kliet_options_socket.setblocking(True)
    kliet_options_socket.send(f'rename&#&{login.seve_info[0]}&#&{rename_entry.get()}'.encode())
    if kliet_options_socket.recv(1024).decode() == 'good':
        kliet_socket.close()
        time.sleep(0.5)
        kliet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        kliet_socket.connect((IP_serwer, 55555))
        kliet_socket.send(login.seve_info[0].encode())
        name = kliet_socket.recv(1024).decode()
        kliet_socket.setblocking(False)
    kliet_options_socket.close()

def ls():
    input_box.insert('end', '/ls(): ')



frame1 = customtkinter.CTkFrame(window, fg_color='#ccaacc')
frame1.pack_propagate(False)
frame1.place(x=0,y=0)
frame2 = customtkinter.CTkTextbox(window, fg_color='#ffffff', state='disable', font=(None, 30))
frame2.place(x=0,y=0)
menu_button = customtkinter.CTkButton(frame1, image=customtkinter.CTkImage(Image.open('imgs/menu.png'), size=(50, 50)), text='', width=1, height=1, fg_color='#000099', command=open_menu)
menu_button.place(x=0,y=0)
input_box = customtkinter.CTkEntry(window, font=(None, 25))
enter_button = customtkinter.CTkButton(window, text='>', width=60, height=60, fg_color='#555599', font=(None, 45), command=enter)

name_labl=customtkinter.CTkLabel(frame1, text=name, font=(None, 20))
rename_button=customtkinter.CTkButton(frame1, text='rename', font=(None, 20), command=rename)
rename_entry=customtkinter.CTkEntry(frame1, placeholder_text='new name', font=(None, 20))

ls_botton=customtkinter.CTkButton(frame1, text='особисте', font=(None, 20), command=ls)


auto_size()
rswmsg()

window.mainloop()

# '574576(@%)illa: hello'.split('(@%)')