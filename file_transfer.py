import argparse
import paramiko
import zipfile
import logging
import datetime
import random
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

logging.basicConfig(filename='log/file_transfer.log', level=logging.DEBUG)
random.seed(24)


def get_random_number_str(random_size: int = 1) -> str:
    random_num_str = ''
    for i in range(random_size):
        random_num_str += str(int(random.uniform(0, 9)))
    return random_num_str


def file_transfer(argparse_args):
    local_path = argparse_args.local_path
    remote_path = argparse_args.remote_path
    user = argparse_args.u
    host = argparse_args.I
    port = argparse_args.P
    rsa_key_file = argparse_args.i

    current_time = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    logging.info(f"現在時刻: {current_time}")
    logging.info(f"配信対象ファイル: {local_path}")
    logging.info(f"配信先PATH: {remote_path}")


    random_number_str = get_random_number_str(4)

    if local_path is None or remote_path is None:
        logging.error("local_pathとremote_pathを設定してください")
        return

    # 秘密鍵ファイルからキーを取得
    rsa_key = paramiko.RSAKey.from_private_key_file(rsa_key_file)

    # 秘密鍵ファイルにパスフレーズを設定している場合は下記
    # PASSPHRASE = 'passphrase'
    # rsa_key = paramiko.RSAKey.from_private_key_file(KEY_FILE, PASSPHRASE)

    # 対N通信を想定し、同時送信対策とファイル名が被らないよう日付+乱数でユニークにする
    file_name = "file" + current_time + "-" + random_number_str
    zip_file = file_name + ".zip"

    # 解凍後のファイル名
    unzip_file_name = local_path.strip(".csv") + "_" + file_name + ".csv"

    # ZIPファイルを作成/ZIPファイルに追加
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as f:
        f.write(local_path, unzip_file_name)
    logging.info(f"配信先ZIPファイル: {zip_file}")

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port, user, pkey=rsa_key)
        sftp = client.open_sftp()
        sftp.put(zip_file, remote_path + "/" + zip_file)
        logging.info(f"転送完了しました: {zip_file}")

    except Exception as e:
        logging.error(f"転送失敗!!: {e}")

    finally:
        sftp.close()
        client.close()
        os.remove(local_path)




# GUIプログラムtkinter
# button1(参照)クリック時の処理
def button1_clicked():
    iDir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(initialdir = iDir)
    file1.set(filepath)

# button2(start)クリック時の処理
def button2_clicked(parser):
    if file1.get():
        messagebox.showinfo('転送完了', u'以下の対象ファイルをサーバへ転送しました。\n' + file1.get())
        parser.add_argument('-local_path', default=file1.get())
        argparse_args = parser.parse_args()
        file_transfer(argparse_args)
    else:
        messagebox.showinfo('ファイルを選択してください。')

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

    # ラベルの作成
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-remote_path', default="/home/ubuntu/files/archive")
    parser.add_argument('-u', default='ubuntu')
    parser.add_argument('-I', default='153.126.154.31')
    parser.add_argument('-P', default=22)
    parser.add_argument('-i', default='/Users/tomoki/.ssh/id_rsa_ftp')
    tkinter_start(parser)
