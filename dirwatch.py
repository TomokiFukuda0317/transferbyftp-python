#!/usr/bin/env python
"""
    実行コマンド　
    $ python dirwatch.py　${監視対象のディレクトリ}
"""

from __future__ import print_function

import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler



class MyHandler(PatternMatchingEventHandler):
    def __init__(self, patterns):
        super(MyHandler, self).__init__(patterns=patterns)

    def _run_command(self):
        # ファイル更新をトリガーに実行するpythonを記述
        print("ファイルに更新がありました。")

    def on_created(self, event):
        # filepath = event.src_path
        # filename = os.path.basename(filepath)
        # print(filepath)
        # if zipfile.is_zipfile(filepath):
        #     with zipfile.ZipFile(filename,'r') as zf:
        #         zf.extractall(target_dir)
        #     print('Zipファイルを解凍しました')
        # else:
        #     print('%sができました' % filename)
        
        self._run_command()

# ファイル監視の開始
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
        watch(sys.argv[1], ["*csv"])