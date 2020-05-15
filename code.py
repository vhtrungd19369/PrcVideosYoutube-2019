from googlesearch import search_videos
from urllib.request import urlopen
from urllib.parse import urlencode
from os.path import expanduser
from pytube import YouTube
import speech_recognition as sr
import platform as pf
import pydub as pyd
import numpy as np
import glob as gl
import subprocess
import os
import re

"""
"""
# Ham co chuc nang tao folder de luu tap tin 
def create_folder():	
	try:
		# Ktra OS dang su dung
		if pf.system()=="Linux":
                        print("You are using Linux, great!")
                        folder_name = str(input("Enter the folder name to save the files: "))				
			# "~" co nghia la lay duong dan /home/$USER + them ten thu muc muon tao
                        fn_path = os.path.join(expanduser("~"), folder_name)
			# Ktra duong dan co ton tai ko, neu khong ton tai thi tao thu muc, neu ton tai thi khong tao thu muc
                        check_path = os.path.exists(fn_path)
                        if check_path is False:
                                os.mkdir(fn_path)
                        print("The path to save the files:",fn_path)
		else:
			print("Please use Linux in the future!")
			folder_name = input("Enter the folder name to save the files: ")
			fn_path = os.path.join(expanduser("~"), folder_name)
			check_path = os.path.exists(fn_path)
			if check_path is False:
				os.mkdir(fn_path)
			print("The path to save the files:",fn_path)
		return fn_path
	except:
		print("N/A")

# Ham doc vao ten cua mot file va tao thu muc voi ten file nhan duoc
def mv_files(fol_name, fi_name, ext):
	# Ham co chuc nang tao thu muc, di chuyen cac file vao thu muc vua tao
	try:
		# Lay ten cua file bo di phan mo rong ".mp4"
		folder_name = fi_name[:-4]
		os.mkdir(folder_name)
		# Lay ten file them phan mo rong .ext(txt, mp3, ...)
		txt_file = os.path.splitext(fi_name)[0]+ext
		# Them ki tu "_" vao khoang trang trong ten file
		src_textension = txt_file.replace(" ","_")
		# Them ki tu "_" vao khoang trang trong ten thu muc
		dst = folder_name.replace(" ","_")
		# Them ki tu "_" vao ten khoang trang ten file .txt
		os.rename(txt_file, src_textension)
		# Doi ten thu muc (Them "_" vao ten thu muc)
		os.rename(folder_name, dst)
		# Di chuyen file "src_textension.txt" vao thu muc "dst" 
		subprocess.call("mv %s %s" %(src_textension, dst), shell=True)
		try:
			# Lay duong dan thu muc chua file *.wav
			f_path = fol_name+"/*.wav"
			# Liet ke tat ca cac file co duoi .wav
			lf_wav = gl.glob(f_path)
			for fwav in lf_wav:
				src_wexten = fwav.replace(" ","_")
				os.rename(fwav, src_wexten)
				subprocess.call("mv %s %s" %(src_wexten, dst), shell=True)
		except:
			print("Error when move *.wav to ",dst)
		return dst
	except:
		print("Error when moving file to folder!")

def mp4_to_audio(folder=None):
	# Neu thu muc ko duoc truyen vao thi tao thu muc moi
	if folder is None:
		folder = create_folder()
	f_path = os.path.join(expanduser('~'), folder+'/*.mp4')
	f_list = gl.glob(f_path)
	# Neu danh sach file rong thi thong bao loi
	if f_list==[]:
		print("----------------------------------")
		print("Could't find the *.mp4 files")
		print("----------------------------------")
	total_flist = len(f_list)
	if total_flist == 1:
		print("Num of converted video:", total_flist)
	else:
		print("Num of converted videos:", total_flist)
	for each_file in f_list:
		#print(">>",each_file)
		# Doi phan duoi mo rong cua file thanh .wav
		wav_file = os.path.splitext(each_file)[0]+".wav"
		# Neu duoi cua file la .mp4 thi tien hanh chuyen doi .mp4 thanh .wav
		if each_file.endswith(".mp4"):	
			to_wav = pyd.AudioSegment.from_file(each_file)
			to_wav.export(wav_file, format="wav")
		
		#print("Convert done >>>",wav_file)
	if total_flist == 1:
		print("==> Successfully converted an audio file <==")
		print("--------------------------------------------------------------------------------")
	else:
		print("==> Successfully converted",total_flist,"audio files <==")
		print("--------------------------------------------------------------------------------")
