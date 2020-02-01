# transferbyftp-python

## Feature
ファイル転送プログラム：file_transfer.py
ファイル転送プログラム(GUI)：file_transfer_tkinter.py
またクライアント側で、ファイル転送をトリガーに処理実行を行うプログラム：dirwatch.py

## Requirements

## System
Python: 3.7.4

## Usage
```
python file_transfer.py　-local_path ${対象のcsvファイルのパス} -remote_path ${転送先のパス} -u ${ホスト名} -I ${ユーザ名}　-P ${ポート番号} -i ${公開鍵}
```
（local_pathは必須。それ以外はソースにdefaultを設定している。）
## License

MIT

##  Author

Tomoki Fukuda

### 備考
クライアント側
clientPCからUbuntサーバへftp/pythonを使ったデータ転送
1対N通信を想定し、同時送信対策とファイル名が被らないよう日付+乱数でユニークにする

サーバ側
ファイル受信をトリガーに処理を実行する無料の機能がなかったので、今回はwatchdogでファイル監視。（cronでも良い）
Ubuntu の場合、下記をインストール
+ apt-get install watchdog



