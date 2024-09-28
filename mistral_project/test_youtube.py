from langchain.document_loaders import YoutubeLoader

# Chargez la transcription d'une vidéo YouTube
loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=W0Vd1NGrEEc&ab_channel=Cl%C3%A9mentViktorovitch", add_video_info=True)
document = loader.load()