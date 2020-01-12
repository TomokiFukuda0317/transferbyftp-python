#!/usr/bin/env python
"""
    実行コマンド　
    $ python file_transfer.py　-t ${対象のcsvファイル} -r ${転送先のパス} -H ${ホスト名} -P ${ポート番号} -I ${ユーザ名} -i ${公開鍵}
"""

import paramiko
import sys
import zipfile
import logging
import datetime
import random
import os
import argparse
logging.basicConfig(filename='log/file_transfer.log', level=logging.DEBUG)

# パーサーを作る
parser = argparse.ArgumentParser(
            prog='file_transfer', # プログラム名
            usage='対象ファイルをサーバへ転送します', # プログラムの利用方法
            description='description', # 引数のヘルプの前に表示
            epilog='end', # 引数のヘルプの後で表示
            add_help=True, # -h/–help オプションの追加
            )
 
# 引数の追加
parser.add_argument('-t', '--target_file', help='転送する対象ファイルを指定する', required=True)
# 引数の追加
parser.add_argument('-r', '--remote_path', help='転送先のパスを指定する', required=True)
# 引数の追加
parser.add_argument('-H', '--HOST', help='接続に使用するホスト名を指定する', required=True)
# 引数の追加
parser.add_argument('-P', '--PORT', help='接続に使用するポート番号を指定する', required=True, type=int)
# 引数の追加
parser.add_argument('-I', '--USER', help='接続に使用するユーザー名を指定する', required=True)
# 引数の追加
parser.add_argument('-i', '--KEY_FILE', help='接続に使用する公開鍵ファイルを指定する', required=True)

# 引数を解析する
args = parser.parse_args()

# HOST = '153.126.154.31'
# PORT = 22
# USER = 'ubuntu'
# KEY_FILE = '/Users/tomoki/.ssh/id_rsa_ftp'

HOST = args.HOST
PORT = args.PORT
USER = args.USER
KEY_FILE = args.KEY_FILE

# 秘密鍵ファイルからキーを取得
rsa_key = paramiko.RSAKey.from_private_key_file(KEY_FILE)

# 秘密鍵ファイルにパスフレーズを設定している場合は下記
# PASSPHRASE = 'passphrase'
# rsa_key = paramiko.RSAKey.from_private_key_file(KEY_FILE, PASSPHRASE)

# args = sys.argv

current_time = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
print("現在時刻："+current_time)
target_file = args.target_file
print("対象ファイル名：" + target_file)
random_num = str(random.random())

# 対N通信を想定し、同時送信対策とファイル名が被らないよう日付+乱数でユニークにする
file_name = "file"+current_time+"-"+random_num
zip_file = file_name+".zip"

# 解凍後のファイル名
unzip_file_name = target_file.strip(".csv")+"_"+file_name+".csv"

# ZIPファイルを作成/ZIPファイルに追加
with zipfile.ZipFile(zip_file,'w',zipfile.ZIP_DEFLATED) as z:
    z.write(target_file,unzip_file_name)
print("対象ファイルをzip化してFTPサーバへ転送します："+zip_file)

local_path = zip_file
# 転送先サーバ側のディレクトリを設定
remote_path = args.remote_path
# remote_path = "/home/ubuntu/files/archive/."

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
