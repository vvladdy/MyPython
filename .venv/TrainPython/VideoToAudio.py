# pip install moviepy редактор видео

import os
import moviepy.editor
from pathlib import Path

from moviepy.video.compositing.CompositeVideoClip import clips_array
from moviepy.video.fx.resize import resize

videofile_file = Path('Files/video11.mp4')

video = moviepy.editor.VideoFileClip(f'{videofile_file}')
# print(video.size)
print(video.duration/60)

# audio = video.audio
# audio.write_audiofile(f'Files/{videofile_file.stem}.mp3')

print(video.fps)
video2 = video.subclip(t_end=(0, 0,30))
print(video2.duration)
# video2.write_videofile('Files/Video11_30sec.mp4')

video3 = moviepy.editor.VideoFileClip('Files/Video11_30sec.mp4')
# поворот видео на градусы
video3 = video3.rotate(180)
# video3.write_videofile('Files/Video11_30sec_rotat.mp4')

# Добовить громкости
video3.volumex(1)
# video3.write_videofile('Files/Video11_30sec_volumex.mp4')
print(video3.size)

# изменение размера видео коэф-нт больше\меньше
video_resize = resize(video2, 0.5)
print(video_resize.size)
# video_resize.write_videofile('Files/Video11_30sec_shrink.mp4')

# наложение звуковой дорожки из одного видео на другое
# video3 = video.set_audio(video2)

# объединение видео
fc = clips_array([[video3, video_resize],
                  [video, video2]])
fc.write_videofile('Files/Video11_30sec_togather.mp4')




# os.startfile(r"D:\MyPythonFolder\MyPython\.venv\TrainPython\Files"
#              r"\Video11_30sec_volumex.mp4")
os.startfile(r"D:\MyPythonFolder\MyPython\.venv\TrainPython\Files"
             r"\Video11_30sec_togather.mp4")