# Ham chuyen doi file .mp3 thanh .wav, cau lenh tuong tu nhu ham tren
def mp3_to_audio(folder=None):
	if folder is None:
		folder = create_folder()
	f_path = os.path.join(expanduser('~'), folder+'/*.mp3')
	f_list = gl.glob(f_path)
	if f_list==[]:
		print("----------------------------------")
		print("Could't find the *.mp3 files")
		print("----------------------------------")
	total_flist = len(f_list)
	if total_flist == 1:
		print("Num of converted video:", total_flist)
	else:
		print("Num of converted videos:", total_flist)
	for each_file in f_list:
		print(">>",each_file)
		wav_file = os.path.splitext(each_file)[0]+".wav"
		if each_file.endswith(".mp3"):	
			to_wav = pyd.AudioSegment.from_mp3(each_file)
			to_wav.export(wav_file, format="wav")
		print("--------------------------------------------------------------------------------")
		print("Done >>>",wav_file)
		print("--------------------------------------------------------------------------------")
		#move_mv_files(wav_file, ".wav")
	if total_flist == 1:
		print("==> Successfully converted an audio file <==")

def all_to_audio(folder=None):
	# The directory contains the default operating system video files
	if folder is None:
		folder = create_folder()
	f_path = os.path.join(expanduser('~'), folder+'/*.mp*')
	f_list = gl.glob(f_path)
	if f_list==[]:
		print("----------------------------------")
		print("Could't find the *.mp3 or *.wav files")
		print("----------------------------------")
	total_flist = len(f_list)
	if total_flist == 1:
		print("Num of converted video:", total_flist)
	else:
		print("Num of converted videos:", total_flist)
		
	for each_file in f_list:
		print(">>",each_file)
		wav_file = os.path.splitext(each_file)[0]+".wav"
		if each_file.endswith(".mp4"):	
			to_wav = pyd.AudioSegment.from_file(each_file)
			to_wav.export(wav_file, format="wav")
		elif each_file.endswith(".mp3"):
			to_wav = pyd.AudioSegment.from_mp3(each_file)
			to_wav.export(wav_file, format="wav")
		else:
			print("No file support!")
		print("--------------------------------------------------------------------------------")
		print("Done >>>",wav_file)
		print("--------------------------------------------------------------------------------")
	if total_flist == 1:
		print("==> Successfully converted an audio file <==")
	else:
		print("==> Successfully converted",total_flist,"audio files <==")
# Ham chuyen doi .wav thanh van ban dang .txt
def speech_to_text(path=None):
	try:
		# Neu duong dan rong thi yeu cau nguoi dung nhap duong dan
		print("Path:",path)
		if path is None:
			path = create_folder()
		f_path = path+"/*.wav"
		lf_wav = gl.glob(f_path)
		if lf_wav == []:
			print("----------------------------------")
			print("Could't find the *.wav file")
			print("----------------------------------")
		r = sr.Recognizer()
		for AUDIO_FILE in lf_wav:
			print("Translate an audio file:")
			print(AUDIO_FILE)
			with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
				txt_file = os.path.splitext(AUDIO_FILE)[0]+".txt"
			try:
				# recognize speech using Sphinx
				text = r.recognize_sphinx(audio)
				with open(txt_file, "w") as f:
					f.write(text)
				mv_files(f_path, txt_file,".txt")
				print("Done >>>",txt_file)
				print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
			except sr.UnknownValueError:
				print("Sphinx could not understand audio!")
			except sr.RequestError as e:
				print("Sphinx error; {0}".format(e))
	except:
		print("Error N/A")

