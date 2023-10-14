from kivy.config import Config
Config.set('kivy', 'window_icon', 'your_icon.ico')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
import japanize_kivy   

import yt_dlp

class Youtube_mp4_m4a_Downloader(App):
    def build(self):
        self.youtube_url = ""

        self.icon = 'img/downloader_icon.jpg'

        # レイアウトを作成
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # タイトル部分
        title_label = Label(text="Youtube mp4 m4a ダウンローダー", font_size='24sp', halign='center', size_hint=(1, None), height=60)
        main_layout.add_widget(title_label)

        # YouTube URL 入力と "Fetch Video Info" ボタン部分
        input_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=40)
        self.url_input = TextInput(hint_text="YouTube の URL を入力してください", multiline=False, padding_x=(10, 0), padding_y=[15, 0])  # 左詰めの幅設定と上下中央寄せ
        fetch_button = Button(text="ビデオ情報を取得", size_hint=(None, None), size=(160, 40))
        fetch_button.bind(on_press=self.fetch_video_info)
        input_layout.add_widget(self.url_input)
        input_layout.add_widget(fetch_button)

        main_layout.add_widget(input_layout)

        # 見出し行を作成
        headers_layout = GridLayout(cols=6, spacing=10, size_hint=(1, None), height=40)
        headers = ["フォーマット ID", "拡張子", "解像度", "プロトコル", "ビデオコーデック", "アスペクト比"]
        for header in headers:
            header_label = Label(text=header, halign='left')
            headers_layout.add_widget(header_label)

        main_layout.add_widget(headers_layout)

        # スクロール可能な動画情報のリスト
        self.video_info_table = GridLayout(cols=6, spacing=10, size_hint_y=None, row_default_height=60)
        self.video_info_table.bind(minimum_height=self.video_info_table.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        scroll_view.add_widget(self.video_info_table)
        main_layout.add_widget(scroll_view)

        # フォーマットID入力と "Download Selected Format" ボタン部分
        download_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=40)
        self.id_input = TextInput(hint_text="フォーマット ID を入力してください", multiline=False, padding_x=(10, 0), padding_y=[15, 0])  # 左詰めの幅設定と上下中央寄せ
        download_button = Button(text="ダウンロード", size_hint=(None, None), size=(220, 40))
        download_button.bind(on_press=self.download_video)
        download_layout.add_widget(self.id_input)
        download_layout.add_widget(download_button)

        main_layout.add_widget(download_layout)

        return main_layout

    def create_colored_label(self, text, color):
        return Label(text=text, halign='left', color=get_color_from_hex(color))

    def fetch_video_info(self, instance):
        url = self.url_input.text
        self.youtube_url = self.url_input.text
        if url:
            with yt_dlp.YoutubeDL() as ydl:
                try:
                    video_info = ydl.extract_info(url, download=False)
                    self.video_info_table.clear_widgets()

                    # 動画情報をソートして表示（拡張子でソート）
                    sorted_formats = sorted(video_info['formats'], key=lambda x: x['ext'])
                    for fmt in reversed(sorted_formats):
                        if fmt['ext'] in ['mhtml', 'webm', '3gp']:
                            continue  # 'mhtml' と 'webm' を除外
                        format_id = self.create_colored_label(str(fmt['format_id']), "#FFFF00")  # 黄色
                        extension = self.create_colored_label(fmt['ext'], "#00FFFF")  # 水色
                        resolution = self.create_colored_label(fmt['resolution'],  "#FFA500")  # オレンジ
                        protocol = self.create_colored_label(fmt['protocol'], "#FF1493")  # ピンク（濃いめ）
                        video_codec = self.create_colored_label(fmt['vcodec'], "#ADFF2F")  # 黄緑
                        aspect_ratio = self.create_colored_label(str(fmt['aspect_ratio']), "#a858a8")  # 紫

                        self.video_info_table.add_widget(format_id)
                        self.video_info_table.add_widget(extension)
                        self.video_info_table.add_widget(resolution)
                        self.video_info_table.add_widget(protocol)
                        self.video_info_table.add_widget(video_codec)
                        self.video_info_table.add_widget(aspect_ratio)
                except yt_dlp.utils.DownloadError as e:
                    self.video_info_table.clear_widgets()
                    error_label = Label(text=f"エラー: {str(e)}", halign='center')
                    self.video_info_table.add_widget(error_label)
        else:
            self.video_info_table.clear_widgets()
            info_label = Label(text="YouTube の URL を入力してください", halign='center')
            self.video_info_table.add_widget(info_label)

    def download_video(self, instance):
        format_id = self.id_input.text
        if format_id:
            for fmt in self.video_info_table.children:
                info = fmt.text.split('\n')[0]
                if format_id in info:
                    with yt_dlp.YoutubeDL() as ydl:
                        video_info = ydl.extract_info(self.youtube_url, download=False)
                        for video in video_info['formats']:
                            if video['format_id'] == format_id:
                                option = {
                                    'outtmpl' : 'downloads/%(title)s_%(ext)s_%(resolution)s.%(ext)s',
                                    'format': str(format_id)
                                }
                                try:
                                    ydl_download_start = yt_dlp.YoutubeDL(option)
                                    ydl_download_start.download([self.youtube_url])
                                    self.show_download_complete()
                                except yt_dlp.utils.DownloadError as e:
                                    self.id_input.text = f"ダウンロードエラー: {str(e)}"
                                return
            self.id_input.text = "フォーマットが見つかりません。"

    def show_download_complete(self):
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text="ダウンロード完了!"))

        popup = Popup(title='通知', content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    Youtube_mp4_m4a_Downloader().run()
