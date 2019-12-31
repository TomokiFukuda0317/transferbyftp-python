#!/usr/bin/env python
"""
    実行コマンド　
    $ python file_transfer.py　${対象のcsvファイル}
"""

import paramiko
import sys
import zipfile
import logging
import datetime
import random
import os
logging.basicConfig(filename='log/file_transfer.log', level=logging.DEBUG)

HOST = '153.126.154.31'
PORT = 22
USER = 'ubuntu'
KEY_FILE = '/Users/tomoki/.ssh/id_rsa_ftp'

# 秘密鍵ファイルからキーを取得
rsa_key = paramiko.RSAKey.from_private_key_file(KEY_FILE)

# 秘密鍵ファイルにパスフレーズを設定している場合は下記
# PASSPHRASE = 'passphrase'
# rsa_key = paramiko.RSAKey.from_private_key_file(KEY_FILE, PASSPHRASE)

args = sys.argv

current_time = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
print("現在時刻："+current_time)
print("対象ファイル名：" + args[1])
tmp = str(random.random())

# 対N通信を想定し、同時送信対策とファイル名が被らないよう日付+乱数でユニークにする
file_name = "file"+current_time+"-"+tmp
zip_file = file_name+".zip"

# 解凍後のファイル名
unzip_file_name = args[1].strip(".csv")+"_"+file_name+".csv"

# ZIPファイルを作成/ZIPファイルに追加
with zipfile.ZipFile(zip_file,'w',zipfile.ZIP_DEFLATED) as tmp:
    tmp.write(args[1],unzip_file_name)
print("対象ファイルをzip化してFTPサーバへ転送します："+zip_file)

local_path = zip_file
# 転送先サーバ側のディレクトリを設定
remote_path = "/home/ubuntu/files/archive/."

def main(local_file,remote_file):
    """
    SFTPでファイル転送
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, PORT, USER, pkey=rsa_key) 
        sftp = client.open_sftp()
        sftp.put(local_file,remote_file+"/"+zip_file)
        print("転送完了しました")

    except Exception as e:
        logging.error(e)
        print(e)
        print("転送失敗")

    finally:
        sftp.close()
        client.close()
        os.remove(local_file)

if __name__ == "__main__":
    main(local_path,remote_path)