def down_video():
	print("<Enter 'menu' to return to the main menu>")
	print("<Enter 'exit' to exit the program>")
	search_keyword = input('Search videos on Youtube: ')
	while True:
		try:
			check_keyword = str(search_keyword)
			if check_keyword=='exit':
				break
			elif check_keyword=='menu':
				main()
				break
			number_of_videos = input('Number of videos: ')
			if number_of_videos=='exit':
				break
			elif number_of_videos=='menu':
				main()
				break
			check_number = int(number_of_videos)
			if check_number <= 0:
				print("Please enter a number > 0")
			else:
				# Get the home directory of the operating system as the path to save the files:
				output_path = create_folder()
				print('---------------------------------------------------------------')
				try:
					# Thuc hien truy van den may chu Youtube de nhan ve ID video
					query_youtube = urlencode({"search_query": check_keyword})
					content = urlopen("http://www.youtube.com/results?" + query_youtube)
					results = re.findall(r'href=\"\/watch\?v=(.{11})', content.read().decode())
					results = list(dict.fromkeys(results))
					for i in range(0, check_number):
						url = "https://www.youtube.com/watch?v="+results[i]
						print("Downloading....")
						print(url)
						YouTube(url).streams.filter(subtype='mp4', progressive=True).first().download(output_path)
						print('---------------------------------------------------------------')
						
					else:	
						if check_number is 1:
							print ('>>> Download',check_number,'video completed!')
						else:
							print('>>> Download',check_number,'videos completed!')
						#print('>>> Videos save to path: ==>',output_path,'<==')
						print('---------------------------------------------------------------')
					break
				except Exception as e:
					print("Download videos error!", +e)
		except ValueError:
			print(">> Value must be a number, try again please!")

def down_video_transcribe():
	print("<Enter 'menu' to return to the main menu>")	
	print("<Enter 'exit' to exit the program>")
	search_keyword = input('Search videos on Youtube: ')
	while True:
		try:
			check_keyword = str(search_keyword)
			if check_keyword=='exit':
				break
			elif check_keyword=='menu':
				main()
				break
			number_of_videos = input('Number of videos: ')
			if number_of_videos=='exit':
				break
			elif number_of_videos=='menu':
				main()
				break
			check_number = int(number_of_videos)
			if check_number <= 0:
				print("Please enter a number > 0")
			else:
				# Get the home directory of the operating system as the path to save the files:
				output_path = create_folder()
				print('---------------------------------------------------------------')
				# Thuc hien truy van den may chu Youtube de nhan ve ID video
				query_youtube = urlencode({"search_query": check_keyword})
				content = urlopen("http://www.youtube.com/results?" + query_youtube)
				results = re.findall(r'href=\"\/watch\?v=(.{11})', content.read().decode())
				results = list(dict.fromkeys(results))
				for i in range(0, check_number):
					url = "https://www.youtube.com/watch?v="+results[i]
					print("Downloading....")
					print(url)
					YouTube(url).streams.filter(subtype='mp4', progressive=True).first().download(output_path)
					print('---------------------------------------------------------------')
				else:	
					if check_number is 1:
						print ('>>> Download',check_number,'video completed!')
					else:
						print('>>> Download',check_number,'videos completed!')
					print('>>> Videos save to path: ==>',output_path,'<==')
					print('---------------------------------------------------------------')
				try:
					mp4_to_audio(output_path)
					speech_to_text(output_path)
					files = output_path+"/*.mp4"
					lst_videos = gl.glob(files)
					for i in lst_videos:
						folder_name = i[:-4]
						folder_name = folder_name.replace(" ","_")
						check_dst_video = os.path.exists(folder_name)		
						if check_dst_video is False:
							os.mkdir(folder_name)
						scene_detect(output_path, folder_name)
				except Exception as ex:
					print(">>> Error:",ex)
				break
		except ValueError as value:
			print(">> Value must be a number, try again please!")

