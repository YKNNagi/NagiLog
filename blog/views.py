from django.shortcuts import render,redirect
from .models import Article, Tag
from .forms import ArticleForm, TagForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(
    lambda user: user.is_superuser,
    login_url="dashboard",
    redirect_field_name=None,
)
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
    articles = Article.objects.all().order_by("-created_at")
    tags = Tag.objects.all()

    selected_tag = request.GET.get("tag")

    if selected_tag:
        articles = articles.filter(
            tags__name=selected_tag
        )

    context = {
        "articles": articles,
        "tags": tags,
    }

    return render(request, "blog/dashboard.html", context)

@user_passes_test(
    lambda user: user.is_superuser,
    login_url="dashboard",
    redirect_field_name=None,
)
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

@user_passes_test(
    lambda user: user.is_superuser,
    login_url="dashboard",
    redirect_field_name=None,
)
def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == "POST":
        article.delete()
        return redirect("dashboard")

    context = {
        "article": article,
    }

    return render(
        request,
        "blog/article_confirm_delete.html",
        context,
    )

@user_passes_test(
    lambda user: user.is_superuser,
    login_url="dashboard",
    redirect_field_name=None,
)
def tag_create(request):
    if request.method == "POST":
        form = TagForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = TagForm()

    context = {
        "form": form,
    }

    return render(request, "blog/tag_form.html", context)