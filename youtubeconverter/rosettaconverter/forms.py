from django import forms

class YouTubeForm(forms.Form):
    youtube_url = forms.URLField(label='YouTube URL', widget=forms.URLInput(attrs={'placeholder': 'Enter YouTube URL'}))
