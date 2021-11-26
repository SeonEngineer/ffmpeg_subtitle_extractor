# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 16:12:05 2021

@author: circi
"""
import os, sys, subprocess, shlex, re
from subprocess import call

#filePath = r'C:\ffmpeg\squid2.mkv'


dir = r'D:\queens'
findStr = 'Forced' #일반자막인경우 Forced, 화면해설인경우 SDH



for filename in os.listdir(dir):
    #print(filename)
    head, tail = os.path.splitext(filename)
    print('filename=', head)
    #print('fileExt=', tail)
    
    if not tail == '.mkv':
        continue
    
    filePath = os.path.join(dir,filename)
    
    cmnd = ['ffprobe', '-v','error','-of','csv', filePath,
            '-of','csv','-show_entries','stream=index:stream_tags=title,language','-select_streams','s']
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print(filePath)
    out, err =  p.communicate()
    #print("==========output==========")
    #print(out)
    strResult = str(out)
    
    strs = strResult.split('\\r\\n')
    
    korLines = []
    for str_line in strs:
        if 'ko' in str_line:
            korLines.append(str_line)
            
    #print(korLines)
    resultLen = len(korLines)
    
    
    streamID = -1
    
    
    if len(korLines) == 1:
        str_split = korLines[0].split(',')
        streamID = int(str_split[1])
        print('출력할 자막 track = ', str_split)
    elif len(korLines) > 1:
        
        resultStr = korLines[0]
        
        for str_line in korLines:
            print(str_line)
            if str_line.find(findStr) >= 0:
                #print(str_line, "적중")
                resultStr = str_line
                break
        print('출력할 자막 track = ', resultStr)
        str_split = resultStr.split(',')
        streamID = int(str_split[1])
    
    
    if streamID >= 0:
        outputFilePath = os.path.join(dir,head) + '.srt'
        #print("=자막파일을 출력합니다=")
        #print(outputFilePath)
        
        
        idxStr = '0:%d' % (streamID)
        cmnd = ['ffmpeg', '-y', '-i', filePath,
            '-map',idxStr,outputFilePath]
        #print(cmnd)
        
        p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print(filePath)
        
        out, err =  p.communicate()
        
        print('자막 출력 완료: ', head)
        
                    
    
    
    
    
    
    
    
    














