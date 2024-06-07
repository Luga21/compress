import customtkinter as ctk
from tkinter import filedialog
from moviepy.editor import VideoFileClip
from threading import Thread
import time

class VideoCompressor(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
        self.title("Video Compressor")
        self.geometry("600x600")

        self.input_label = ctk.CTkLabel(self, text="Input Video:")
        self.input_label.pack(pady=10)

        self.input_entry = ctk.CTkEntry(self, width=250)
        self.input_entry.pack(pady=10)

        self.browse_input_button = ctk.CTkButton(self, text="Browse video", command=self.browse_input)
        self.browse_input_button.pack(pady=10)

        self.output_label = ctk.CTkLabel(self, text="Output Video Name:")
        self.output_label.pack(pady=10)

        self.output_entry = ctk.CTkEntry(self, width=250)
        self.output_entry.pack(pady=10)

        self.bitrate_label = ctk.CTkLabel(self, text="Bitrate:")
        self.bitrate_label.pack(pady=10)

        self.bitrate_menu = ctk.CTkOptionMenu(self, values=["500k", "1000k", "2000k", "3000k"], command=self.set_bitrate)
        self.bitrate_menu.pack(pady=10)

        self.compress_button = ctk.CTkButton(self, text="Compress Video", fg_color="#8418e9", hover_color="#4c0a8a", command=self.start_compress_video)
        self.compress_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self, width=250)
        self.progress_bar.pack(pady=10)

        self.bitrate = '500k'
        self.compress_thread = None

    def browse_input(self):
        input_path = filedialog.askopenfilename()
        self.input_entry.delete(0, ctk.END)
        self.input_entry.insert(0, input_path)

    def start_compress_video(self):
        self.compress_button.configure(state="disabled")
        self.status_label.configure(text="Compressing video...")
        self.progress_bar.set(0)
        self.compress_thread = Thread(target=self.compress_video)
        self.compress_thread.start()

    def compress_video(self):
        input_path = self.input_entry.get()
        output_name = self.output_entry.get()

        if input_path == '' or output_name == '':
            self.status_label.configure(text="Please provide input video and output name.")
            self.compress_button.configure(state="normal")
            return

        try:
            clip = self.create_clip(input_path)
            if clip is None:
                self.status_label.configure(text="Error creating clip object.")
                self.compress_button.configure(state="normal")
                return

            output_path = f"{output_name}.mp4"
            duration = clip.duration
            self.compress_video_threaded(clip, output_path, duration)

        except Exception as e:
            self.status_label.configure(text=f"Error compressing video: {str(e)}")
        finally:
            self.compress_button.configure(state="normal")

    def create_clip(self, input_path):
        try:
            return VideoFileClip(input_path)
        except Exception as e:
            print(f"Error creating clip object: {str(e)}")
            return None

    def compress_video_threaded(self, clip, output_path, duration):
        last_time = 0
        for t in range(int(duration)):
            self.update_progress_bar(t, duration)
            if t - last_time > 10:
                last_time = t
                self.update_status_label(t, duration)
            time.sleep(0.1)  # Simulate processing time
        clip.write_videofile(output_path, bitrate=self.bitrate)
        self.status_label.configure(text="Video compressed successfully  ;)")
        self.compress_thread = None

    def update_progress_bar(self, t, duration):
        self.progress_bar.set(t / duration * 100)
        self.update_idletasks()

    def update_status_label(self, t, duration):
        self.status_label.configure(text=f"Compressing video... ({t}/{int(duration)})")
        self.update_idletasks()

    def set_bitrate(self, bitrate):
        self.bitrate = str(bitrate)

if __name__ == "__main__":
    app = VideoCompressor()
    app.mainloop()