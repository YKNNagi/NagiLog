from django.shortcuts import render,redirect
from .models import Article, Tag
from .forms import ArticleForm
from django.shortcuts import get_object_or_404

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

def update(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)

        if form.is_valid():
            form.save()
        return redirect("dashboard")


    else:
        form = ArticleForm(instance=article)

    context = {
        "form": form,
    }

    return render(request, "blog/article_form.html", context)