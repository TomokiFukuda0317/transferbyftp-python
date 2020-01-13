# transferbyftp-python

## Feature
ファイル転送プログラム：transferbyftp-python
ファイル転送プログラム(GUI tkinterを使用)：file_transfer_with_tkinter.py
またクライアント側で、ファイル転送をトリガーに処理実行を行うプログラム：dirwatch.py

## Requirements

## System
Python: 3.7.4

## Usage
```
python file_transfer.py　-t ${対象のcsvファイル} -r ${転送先のパス} -H ${ホスト名} -P ${ポート番号} -I ${ユーザ名}
 -i ${公開鍵}
```

## License

MIT

##  Author

Tomoki Fukuda

### 備考
クライアント側
clientPCからUbuntサーバへftp/pythonを使ったデータ転送
1対N通信を想定し、同時送信対策とファイル名が被らないよう日付+乱数でユニークにする

サーバ側
ファイル受信をトリガーに処理を実行する無料の機能がなかったので、今回はwatchdogでファイル監視（cronでも良い）



