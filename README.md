# work_fukuda
ftpサーバ構築

雑多メモ
ftpサーバとして本当にたってる？？

ssh ubuntu@153.126.154.31 -i ~/.ssh/id_rsa_ftp

sudo apt install vsftpd
sudo apt-get install vim

$ sudo su
$ useradd -m ftp-user
$ passwd ftp-user # パスワード設定

FTP用のディレクトリ作成
$ mkdir -p /var/www/ftp_dir
ディレクトリの権限変更
$ chown ftp-user /var/www/ftp_dir
$ chmod 755 /var/www/ftp_dir

FTPの初期設定
$ cp /etc/vsftpd.conf /etc/vsftpd.conf.org
$ vi /etc/vsftpd.conf

編集

FTPの接続用にユーザの登録
$ vi /etc.chroot_list

ftp-user

$ mkdir /etc/user_conf
$ vi /etc/user_conf/ftp-user
local_root=/var/www/ftp_dir

$ sudo /etc/init.d/vsftpd start



sudo apt install -y lftp
https://intellectual-curiosity.tokyo/2019/07/19/ubuntu%E3%81%A7ftp%EF%BC%88vsftpd%EF%BC%89%E3%81%8C%E8%A1%8C%E3%81%88%E3%82%8B%E3%82%88%E3%81%86%E3%81%AB%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95/

+
sudo mkdir /etc/vsftpd.user_list
















------------------
設定ファイルの変更
/etc/vsftpd.conf 
下記を変更。

$ cat <<EOF | sudo tee /etc/vsftpd.conf
listen=YES
local_enable=YES
xferlog_enable=YES
connect_from_port_20=YES
pam_service_name=vsftpd

# Enable upload by local user.
write_enable=YES

# Enable read by anonymous user (without username and password).
secure_chroot_dir=/var/run/vsftpd/empty
anonymous_enable=YES
anon_root=/srv/ftp
allow_anon_ssl=YES
no_anon_password=YES

























#サーバ環境構築手順

1. VirtualBoxのインストール
https://www.virtualbox.org/wiki/Downloads
上記から自分の端末にあったパッケージをダウンロード＆インストールする。

2. Vagrantのインストール
https://www.vagrantup.com/downloads.html
上記から自分の端末にあったパッケージをダウンロード＆インストールする。

3. Boxの選択
https://app.vagrantup.com/boxes/search
上記からインストールするOSを探す。
※ProviderがVirtualBoxであるものを選択すること。

今回は、ubuntu/bionic64を選択する。

4. インスタンスの作成
$ mkdir ~/vagrant
$ mkdir ~/vagrant/ubunt_server
$ cd ~/vagrant/ubunt_server
$ vagrant init ubuntu/bionic64


5. Vagrantfile書き換え
$ vim ./Vagrantfile
（例）ホスト側8080ポートをゲスト側80ポートにフォワードする
$ vagrant reload

Vagrantfile内
# config.vm.network "forwarded_port", guest: 80, host: 808
config.vm.network "forwarded_port", guest: 80, host: 8080

6. サーバ起動
$ vagrant up

7. vagrant@ubuntu-bionic上で
以下コマンドを実行
$ pip install watchdog
$ apt install unzip
設定
インフラ

memo------
起動
$ vagrant up
シャットダウン
$ vagrant halt
再起動
$ vagrant reload
状態確認
$ vagrant status
一時停止
$ vagrant suspend
復帰
一時停止中から復帰する。
$ vagrant resume

サーバへアクセス
＄ vagrant ssh
または
$ ssh vagrant@127.0.0.1 -P 2222 -i 秘密鍵



