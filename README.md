# Transferbyftp python

N対1の複数通信に対応したクライアント/サーバ FTPプログラム。

## Features

- 配信対象ファイルのZIP圧縮
- FTP/SFTPによるサーバ転送
- ファイル受信トリガープログラム

## Requirements

- サーバ
    - Ubuntu 16.04 more
    - Python 3.7.0 more

- クライアント
    - Any platform
    - Python 3.7.0 more

## Usage

- サーバ

ファイル受信監視

```
$ python dirwatch.py DIRECTORY_PATH
```

- クライアント

ZIP圧縮 + ファイル転送

```
$ python file_transfer.py FILE_NAME
```

## License

MIT