#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pyaudio import PyAudio, paInt16 
import numpy as np 
from datetime import datetime 
import wave
import os
from pydub import AudioSegment
import json
from PlayCard import *
import time
class pattern:

    def match(self,input):
        poker = ["尖", "二","三","四","五","六","七","八","九","十","勾","圈", "小王", "大王"]
        trans = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "w", "W"]
        quantity = ["一个","两个","三个","四个"]
        key = input.replace(' ','')
        number = 0
        for i in range(4):
            if key[0:2] == quantity[i]:
                number = i + 1
        card = ""
        for i in range(13):
            # print(key[2:3],poker[i])
            if key[2:3] == poker[i]:
                card = trans[i]
        output = ""
        for i in range(number):
            output = output + card
        return output

def exract(saying):
    Pattern = pattern()
    for key in saying:
        if(saying[key] < 0.3):
            continue
        word = key
        #word = "一个三"
        output = Pattern.match(word)
        print(output)
        return output

class recoder:
    NUM_SAMPLES = 2000      #pyaudio内置缓冲大小
    SAMPLING_RATE = 20000    #取样频率
    LEVEL = 2000         #声音保存的阈值
    COUNT_NUM = 20      #NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
    SAVE_LENGTH = 8         #声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样
    TIME_COUNT = 30     #录音时间，单位s

    Voice_String = []

    def savewav(self,filename):
        wf = wave.open(filename, 'wb') 
        wf.setnchannels(1) 
        wf.setsampwidth(2) 
        wf.setframerate(self.SAMPLING_RATE) 
        wf.writeframes(np.array(self.Voice_String).tostring()) 
        # wf.writeframes(self.Voice_String.decode())
        wf.close() 

    def recoder(self):
        pa = PyAudio() 
        stream = pa.open(format=paInt16, channels=1, rate=self.SAMPLING_RATE, input=True, 
            frames_per_buffer=self.NUM_SAMPLES) 
        save_count = 0 
        save_buffer = [] 
        time_count = self.TIME_COUNT

        while True:
            time_count -= 1
            # print time_count
            # 读入NUM_SAMPLES个取样
            string_audio_data = stream.read(self.NUM_SAMPLES) 
            # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            # 计算大于LEVEL的取样的个数
            large_sample_count = np.sum( audio_data > self.LEVEL )
            print(np.max(audio_data))
            # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            if large_sample_count > self.COUNT_NUM:
                save_count = self.SAVE_LENGTH 
            else: 
                save_count -= 1

            if save_count < 0:
                save_count = 0 

            if save_count > 0 : 
            # 将要保存的数据存放到save_buffer中
                #print  save_count > 0 and time_count >0
                save_buffer.append( string_audio_data ) 
            else: 
            #print save_buffer
            # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
                #print "debug"
                if len(save_buffer) > 0 : 
                    self.Voice_String = save_buffer
                    save_buffer = [] 
                    print("Recode a piece of  voice successfully!")
                    return True
            if time_count==0: 
                if len(save_buffer)>0:
                    self.Voice_String = save_buffer
                    save_buffer = [] 
                    print("Recode a piece of  voice successfully!")
                    return True
                else:
                    return False

if __name__ == "__main__":
    while True:
        print("begin recording voice")
        r = recoder()
        r.recoder()
        r.savewav("test.wav")
        song = AudioSegment.from_wav("test.wav")
        song.export("test.flac",format = "flac")
        command = "curl -X POST -u  'dd71ff24-f008-4270-b4a8-fc6f10e719c8':'UMSWcHv3AUyj' --header 'Content-Type: audio/flac' --data-binary @test.flac 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?model=zh-CN_BroadbandModel'"
        res = os.popen(command).read()
        # print(res)
        res_str = json.dumps(res)
        res_str.replace(" ", "")
        res_str.replace("\n", "")
        res_dict = json.loads(res_str)
        res_dict = json.loads(res_dict)
        print("\nRESULT!\n")
        print(type(res_dict))
        print(res_dict)
        return_res = res_dict['results']

        # res = exract(return_res) # generate card string
        # PlayCard(res) # Play card

        print(return_res)
        if len(return_res) != 0:
            #print("Have result:")
            #print(return_res[0]['alternatives'])
            final_res = {}
            for item in return_res[0]['alternatives']:
                content = item['transcript']
                confidence = item['confidence']
                final_res[content] = confidence
            for key in final_res.keys():
                print("key is:" ,key)
                print("confidence is:", final_res[key])
            res_real = exract(final_res)
            print("result by zmh: ", res_real)
            PlayCard(res_real)
        else:
            print("No recognized result")
