import os, random
import shutil
import math
import datetime
import matplotlib.pyplot as plt
import cv2
import glob
from os import startfile
import subprocess
import shutil
from shutil import copyfile
import codecs

def Clear():
	subprocess.call('cls',shell=True)

class WaterMark:
	resize = 0
	maintainRatio = 0
	scaleWH = "n"
	scalePercent = 15


#Eventually I will add all the methods into the console menu
#All the methods are accessed below by using the State variable
#Right now the app is locked in the menu
#Set the state here if you want to use the app

State = 0

#Just make sure to look through the code and know what's going to happen
#Like preparing folders with your input videos and folders for your gifs/pictures


while True: #Console menu WORK IN PROGRESS DO NOT USE SKIP OVER THIS
	Clear()  
	print('Welcome to MassVod, a very convenient tool for mass producing videos')
	print('Features: ')
	print('   1   Watermark videos ')
	print('   2   Split videos into scenes ')
	print('   3   Gather all clips into one folder ')
	print('   4   Add pictures/gifs to clips ')
	print('   5   Export Videos ')
	print('   6   Do parts/everything above in order ')
	print('   7   Recompile video format ')
	print('   0   Exit ')
	print('What you would like to do?')
	x = input()
	if x == "0" or x == "exit":
		break
	if x == '1':
		Clear()
		while True:
			print('You have selected Watermark videos')
			print('Type b to go back')
			waterMark = WaterMark()
			print('Would you like to resize the watermark? y/n')
			x = input()
			if x == 'b':
				break
			if x == 'y':
				waterMark.resize = 1
				print('Would you like to maintain the watermark aspect ratio? y/n')
				x = input()
				if x == 'b':
					break
				if x == "y":
					waterMark.maintainRatio = 1
					print("Resize the watermark relative to the width or the height of the source video? w/h")
					x = input()
					if x == 'b':
						break
					if x == "w":
						waterMark.scaleWH = "w"
						print("What percentage would you like the watermark width to be relative to the source video? ex. 20%")
						x = input()
						if x == 'b':
							break
						if "%" in x:
							x.replace('%','')
						waterMark.scalePercent = x
					if x == "h":
						waterMark.scaleWH = "h"
						print("What percentage would you like the watermark height to be relative to the source video? ex. 15%")
						x = input()
						if x == 'b':
							break
						if "%" in x:
							x.replace('%','')
			print('Would you like to preview the watermark? y/n')
			x = input()
			if x == "y":
				print("Snapshot stored in ")
			print('Are you ready to export? y/n')
			x = input()
				

while State == 2: #Watermark videos at the bottom left corner of screen UPDATE TO DO ANY CORNER / MIDDLE  
	
	Video = glob.glob(os.getcwd() + "/Videos/*.mp4")
	cur = glob.glob(os.getcwd() + "/Watermarked/*.mp4")
	number = 0		
	for name in cur:
		number += 1
	for vid in Video:
		a = subprocess.Popen('ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 ' + vid, stdout=subprocess.PIPE, shell=True)
		(output, err) = a.communicate()
		
		#TODO Scale watermark based on user input
		subprocess.call('ffmpeg -i ' + vid + ' -i ' + os.getcwd() + '\Logos\Watermark.png -filter_complex "overlay=0:0" ' + os.getcwd() + '\Watermarked/' + 'Video'  + str(number) + '.mp4')
		number += 1
		
	State = 32352523523  #Set to random state so it doesn't continue unless you set it to 3 
while State == 3: #Split videos
	
	WaterMarked = glob.glob(os.getcwd() + "\Watermarked/*.mp4")
	
	pNum = len(glob.glob(os.getcwd() + "\Splitted\Video/*"))
	for vid in WaterMarked:
		#Fix this later
		os.mkdir(os.getcwd() + "\Splitted\Video/" + str(pNum) + '/')
		subprocess.call('scenedetect -d 12 -i ' + vid  + ' -o ' + os.getcwd() + '\Splitted\Video/' + str(pNum) + '/ detect-content split-video')
		pNum += 1

	State = 4421323
while State == 4: #Collect clips into one folder for each category
	
	splitVid = glob.glob(os.getcwd() + '\Splitted\Video/*') #get all videos splitted
	
	if not os.path.exists(os.getcwd() + '\FinalVideos\Temp/'):
		os.mkdir(os.getcwd() + '\FinalVideos\Temp/')
	for folder in splitVid:  #For each folder 
		vids = glob.glob(folder + '/*.mp4')#grab all clips
		for vid in vids:
			if not os.path.exists(os.getcwd() + '\FinalVideos\Temp/' + os.path.basename(vid)):
				shutil.move(vid, os.getcwd() + '\FinalVideos\Temp/') #move clips to one folder
	State = 1124124214
