
import argparse
import paramiko
import zipfile
import logging
import datetime
import random
import os

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
    unzip_file_name = remote_path.strip(".csv") + "_" + file_name + ".csv"

    # ZIPファイルを作成/ZIPファイルに追加
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as f:
        f.write(remote_path, unzip_file_name)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-local_path', None)
    parser.add_argument('-remote_path', "/home/ubuntu/files/archive")
    parser.add_argument('-u', 'ubunut')
    parser.add_argument('-I', '192.168.1.1')
    parser.add_argument('-P', 22)
    parser.add_argument('-i', '/Users/tomoki/.ssh/id_rsa_ftp')
    argparse_args = parser.parse_args()
    file_transfer(argparse_args)

