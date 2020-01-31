import argparse
import logging
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import file_transfer

logging.basicConfig(filename='log/file_transfer.log', level=logging.DEBUG)

# GUIプログラムtkinter
# button1(参照)クリック時の処理
def button1_clicked():
    iDir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(initialdir = iDir)
    file1.set(filepath)

# button2(start)クリック時の処理
def button2_clicked(parser):
    if file1.get():
        parser.add_argument('-local_path', default=file1.get())
        argparse_args = parser.parse_args()
        #ファイル転送
        result_flag = file_transfer.file_transfer(argparse_args)
        if result_flag:
            messagebox.showinfo('転送完了', '対象ファイルをサーバへ転送しました。\n対象ファイル：' + file1.get())
        else:
            messagebox.showinfo('転送失敗','転送に失敗しました。\n選択したファイルが正しいか確認してください。')

    else:
        messagebox.showinfo('ファイル未選択','ファイルを選択してください。')

def tkinter_start(parser):
    # rootの作成
    root = Tk()
    root.title('ファイル転送')
    root.resizable(False, False)

    # Frame1の作成
    frame1 = ttk.Frame(root, padding=10)
    frame1.grid()

    # 参照ボタンの作成
    button1 = ttk.Button(root, text=u'参照', command=button1_clicked)
    button1.grid(row=0, column=3)

    # 「ファイル」ラベルの作成
    s = StringVar()
    s.set('対象ファイル>>')
    label1 = ttk.Label(frame1, textvariable=s)
    label1.grid(row=0, column=0)

    # 参照ファイルパス表示ラベルの作成
    global file1
    file1 = StringVar()
    file1_entry = ttk.Entry(frame1, textvariable=file1, width=50)
    file1_entry.grid(row=0, column=2)

    # Frame2の作成
    frame2 = ttk.Frame(root, padding=(0,5))
    frame2.grid(row=1)

    # Startボタンの作成
    button2 = ttk.Button(frame2, text='Start', command=lambda:button2_clicked(parser))
    button2.pack(side=LEFT)

    # Cancelボタンの作成
    button3 = ttk.Button(frame2, text='Cancel', command=quit)
    button3.pack(side=LEFT)

    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('-remote_path', default="/home/ubuntu/files/archive")
    parser.add_argument('-u', default='ubuntu')
    parser.add_argument('-I', default='153.126.154.31')
    parser.add_argument('-P', default=22)
    parser.add_argument('-i', default='/Users/tomoki/.ssh/id_rsa_ftp')
    tkinter_start(parser)