def choice_convert():
	menuItems = np.array(["[1] Convert mp3 => wav file.", 
			"[2] Convert mp4 => wav file.", 
			"[3] Convert mp4, mp3 => wav file.", 
			"[4] Return to the main menu.", 
			"[5] Exit."])
	print("*******************************************************")
	for i in menuItems:
		print(i)
	print("*******************************************************")
	while True:
		try:
			y_choice = int(input("[Your_choice][Covert video] > "))
			if y_choice==1:
				mp3_to_audio()
			elif y_choice==2:
				mp4_to_audio()
			elif y_choice==3:
				all_to_audio()
			elif y_choice==4:
				main()
				break
			elif y_choice==5:
				break
			else:
				print(">> No choice found!")
		except ValueError:
			print(">> Value must be a number, try again please!")

# Ham co chuc nang cat video thanh cac canh
def scene_detect(src_file=None, dst_file=None):
	
	while True:
		try:
			src_video = ""
			dst_video = ""
			# Neu ko co tham so dau vao thi cho nguoi dung nhap vao ten thu muc chua file .mp4
			if dst_file is None:
				print("<Enter 'menu' to return to the main menu>")	
				print("<Enter 'exit' to exit the program>")
				print("<Only enter folder name!>")
				"""src_video = str(input("Input video: "))
				if src_video=="exit":
					break
				elif src_video=="menu":
					main()
					break"""
				dst_video = str(input("Ouput video: "))
				if dst_video=="exit":
					break
				elif dst_video=="menu":
					main()
					break
			else:
				src_video = str(src_file)
				dst_video = str(dst_file)
			
			src_video_lst = os.path.join(expanduser('~'), src_video+'/*.mp4')
			dst_video_lst = os.path.join(expanduser('~'), dst_video)
			# Liet ke danh sach file .mp4
			lst_video = gl.glob(src_video_lst)
			#print (lst_video)
			check_dst_video = os.path.exists(dst_video_lst)
			# Neu duong dan thu muc ko ton tai thi tao thu muc 
			if check_dst_video is False:
				os.mkdir(dst_video_lst)
			# Neu danh sach file .mp4 la rong thi bao loi
			if lst_video==[]:
				print("----------------------------------")
				print("Could't find the *.mp4 files.")
				print("----------------------------------")
			for i in lst_video:
				# Them dau \" vao truoc va sau ten file
				i = "\""+i+"\""	
				subprocess.call("scenedetect -i %s detect-content list-scenes -o %s split-video -o %s" %(i, dst_video_lst, dst_video_lst), shell=True)
			break
		except Exception as e:
			print("Error when cutting video"+e)


def main():
	menuItems_func = np.array(["[0] Download Video, Transcribe and Scene Detect.",
				"[1] Download Video on Youtube.", 
				"[2] Scene Detect Video.", 
				"[3] Covert Video.",
				"[4] Exit."])
	print("############### Hello world! ##################")
	for i in menuItems_func:
		print(i)
	print("###############################################")	
	while True:
		try:
			f_choice = int(input("[Your_choice] > "))
			if f_choice==0:
				down_video_transcribe()
				break
			elif f_choice==1:
				down_video()
				break
			elif f_choice==2:
				scene_detect()
				break
			elif f_choice==3:
				choice_convert()
				break
			elif f_choice==4:
				break
			else:
				print(">> No choice found!")
		except ValueError:
			print(">> Value must be a number, try again please!")

if __name__ == '__main__':
	print("""
 _   _ _              _                          _____ _   _ _______ _______ 
| \ | (_)            | |                        / ____| \ | |__   __|__   __|
|  \| |_  ___ _ __   | |    _   _  __ _ _ __   | |    |  \| |  | |     | |   
| . ` | |/ _ \ '_ \  | |   | | | |/ _` | '_ \  | |    | . ` |  | |     | |   
| |\  | |  __/ | | | | |___| |_| | (_| | | | | | |____| |\  |  | |     | |   
|_| \_|_|\___|_| |_| |______\__,_|\__,_|_| |_|  \_____|_| \_|  |_|     |_|   
                                                                            
	""")
	main()
