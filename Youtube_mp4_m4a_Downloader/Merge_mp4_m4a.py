from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from datetime import datetime
import subprocess
from kivy.graphics import Color, Rectangle
import japanize_kivy

### 日本語の文字化け対策
japanize_kivy.mode_on()

class VideoMergerApp(App):
    def build(self):
        self.input_mp4 = None
        self.input_m4a = None

        self.icon = 'img/merge_icon.jpg'

        layout = GridLayout(rows=8, cols=1, spacing=10, padding=10)

        ######
        file_chooser_mp4_layout = GridLayout(rows=1, cols=1, size_hint_y=None)

        # スクロール可能なフォルダ選択エリアを作成
        self.file_chooser_mp4 = FileChooserListView(
            path="./downloads", filters=["*.mp4"], dirselect=True,
            size_hint_y=None, height=100
        )
        file_chooser_mp4_layout.add_widget(self.file_chooser_mp4)
        file_chooser_mp4_scroll = ScrollView(size_hint=(1, None), size=(150, 150))
        file_chooser_mp4_scroll.add_widget(file_chooser_mp4_layout)

        # self.file_chooser_mp4の背景色を変更
        with self.file_chooser_mp4.canvas.before:
            Color(0.0, 0.3, 0.6)  # 青
            self.file_chooser_mp4_rect = Rectangle(pos=self.file_chooser_mp4.pos, size=self.file_chooser_mp4.size)
            self.file_chooser_mp4.bind(pos=self.update_rect, size=self.update_rect)

        file_chooser_mp4_layout.bind(minimum_height=file_chooser_mp4_layout.setter('height'))

        self.file_chooser_mp4.bind(selection=self.on_file_mp4_selection)
        ####

        ###############
        file_chooser_m4a_layout = GridLayout(rows=1, cols=1, size_hint_y=None)


        self.file_chooser_m4a = FileChooserListView(
            path="./downloads", filters=["*.m4a"], dirselect=True,
            size_hint_y=None, height=100
        )

        file_chooser_m4a_layout.add_widget( self.file_chooser_m4a)
        file_chooser_m4a_scroll = ScrollView(size_hint=(1, None), size=(150, 150))
        file_chooser_m4a_scroll.add_widget(file_chooser_m4a_layout)

        # self.file_chooser_m4aの背景色を変更
        with self.file_chooser_m4a.canvas.before:
            Color(0.0, 0.3, 0.6, 1)  # 青
            self.file_chooser_m4a_rect = Rectangle(pos=self.file_chooser_m4a.pos, size=self.file_chooser_m4a.size)
            self.file_chooser_m4a.bind(pos=self.update_rect, size=self.update_rect)

        file_chooser_m4a_layout.bind(minimum_height=file_chooser_m4a_layout.setter('height'))

        self.file_chooser_m4a.bind(selection=self.on_file_m4a_selection)
        ############


        mp4_label = Label(text="Select mp4 file:", size_hint_y=None, height=30)
        mp4_label.border = (1, 1, 1, 1)
        m4a_label = Label(text="Select m4a file:", size_hint_y=None, height=30)
        m4a_label.border = (1, 1, 1, 1)

        self.status_label = Label(text="")

        layout.add_widget(mp4_label)
        layout.add_widget(file_chooser_mp4_scroll)
        layout.add_widget(m4a_label)
        layout.add_widget(file_chooser_m4a_scroll)

        merge_button = Button(
            text="Merge mp4 and m4a", on_press=self.merge_video_and_audio, size_hint_y=None, height=40
        )
        layout.add_widget(merge_button)

        return layout

    def on_file_mp4_selection(self, instance, value):
        self.input_mp4 = value[0]

    def on_file_m4a_selection(self, instance, value):
        self.input_m4a = value[0]

    def merge_video_and_audio(self, instance):
        if self.input_mp4 and self.input_m4a:
            current_time = datetime.now().strftime('%Y%m%d%H%M%S')
            output_file = f"merged/merge_{current_time}.mp4"
            ffmpeg_command = [
                "ffmpeg",
                "-i", self.input_mp4,
                "-i", self.input_m4a,
                "-c", "copy",
                "-shortest",
                output_file,
            ]
            subprocess.run(ffmpeg_command)

            self.status_label.text = f"Merge complete. Output: {output_file}"

            popup = Popup(title="Merge Complete", content=Label(text=f"Output: {output_file}"), size_hint=(1, 0.2),  size=(50, 50))
            popup.open()
        else:
            self.status_label.text = "Please select both mp4 and m4a files."

    def update_rect(self, instance, value):
        self.file_chooser_mp4_rect.pos = instance.pos
        self.file_chooser_mp4_rect.size = instance.size

        self.file_chooser_m4a_rect.pos = instance.pos
        self.file_chooser_m4a_rect.size = instance.size


if __name__ == "__main__":
    VideoMergerApp().run()
