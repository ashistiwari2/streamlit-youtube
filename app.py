import streamlit as st
import requests
from pytube import YouTube, StreamQuery

import base64
import os
from time import sleep

# https://www.youtube.com/watch?v=Ch5VhJzaoaI&t=90s

def clear_text():
    st.session_state["url"] = ""
    st.session_state["mime"] = ""
    st.session_state["quality"] = ""

def download_file(stream, fmt):
    """  """
    if fmt == 'audio':
        title = stream.title + ' audio.'+ stream_final.subtype
    else:
        title = stream.title + '.'+ stream_final.subtype

    stream.download(filename=title)
    
    if 'DESKTOP_SESSION' not in os.environ: #and os.environ('HOSTNAME')=='streamlit':
    
        with open(title, 'rb') as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            href = f'<a href="data:file/zip;base64,{b64}" download=\'{title}\'>\
                Here is your link \
            </a>'
            st.markdown(href, unsafe_allow_html=True)

        os.remove(title)


def can_access(url):
    """ check whether you can access the video """
    access = False
    if len(url) > 0:
        try:
            tube = YouTube(url)
            if tube.check_availability() is None:
                access=True
        except:
            
            st.warning('--Invalid link---')
            #st.experimental_rerun()
#             ph = st.empty()
#             N = 10
#             bar = st.progress(0)
#             for secs in range(0, N, 1):
#                 mm, ss = (N - secs) // 60, (N - secs) % 60
#                 bar.progress((secs + 1) * 10)
#                 ph.metric("Redirecting in...", f"{mm:02d}:{ss:02d}")
#                 sleep(1)
        

#                st.experimental_rerun()
  
        
    return access

def refine_format(fmt_type: str='audio') -> (str, bool):
    """ """
    if fmt_type == 'video (only)':
        fmt = 'video'
        progressive = False
    elif fmt_type == 'video + audio':
        fmt = 'video'
        progressive = True
    else:
        fmt = 'audio'
        progressive = False

    return fmt, progressive


st.set_page_config(page_title=" Youtube downloader", layout="wide")

# ====== SIDEBAR ======
with st.sidebar:
    st.title("Youtube download app")
    url = st.text_input("Insert your link here", key="url")

    fmt_type = st.selectbox("Choose format:", ['video (only)', 'audio (only)', 'video + audio'], key='fmt')

    fmt, progressive = refine_format(fmt_type)
#     with st.form(key='youtube', clear_on_submit=True):
        

  
#         submit_text = st.form_submit_button(label='Submit')


    if can_access(url) :

        tube = YouTube(url)

        streams_fmt = [t for t in tube.streams if t.type==fmt and t.is_progressive==progressive]

        mime_types = set([t.mime_type for t in streams_fmt])
        mime_type = st.selectbox("Mime types:", mime_types, key='mime')

        streams_mime = StreamQuery(streams_fmt).filter(mime_type=mime_type)

        # quality is average bitrate for audio and resolution for video
        if fmt=='audio':
            quality = set([t.abr for t in streams_mime])
            quality_type = st.selectbox('Choose average bitrate: ', quality, key='quality')
            stream_quality = StreamQuery(streams_mime).filter(abr=quality_type)
        elif fmt=='video':
            quality = set([t.resolution for t in streams_mime])
            quality_type = st.selectbox('Choose resolution: ', quality, key='quality')
            stream_quality = StreamQuery(streams_mime).filter(res=quality_type)

        # === Download block === #
        if stream_quality is not None:
            stream_final = stream_quality[0]
            if 'DESKTOP_SESSION' in os.environ:
                download = st.button("Download file", key='download')
            else:
                download = st.button("Get download link", key='download')

            if download:
                download_file(stream_final, fmt)
                st.success('Success download!')
                st.balloons()

        st.button("Clear all address boxes", on_click=clear_text)

        st.info(
            "This is an open source project and you are very welcome to contribute your "
            "comments, questions, resources and apps as "
            "[issues](https://github.com/maxmarkov/streamlit-youtube/issues) or "
            "[pull requests](https://github.com/maxmarkov/streamlit-youtube/pulls) "
            "to the [source code](https://github.com/maxmarkov/streamlit-youtube). "
        )



# ====== MAIN PAGE ======

if can_access(url):
    if streams_fmt is None:
        st.write(f"No {fmt_type} stream found")
    st.write(tube.thumbnail_url)
#     imgUrl = f"http://i.ytimg.com/vi/{link2[1]}/maxresdefault.jpg"
#     st.write(imgUrl)
    with st.spinner(f'Searching video on youtube for {url}.....'):
        
        st.video(url)
        col1, col2 = st.columns(2)
        sleep(8)
        with col1:
            st.image(tube.thumbnail_url, caption=tube.title, width=200, channels="RGB", output_format="auto")
            st.write("Title :{}".format(tube.title))
            st.write("Views :{}".format(tube.views))
            
        with col2:
            st.write("Duration:{}".format(tube.length))
            st.write("Descrption:{}".format(tube.description))
            st.write("Rating:{}".format(tube.rating))
     
 
