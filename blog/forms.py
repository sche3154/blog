from django import forms
from .models import Comment, Post, Category

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

        widgets = {
            'body': forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Leave a comment!"}) 
                }

class PostForm(forms.ModelForm):
    new_category = forms.CharField(max_length=100
                                   ,required=False
                                   , help_text="Enter a new category if it doesn't exist")
    class Meta:
        model = Post
        fields = ['title', 'body', 'categories', 'new_category']
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['categories'].queryset = Category.objects.all()
    #     if not Category.objects.exists():
    #         self.fields['categories'].widget.attrs['disabled'] = 'disabled'

    def clean(self):
        cleaned_data = super().clean()
        new_category_name = cleaned_data.get('new_category')
        category = cleaned_data.get('categories')

        if not category and not new_category_name:
            raise forms.ValidationError("You must select an existing category or enter a new one.")

        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            cleaned_data['categories'] = category

        return cleaned_data