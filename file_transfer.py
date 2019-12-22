#!/usr/bin/env python
import paramiko
import sys
import zipfile,os
import logging
import datetime
logging.basicConfig(filename='log/file_transfer.log', level=logging.DEBUG)

HOST = '153.126.154.31'
PORT = 22 # SFTPのポート
USER = 'ubuntu'
KEY_FILE = '/Users/tomoki/.ssh/id_rsa_ftp'
# KEY_FILE = '/Users/tomoki/vagrant/ubunt_server/.vagrant/machines/default/virtualbox/private_key' # 秘密鍵ファイル

# 秘密鍵ファイルからキーを取得
rsa_key = paramiko.RSAKey.from_private_key_file(KEY_FILE)

# 秘密鍵ファイルにパスフレーズを設定している場合は下記
# PASSPHRASE = 'passphrase'
# rsa_key = paramiko.RSAKey.from_private_key_file(KEY_FILE, PASSPHRASE)

args = sys.argv

current_time = datetime.datetime.today().strftime("%Y%m%d_%H%M%S")
print("現在時刻："+current_time)
print("転送ファイル名：" + args[1])
#os.chdir('/Users/tomoki/dev2')
zip_file = "file.zip"

# 圧縮するファイルのディレクトリへ移動
#os.chdir('C:\\user1\\data')

# ZIPファイルを作成/ZIPファイルに追加
with zipfile.ZipFile(zip_file,'w') as tmp:
    tmp.write(args[1], compress_type=zipfile.ZIP_DEFLATED)


print(zip_file)

local_path = zip_file
remote_path = "/home/ubuntu/files/"+current_time


def main(local_file,remote_file):
    """
    SFTPでファイル転送
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, PORT, USER, pkey=rsa_key) # キーを指定することでパスワードは必要なし
        sftp = client.open_sftp()
        sftp.mkdir(remote_path)
        sftp.put(local_file,remote_file+"/"+zip_file)
        print("転送完了")

    except Exception as e:
        logging.error(e)
        print(e)
        print("転送失敗")

    finally:
        sftp.close()
        client.close()

if __name__ == "__main__":
    main(local_path,remote_path)