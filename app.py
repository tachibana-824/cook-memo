from googleapiclient.discovery import build
import streamlit as st


# with open('secret.json') as f:
#     secret = json.load(f)

def getIdListFromPlaylist(id,youtube,keyword):

    nextPageToken = 'start'
    response = []

    while(nextPageToken is not None):

        if nextPageToken == 'start':
            search_response = youtube.playlistItems().list(
            part= 'snippet',
            playlistId=id,
            maxResults = 50,
            ).execute()
        else:
            search_response = youtube.playlistItems().list(
            part= 'snippet',
            playlistId=id,
            maxResults = 50,
            pageToken = nextPageToken
            ).execute()

        if 'nextPageToken' in search_response:
            nextPageToken = search_response['nextPageToken']
        else:
            nextPageToken = None
        
        for item in search_response['items']:
            if keyword in item['snippet']['description']:
                response.append(item['snippet']['resourceId']['videoId'])
            
    return response

DEVELOPER_KEY = "AIzaSyBnaaFyojdo-6_Fbhu0k69LlJMK5YG0my4"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)



st.title('cook memo')

st.sidebar.write('キーワード入力')
keyword = st.sidebar.text_input('キーワードを入力してください','例 :にんじん')
st.sidebar.write('再生リスト入力')
id = st.sidebar.text_input('再生リストidを入力してください',)


st.write('キーワード :',keyword)

st.write('再生リスト :',id)



if st.button('動画表示'):
    video_ids = getIdListFromPlaylist(id=id,youtube=youtube,keyword=keyword)
    for video_id in video_ids:
        
        url = f'https://www.youtube.com/watch?v={video_id}'
        video_field = st.empty()

        if len(video_id)>0:
            try:
                video_field.video(url)
            except:
                st.error('リンクが間違っています。')

