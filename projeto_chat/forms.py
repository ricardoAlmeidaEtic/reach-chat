from django import forms

class MessageForm(forms.Form):
    your_message = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), label="Your Message", max_length=100)
    your_image = forms.FileField(required=False)