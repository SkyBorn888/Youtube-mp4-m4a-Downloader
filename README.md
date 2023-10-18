# Youtube-mp4-m4a-Downloader
<img src="https://github.com/SkyBorn888/Youtube-mp4-m4a-Downloader/assets/79365546/f744f035-ed6e-4385-addc-170319fd29fc" width=45%>
<img src="https://github.com/SkyBorn888/Youtube-mp4-m4a-Downloader/assets/79365546/0514ddae-dd53-4210-8c05-b81acd952b61" width=45%>

## 概要
yt-dlp、kivyを使ったYoutubeのmp4とm4aのダウンローダー。
ffmpegコマンドを使って mp4 m4a を結合する。

## 環境
Python 3.9.13<br>
Kivy==2.2.1<br>
japanize-kivy==0.1.1<br>
yt-dlp==2023.10.13<br>
pyinstaller==5.6.2<br>
ffmpeg==ffmpeg-master-latest-win64-gpl-shared<br><br>
fonts==https://moji.or.jp/ipafont/ipaex00401/

## テスト済み環境
Windows11

## 前提条件
ffmepgをインストールする必要がある。
https://www.ffmpeg.org/

## 使い方！？ 
気が向いたら書く、バグも多いし。ケっ！

## ツリー
Youtube_mp4_m4a_Downloader<br>
├ downloads 【ダウンロードした mp4 又は m4a が置かれる】<br>
│ └ dummy.txt 【特に意味なし 消しても良い】<br>
├ img 【アイコンを配置】<br>
│ ├ downloader_icon.jpg<br>
│ ├ downloader_icon.ico<br>
│ ├ merge_icon.jpg<br>
│ └ merge_icon.ico<br>
├ merged　【mp4とm4aを結合した mp4 が置かれる】<br>
│ └ dummy.txt 【特に意味なし 消しても良い】<br>
├ resouces　【】使用しているフォントを配置<br>
│ └ 【ipaexg00401】<br>
│ 　 ├ IPA_Font_License_Agreement_v1.0.txt<br>
│ 　 ├ ipaexg.ttf<br>
│ 　 └ Readme_ipaexg00401.txt<br>
├ Merge_mp4_m4a.exe 【mp4 m4a 結合アプリ】<br>
└ Youtube_mp4_m4a_Downloader.exe　【Youtubeeから mp4 m4aをダウンロードするアプリ】<br>

## pyinstaller 実行コマンド
```sh
pyinstaller --onefile --noconsole --hiddenimport win32timezone --icon=img/icon name.ico .\hogehoge.py
```
