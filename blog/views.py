from django.shortcuts import render,redirect
from .models import Article, Tag
from .forms import ArticleForm

def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = ArticleForm()

    context = {
        "form": form,
    }

    return render(request, "blog/article_form.html", context)

def dashboard(request):
    articles = Article.objects.all()

    context = {
        "articles": articles
    }

    return render(request, "blog/dashboard.html", context)