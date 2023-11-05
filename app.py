import streamlit as st
import yt_dlp
import streamlit_ext as ste


st.header("유튜브 다운로드")

if 'video_title' not in st.session_state:
    st.session_state['video_title'] = ''


url = st.text_input("주소를 입력해주세요")

print(url)

def download_audio(link):
  global video_title
  with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '%(title)s.mp3'}) as video:
    info_dict = video.extract_info(link, download = True)
    video_title = info_dict['title']
    print(video_title)
    video.download(link)   
    print("Successfully Downloaded - see local folder on Google Colab")
    st.session_state['video_title'] = video_title



downloaded = st.button('주소점검하기(1단계)', on_click=download_audio, args=[url])

if downloaded:
    st.write(st.session_state['video_title'])
    file_name = st.session_state['video_title'] + ".mp3"

    with open(file_name, "rb") as file:
        btn = ste.download_button(
                label='다운로드',
                data=file,
                file_name=file_name,
                mime="audio/mp3",
            )

