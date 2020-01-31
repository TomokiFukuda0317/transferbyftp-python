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

def file_transfer(argparse_args:"ArgumentParser オブジェクト") ->"送信したzipファイル名":
    local_path = argparse_args.local_path
    remote_path = argparse_args.remote_path
    user = argparse_args.u
    host = argparse_args.I
    port = argparse_args.P
    rsa_key_file = argparse_args.i
    
    # 秘密鍵ファイルからキーを取得
    rsa_key = paramiko.RSAKey.from_private_key_file(rsa_key_file)

    current_time = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    logging.info(f"現在時刻: {current_time}")
    logging.info(f"配信対象ファイル: {local_path}")
    logging.info(f"配信先PATH: {remote_path}")

    random_number_str = get_random_number_str(4)

    if local_path is None or remote_path is None:
        logging.error("local_pathとremote_pathを設定してください。")
        print("local_pathとremote_pathを設定してください。")
        return

    # ファイル名を作成、対N通信を想定し同時送信対策とファイル名が被らないよう日付+乱数でユニークにする
    unique_suffix = "file" + current_time + "-" + random_number_str
    file_name = os.path.splitext(os.path.basename(local_path))[0] + "_" + unique_suffix
    zip_file = file_name + ".zip"
    csv_file = file_name + ".csv"

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port, user, pkey=rsa_key)
        sftp = client.open_sftp()

        # ZIPファイルを作成/ZIPファイルに追加
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as f:
            f.write(local_path, csv_file)
        logging.info(f"配信先ZIPファイル: {zip_file}")
        sftp.put(zip_file, remote_path + "/" + zip_file)
        logging.info(f"転送完了しました: {zip_file}")
        result_flag = True

    except Exception as e:
        logging.error(f"転送失敗!!: {e}")
        print("転送に失敗しました。\n選択したファイルが正しいか確認してください。")
        result_flag = False

    finally:
        sftp.close()
        client.close()
        #ファイル転送後、ローカルのzipファイル削除
        os.remove(zip_file)
    return result_flag


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-local_path', default=None)
    parser.add_argument('-remote_path', default="/home/ubuntu/files/archive")
    parser.add_argument('-u', default='ubuntu')
    parser.add_argument('-I', default='153.126.154.31')
    parser.add_argument('-P', default=22)
    parser.add_argument('-i', default='/Users/tomoki/.ssh/id_rsa_ftp')
    argparse_args = parser.parse_args()
    #ファイル転送
    file_transfer(argparse_args)