while State == 5: #randomly collect clips into video folders 10 minutes long
	VidNumber = 1
	inVid = glob.glob(os.getcwd() + "\FinalVideos\*")
	for obj in inVid:
		print(obj)
		if 'Temp' not in obj:
			VidNumber += 1 
	newVidTime = 0;
	while len(glob.glob(os.getcwd() + "\FinalVideos\Temp/*")) > 0:
		vid = random.choice(glob.glob(os.getcwd() + "\FinalVideos\Temp/*"))
		a = subprocess.Popen('ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 ' + vid, stdout=subprocess.PIPE, shell=True)
		(output, err) = a.communicate()
		out = str(output).strip("'")
		out = out.replace("r", "")
		out = out.replace("n", "")
		out = out.replace("b", "")
		out = out.replace("'", "")
		out = out[:-2]
		print(float(out)) #magically get video length
		newVidTime += float(out)
		if not os.path.exists(os.getcwd() + '\FinalVideos/' + 'Video' + str(VidNumber)):
			os.mkdir(os.getcwd() + '\FinalVideos/' + 'Video' + str(VidNumber) + '/')
			os.mkdir(os.getcwd() + '\FinalVideos/' + 'Video' + str(VidNumber) + '/RAW/')
		shutil.move(vid, os.getcwd() + '\FinalVideos/' + 'Video' + str(VidNumber) + '/RAW/')
		
		if newVidTime / 60 > 10: #INSERT USER INPUT FOR VIDEO LENGTH HERE <---------------------------------
			VidNumber += 1
			newVidTime = 0
	
	State = 325434534534534
while State == 6: #Edit 25% clips to have a funny picture in the bottom left corner ALSO SCALE VIDEO AND GIF MAGICALLY
	videos = glob.glob(os.getcwd() + '\FinalVideos/' + '/*')
	for video in videos:
		if "Finished" not in video:
			if os.path.exists(video + "/AddedGifs/"):
				print(video)
				shutil.rmtree(video + "/AddedGifs/")
				if os.path.exists(video + "/OldClips/"):
					oldv = glob.glob(video + "/OldClips/*.mp4")
					for old in oldv:
						shutil.move(old, video + "/RAW/")
					os.rmdir(video + "/OldClips/")
			clips = glob.glob(video + "/RAW/*")
			gifs = glob.glob(os.getcwd() + "\Memes\General/*.gif") #Get the gifs
			amount = len(clips) / 4   # SET GIF DISTRIBUTION AMOUNT BY USER <-------------
			c = 0
			while c < amount:
				clip = random.choice(clips)
				clips.remove(clip)
				gif = random.choice(gifs)
				gifs.remove(gif)
			
				if not os.path.exists(video + '/AddedGifs/'):
					os.mkdir(video + '/AddedGifs/')
				#Check resolution of video and gif
				a = subprocess.Popen('ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 ' + clip, stdout=subprocess.PIPE, shell=True)
				(output, err) = a.communicate()
				out = str(output).strip("'")
				out = out.replace("r", "")
				out = out.replace("n", "")
				out = out.replace("b", "")
				out = out.replace("'", "")
				out = out[:-2]
				clipRes = out.split('x')  #Magically filter the output to get the video resolution
				
				a = subprocess.Popen('ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 ' + gif, stdout=subprocess.PIPE, shell=True)
				(output, err) = a.communicate()
				out = str(output).strip("'")
				out = out.replace("r", "")
				out = out.replace("n", "")
				out = out.replace("b", "")
				out = out.replace("'", "")
				out = out[:-2]
				gifRes = out.split('x')  #Magically filter the output to get the gif resolution
				
				SCALE = 0
				if int(gifRes[0]) >= int(clipRes[0]) / 4:  #SCALE AMOUNT SET BY USER <------------------------------
					SCALE = 1
				if int(gifRes[1]) >= int(clipRes[1]) / 4:  #HOZ/VER CHOICE SET BY USER <------------------------------
					SCALE = 1
				
				finished = 0
				factor = 1
				while finished == 0:
					if int(gifRes[0]) / factor < int(clipRes[0]) / 4: #<-------------------------------
						finished = 1
					if int(gifRes[1]) / factor < int(clipRes[1]) / 4:
						finished = 1
					factor += .2 #decrease this to increase scale accuracy 
					
				finalRes = [int(int(gifRes[0]) / factor), int(int(gifRes[1]) / factor)]
				
				if SCALE == 1:  #Export video with added gif with scaling
					subprocess.call('ffmpeg -i ' + clip + ' -ignore_loop 0 -i ' + gif + ' -filter_complex "[1:v]scale=' + str(finalRes[0]) + ':' + str(finalRes[1]) + ' [ovrl],[0:v][ovrl]overlay=0:main_h-overlay_h:shortest=1" ' +  video + '/AddedGifs/' + str(c) + '.mp4 ')
				else: #no scaling
					subprocess.call('ffmpeg -i ' + clip + ' -ignore_loop 0 -i ' + gif + ' -filter_complex "overlay=x=0:y=(main_h-overlay_h):shortest=1" ' +  video + '/AddedGifs/' + str(c) + '.mp4 ')
				
				if not os.path.exists(video + '/OldClips/'):
					os.mkdir(video + '/OldClips/')
				shutil.move(clip, video + '/OldClips/')
				c += 1
	
	State = 7
