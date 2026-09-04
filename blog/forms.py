from django import forms
from .models import Article, Tag

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title","body","tags","is_pinned"
        ]

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        name = name.lower()

        if not (name.isascii() and name.isalnum()):
            raise forms.ValidationError(
                "タグ名は半角英数字のみ使用できます。"
            )

        if Tag.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(
                "同じタグがすでに存在します。"
            )

        return name