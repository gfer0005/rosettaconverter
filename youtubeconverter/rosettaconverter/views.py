import os
from django.shortcuts import render
from yt_dlp import YoutubeDL
from moviepy.editor import AudioFileClip
from .forms import YouTubeForm
from django.http import FileResponse

def convert_to_mp3(request):
    if request.method == 'POST':
        form = YouTubeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['youtube_url']
            try:
                # Télécharger la vidéo en audio uniquement
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': '%(title)s.%(ext)s',  # Enregistre avec le nom de la vidéo
                }

                with YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    mp3_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')

                # Télécharger le fichier MP3
                response = FileResponse(open(mp3_file, 'rb'), as_attachment=True)
                response['Content-Disposition'] = f'attachment; filename="{info_dict["title"]}.mp3"'

                # Optionnel : Supprimer le fichier MP3 après téléchargement
                os.remove(mp3_file)

                return response
            except Exception as e:
                return render(request, 'converter/index.html', {'form': form, 'error': str(e)})
    else:
        form = YouTubeForm()

    return render(request, 'converter/index.html', {'form': form})
