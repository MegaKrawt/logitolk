import customtkinter
from PIL import Image

import socket
kliet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kliet_socket.connect(('26.123.126.212', 12345))

'''
msg = (kliet_socket.recv(1024).decode())
kliet_socket.send('msg'.encode())
'''

win_register = customtkinter.CTk()
win_register.geometry('700x400')
events_dict = {
    '1':'не вірний логін або пароль',
    '2':'такий логін вже зайнятий',
    '3':'',
    '4':'',
    '5':'',
}

def auto_sizel():
    frame1.configure(width=win_register.winfo_width()//10*6, height=win_register.winfo_height())
    img_bg.configure(size=(win_register.winfo_width()//10*6, win_register.winfo_height()))
    img_bg_labl.configure(image=img_bg)

    frame2.configure(width=win_register.winfo_width()//10*4, height=win_register.winfo_height())
    frame2.place(x=win_register.winfo_width() // 10 * 6, y=0)

    eventsLabel.pack(pady=(win_register.winfo_height()//10*2, 0))

    frame1.after(50, auto_sizel)

seve_info = None
def log_in():
    if "&#&" in loginEntry.get() or "&#&" in passwordEntry.get():
        eventsLabel.configure(text='заборонено: &#&')
        raise ValueError("&#&")
    kliet_socket.send(f'logintry&#&{loginEntry.get()}&#&{passwordEntry.get()}'.encode())
    msg = (kliet_socket.recv(1024).decode())
    if msg == 'good':
        global seve_info
        seve_info = [loginEntry.get(), passwordEntry.get()]
        win_register.destroy()
    else:
        eventsLabel.configure(text=msg)


def create_account():
    username_Entry.pack(pady=10)

    if len(username_Entry.get()) >= 1:
        kliet_socket.send(f'createtry&#&{loginEntry.get()}&#&{passwordEntry.get()}&#&{username_Entry.get()}'.encode())
        msg = (kliet_socket.recv(1024).decode())
        eventsLabel.configure(text=msg)
    else: pass


frame1 = customtkinter.CTkFrame(win_register, width= win_register.winfo_width()//10*6, height= win_register.winfo_height(), fg_color='#aa00aa')
frame1.place(x=0, y=0)
frame1.pack_propagate(False)
img_bg = customtkinter.CTkImage(Image.open('imgs/bg.png'))
img_bg_labl = customtkinter.CTkLabel(frame1, text='welcome', image=img_bg, font=(None, 50, 'bold'), text_color='#ffffff')
img_bg_labl.pack(side='left')
frame2 = customtkinter.CTkFrame(win_register, width= win_register.winfo_width()//10*4, height= win_register.winfo_height(), fg_color='#ffffff')
frame2.place(x= win_register.winfo_width()//10*6, y=0)
frame2.pack_propagate(False)
eventsLabel = customtkinter.CTkLabel(frame2, font=(None, 20, 'bold'), text_color='#ff0000', text='')
eventsLabel.pack()
loginEntry = customtkinter.CTkEntry(frame2, fg_color='#eae6ff', corner_radius=100, placeholder_text='login', height=40, width=200, font=(None, 20))
loginEntry.pack()
passwordEntry = customtkinter.CTkEntry(frame2, fg_color='#eae6ff', corner_radius=100, placeholder_text='password', height=40, width=200, font=(None, 20))
passwordEntry.pack()
yviuni_button = customtkinter.CTkButton(frame2, text='увійти', fg_color='#d06fc0', text_color='#ffffff', command=log_in, font=(None, 20), height=40, width=200)
yviuni_button.pack(pady=10)
create_account_button = customtkinter.CTkButton(frame2, text='зарееструватись', fg_color='#d06fc0', text_color='#ffffff', command=create_account, font=(None, 20), height=40, width=200)
create_account_button.pack()
username_Entry = customtkinter.CTkEntry(frame2, fg_color='#eae6ff', corner_radius=100, placeholder_text='user name', height=40, width=200, font=(None, 20))

auto_sizel()
win_register.mainloop()

kliet_socket.close()
