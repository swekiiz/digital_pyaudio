from pytube import YouTube  
  

SAVE_PATH = r"./video"
 
link=r"https://youtube.com/watch?v=6tKyuDLW97g"

print(link)

yt = None

try:  
    yt = YouTube(link)  
except:  
    print("Connection Error")
else:
    mp4files = yt.filter('mp4')  
    
    yt.set_filename('01')   

    d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution)  
    try:  
        d_video.download(SAVE_PATH)  
    except:  
        print("Some Error!")  
    print('Task Completed!')  