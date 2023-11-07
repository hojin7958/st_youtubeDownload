import streamlit as st
import yt_dlp
import streamlit_ext as ste
import os
import glob
import re
import emoji



st.header("유튜브 다운로드")


pattern = re.compile(f'[^ .,?!/@$%~％·∼()\x00-\x7Fㄱ-ㅣ가-힣]+')
url_pattern = re.compile(
    r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

def clean(x): 
    x = pattern.sub(' ', x)
    x = emoji.replace_emoji(x, replace='') #emoji 삭제
    x = url_pattern.sub('', x)
    x = x.strip()
    return x


def delete_files():
    for(path,dir,files)in os.walk(os.getcwd()) :#경로
        for filename in files :
            ext=os.path.splitext(filename)[-1]
            if ext=='.mp3':#확장자명
                print("%s\\%s"%(path,filename))
                os.remove("%s\\%s"%(path,filename))



if 'video_title' not in st.session_state:
    st.session_state['video_title'] = ''
    delete_files()

if 'file_name' not in st.session_state:
    st.session_state['file_name'] = ''


url = st.text_input("동영상 주소를 입력해주세요")

print(url)

# 테스트
# https://youtu.be/ToASX6axGuw?si=kpicX8QyYVExBjQF


def download_audio(link):
    global video_title

    with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio'}) as video1:
        info_dict = video1.extract_info(link, download = False)
        video_title = info_dict['title']
        st.session_state['video_title'] = video_title
        file_name = clean(video_title)
        st.session_state['file_name'] = file_name


    with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': f'{file_name}.mp3'}) as video:
        info_dict = video.extract_info(link, download = True)
        video_title = info_dict['title']
        st.session_state['video_title'] = video_title
        file_name = clean(video_title)
        st.session_state['file_name'] = file_name
        print(file_name)
        video.download(link)   
        print("Successfully Downloaded - see local folder on Google Colab")


downloaded = st.button('주소점검하기(1단계)', on_click=download_audio, args=[url])

if downloaded:
    st.write(st.session_state['video_title'])
    file_name = st.session_state['file_name']+'.mp3'

    with open(file_name, "rb") as file:
        btn = ste.download_button(
                label='다운로드',
                data=file,
                file_name=file_name,
                mime="audio/mp3"

            )
        