while State == 7: #Export Videos
	intro = os.getcwd() + "/INTRO.mp4"
	outro = os.getcwd() + "/OUTRO.mp4"  #SET USER INTRO OUTRO BY USER CHOICE <---------------------------------
	useIntro = 0
	useOutro = 0
	
	isVideo = 1  #This is to check if the source material is video or audio, different export method is used FIX SO IT CAN USE BOTH

	videos = glob.glob(os.getcwd() + '\FinalVideos/*')
	for video in videos:
		if "Finished" not in video:
			#gifs = []   SET OPTION NOT TO USE GIFS BY USER <--------------------------------------
			gifs = glob.glob(video + "/AddedGifs/*")
			raw = glob.glob(video + "/RAW/*")
			total = gifs + raw
			Pictures = glob.glob(video + '\Pictures/*')  #SET OPTION TO USE PICTURES <-----------------------
				
			n = 1
			name = "Final"
			fCom = "ffmpeg" #The first part of the huge ffmpeg command
			filterPart1 = ""  #The second part of the huge ffmpeg command
			filterPart2 = ""  #The third part of the huge ffmpeg command lol
			
			if useIntro == 1:  #LET USER DETERMINE OUTPUT RESOLUTION <---------------------------------------------
				fCom += " -i " + intro
				filterPart1 += "[" + str(n - 1) + ":v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v" + str(n - 1) + "];"
				filterPart2 += "[v" + str(n - 1) + "] [" + str(n - 1) + ":a]"
				n += 1
			while len(total) > 0:
				vid = random.choice(total) #randomly choose among all the clips
				total.remove(vid)
				fCom += " -i " + vid  
				if isVideo == 1: #Source is video
					filterPart1 += "[" + str(n - 1) + ":v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v" + str(n - 1) + "];"
					filterPart2 += "[v" + str(n - 1) + "] [" + str(n - 1) + ":a]"
					n += 1
				else:
					filterPart1 += "[" + str(n - 1) + ":0]"
					n += 1
			if useOutro == 1:
				fCom += " -i " + outro
				filterPart1 += "[" + str(n - 1) + ":v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v" + str(n - 1) + "];"
				filterPart2 += "[v" + str(n - 1) + "] [" + str(n - 1) + ":a]"
				
			n -= 1 #Check this
				
			fCom += ' -filter_complex "' + filterPart1 + filterPart2 + "concat=n=" + str(n) #combining the huge command together
			
			if isVideo == 1: #More filter stuff
				fCom +=  ':v=1:a=1[outv][outa]"'
				fCom += ' -map [outv] -map [outa]'
				fCom += ' -vcodec libx264 -crf 27 -vsync 2 -preset ultrafast'
			else:
				fCom +=  ':v=0:a=1[out]"'
				fCom += " -map [out] "
				fCom += ' -preset ultrafast'

			fCom += ' ' + video + "/" + name + ".mp4" #Finalizing the command
			#1280x720
			if os.path.exists(video + "/" + name + ".mov"): #Delete any duplicates
				os.remove(video + "/" + name + ".mov")
			if os.path.exists(video + "/" + name + ".mkv"):
				os.remove(video + "/" + name + ".mkv")
			if os.path.exists(video + "/" + name + ".mp4"):
				os.remove(video + "/" + name + ".mp4")
			if os.path.exists(video + "/" + name + ".ts"):
				os.remove(video + "/" + name + ".ts")
				
			subprocess.call(fCom) #Use the command
			
	State = 8
while State == 8: #Put 'Finished' in video folder name
	videos = glob.glob(os.getcwd() + "\FinalVideos/*")
	for video in videos:
		if "Finished" not in video:
			shutil.move(video, video + "Finished")
	State = 91424214
	
