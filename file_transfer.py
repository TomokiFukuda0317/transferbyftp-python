
import paramiko
import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

HOST = '127.0.0.1'
PORT = 2222 # SFTPのポート
USER = 'vagrant'
KEY_FILE = '/Users/tomoki/vagrant/ubunt_server/.vagrant/machines/default/virtualbox/private_key' # 秘密鍵ファイル
# PASSPHRASE = 'passphrase'
 
# 秘密鍵ファイルからキーを取得
rsa_key = paramiko.RSAKey.from_private_key_file(KEY_FILE)
# 秘密鍵ファイルにパスフレーズを設定している場合は下記
# rsa_key = paramiko.RSAKey.from_private_key_file(KEY_FILE, PASSPHRASE)

args = sys.argv

print("第1引数：" + args[1])
local_path = args[1]
remote_path = "/home/vagrant/test/test.csv"


def main(local_file,remote_file):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, PORT, USER, pkey=rsa_key) # キーを指定することでパスワードは必要なし
        sftp = client.open_sftp()
        sftp.put(local_file,remote_file)

    except Exception as e:
        print(e)

    finally:
        sftp.close()
        client.close()



# # Open a transport
# transport = paramiko.Transport((host, port))

# # Auth
# password = "vagrant"
# username = "19950317"
# transport.connect(username = username, password = password)

# # Go!

# sftp = paramiko.SFTPClient.from_transport(transport)

# # Download

# # filepath = '/etc/passwd'
# # localpath = '/home/remotepasswd'
# # sftp.get(filepath, localpath)

# # Upload

# sftp.put(localpath, remote_path)

# # Close

# sftp.close()
# transport.close()






# import sys
# import paramiko


# args = sys.argv

# print("第1引数：" + args[1])
# local_path = args[1]
# remote_path = "/home/vagrant/test"

# HOST="127.0.0.1"
# PORT=2222
# USERNAME="vagrant"
# PASSWORD="vagrant"

# def make_path(remote_path):

#     try:
#         sftp.chdir(remote_path)  # Test if remote_path exists
#     except IOError:
#         sftp.mkdir(remote_path)  # Create remote_path
#         sftp.chdir(remote_path)

 
# def main(local_path,remote_path):
#     try:
#         client=paramiko.SSHClient()
#         client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         client.connect(HOST,port=PORT,username=USERNAME,password=PASSWORD)
#         sftp=client.open_sftp()
#         print("trying now")

#         # sftp = paramiko.SFTPClient.from_transport(transport)
#         make_path(remote_path)
#         sftp.put(local_path, '.')    # At this point, you are in remote_path in either case
 
#     except Exception as e:
#         print(e)
#         print("exception now")
 
#     finally:
#         sftp.close()
#         client.close()
#         print("done")

main(local_path,remote_path)


# # import os.path

# # def mkdir_p(sftp, remote_directory):
# #     """Change to this directory, recursively making new folders if needed.
# #     Returns True if any folders were created."""
# #     if remote_directory == '/':
# #         # absolute path so change directory to root
# #         sftp.chdir('/')
# #         return
# #     if remote_directory == '':
# #         # top-level relative directory must exist
# #         return
# #     try:
# #         sftp.chdir(remote_directory) # sub-directory exists
# #     except IOError:
# #         dirname, basename = os.path.split(remote_directory.rstrip('/'))
# #         mkdir_p(sftp, dirname) # make parent directories
# #         sftp.mkdir(basename) # sub-directory missing, so created it
# #         sftp.chdir(basename)
# #         return True

# # sftp = paramiko.SFTPClient.from_transport(transport)
# # mkdir_p(sftp, remote_path) 
# # sftp.put(local_path, '.')    # At this point, you are in remote_path
# # sftp.close()