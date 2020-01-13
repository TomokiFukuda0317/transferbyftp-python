#!/usr/bin/env python
"""
    実行コマンド　
    $ python dirwatch.py　-d ${監視対象のディレクトリ}
"""

from __future__ import print_function

import sys
import time
import subprocess
import os
import zipfile
import argparse
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# パーサーを作る
parser = argparse.ArgumentParser(
            prog='dirwatch', # プログラム名
            usage='ディレクトリを監視し、ファイル転送をトリガーに任意の処理を実行する', # プログラムの利用方法
            description='description', # 引数のヘルプの前に表示
            epilog='end', # 引数のヘルプの後で表示
            add_help=True, # -h/–help オプションの追加
            )
 
# 引数の追加
parser.add_argument('-d', '--watch_dir', help='監視するディレクトリを指定する', required=True)

# 引数を解析する
args = parser.parse_args()

class MyHandler(PatternMatchingEventHandler):
    def __init__(self, patterns):
        super(MyHandler, self).__init__(patterns=patterns)

    def _run_command(self):
        # ファイル更新をトリガーに実行するpythonを記述
        print("Hello World!!")

    def on_created(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        file_save_dir = "/home/ubuntu/files/." # 解凍したファイルの保存先

        print("クライアントからzipファイルを受信しました")
        print(filepath)

        with zipfile.ZipFile(filepath,'r') as zf:
            zf.extractall(file_save_dir)
        print(file_save_dir+"へzipファイルを解凍しました")

        self._run_command()

# ファイル監視の開始（watchdogを使用）
def watch(target_dir, extension):
    event_handler = MyHandler(extension)
    observer = Observer()
    observer.schedule(event_handler, target_dir, recursive=True)
    observer.start()

    # 処理が終了しないようスリープを挟んで無限ループ
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    if 2 > len(sys.argv):
        print("監視対象のディレクトリを第１引数に設定してください")
    else:
        watch(args.watch_dir, ["*zip"])