#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This program creates a quit
button. When we press the button,
the application terminates.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import QCoreApplication
import wave
from pyaudio import PyAudio, paInt16
import os  # liu

framerate = 8000
NUM_SAMPLES = 2000
channels = 1
sampwidth = 1
TIME = 2

def my_compile():
    os.system('/home/liuzw/kaldi/egs/thchs30/online_demo/run_tri1.sh')  # liu
    f = open("work/trans.txt", "r")
    for i in f:
        transtxt = i.split()
    transtxt.remove(transtxt[0])
    f.close()
    f = open("online-data/models/mono/words.txt", "r")
    words = dict()
    for i in f:
        a = i.split()
        words[a[1]] = a[0]
    f.close()
    f = open("result", "w+")

    # Create a string for answer
    ans = ""
    
    for i in transtxt:
        f.write(words[i])

        ans = ans + str(words[i])

    return ans


def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()


def my_record():
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=1,
                     rate=framerate, input=True,
                     frames_per_buffer=NUM_SAMPLES)
    my_buf = []
    count = 0
    while count < TIME * 10:  # 控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)  # 一次性录音采样字节大小
        my_buf.append(string_audio_data)
        count += 1
        print('.')
    save_wave_file('/home/liuzw/kaldi/egs/thchs30/online_demo/online-data/audio/01.wav', my_buf)
    stream.close()


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        qbtn = QPushButton('Record', self)
        qbtn.clicked.connect(my_record)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(85, 20)

        cbtn = QPushButton('Compile', self)
        cbtn.clicked.connect(recog_ans = my_compile)
        cbtn.resize(cbtn.sizeHint())
        cbtn.move(85, 50)

        # text print
        self.text = recog_ans

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Voice Recognition')
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()
        
        
    def drawText(self, event, qp):
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
