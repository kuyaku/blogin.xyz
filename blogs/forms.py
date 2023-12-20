from django import forms
from .models import Post, Blogger
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PostCreateForm(forms.ModelForm):
    category_names = forms.CharField(max_length = 300, required=True, widget=forms.TextInput(attrs={'placeholder': 'Comma separated categories'}))
    tag_names = forms.CharField(max_length = 300, required=False, widget=forms.TextInput(attrs={'placeholder': 'Comma separated tags'}))
    title = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'placeholder': 'Heading'}))
    sub_title = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'placeholder': 'Sub heading'}))
    content = forms.CharField(widget=CKEditorUploadingWidget(attrs={'name': 'stylingPallete', 'config': 'basic'}))

    class Meta:
        model = Post
        fields = ['content', 'title', 'sub_title', 'category_names', 'tags']
        # fields = '__all__'
    
    class Media:
        js = ('ckeditor/ckeditor.js', 'js/ckeditor_config.js')


    def clean_category_names(self):
        category_names = self.cleaned_data.get('category_names')
        if category_names:
            return [name.strip().upper() for name in category_names.split(',') if name != '']
        return []
    
    def clean_tag_names(self):
        tag_names = self.cleaned_data.get('tag_names')
        if tag_names:
            return [name.strip().upper() for name in tag_names.split(',') if name != '']
        return []
        

class PostUpdateForm(forms.ModelForm):
    category_names = forms.CharField(max_length = 300, required=False, widget=forms.TextInput(attrs={'placeholder': 'Comma separated categories'}))
    tag_names = forms.CharField(max_length = 300, required=False, widget=forms.TextInput(attrs={'placeholder': 'Comma separated tags'}))
    title = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'placeholder': 'Heading'}))
    sub_title = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'placeholder': 'Sub heading'}))
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['content', 'title', 'sub_title', 'image', 'category_names', 'tags']
        # fields = '__all__'


    def clean_category_names(self):
        category_names = self.cleaned_data.get('category_names')
        if category_names:
            return [name.strip().upper() for name in category_names.split(',') if name != '']
        return []
    
    def clean_tag_names(self):
        tag_names = self.cleaned_data.get('tag_names')
        if tag_names:
            return [name.strip().upper() for name in tag_names.split(',') if name != '']
        return []

class BloggerUpdateForm(forms.ModelForm):
    class Meta:
        model = Blogger
        fields = ['username', 'first_name', 'last_name', 'bio', 'user_interests']
    
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    user_interests = forms.CharField(max_length=300, required=False, widget=forms.TextInput(attrs={'placeholder': 'Comma separated interests'}))

    def clean_user_interests(self):
        interests_name = self.cleaned_data.get('user_interests')
        if interests_name:
            return [name.strip().upper() for name in interests_name.split(',') if name != '']
        return []
