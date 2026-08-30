from django.test import TestCase
from .forms import ArticleForm
from .models import Article, Tag

#フォームテスト
class ArticleFormTest(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(name="Python")

    # 正しい記事を入力した場合、バリデーションを通過することを確認
    def test_valid_article(self):
        form = ArticleForm(
            data={
                "title": "テスト記事",
                "body": "テスト記事中身",
                "tags": [self.tag.id],
                "is_pinned": False,
            }
        )

        self.assertTrue(form.is_valid())

    # タイトルが空の場合、バリデーションエラーになることを確認
    def test_empty_title(self):
        form = ArticleForm(
            data={
                "title": "",
                "body": "テスト記事中身",
                "tags": [self.tag.id],
                "is_pinned": False,
            }
        )

        self.assertFalse(form.is_valid())

    #空白のみのタイトルを入力した場合、バリデーションエラーになることを確認
    def test_whitespace_only_title(self):
        form = ArticleForm(
            data = {
                "title": "　　　",
                "body":"テスト記事中身",
                "tags":[self.tag.id],
                "is_pinned": False,
            }
        )

        self.assertFalse(form.is_valid())

    # 本文が空の場合、バリデーションエラーになることを確認
    def test_empty_body(self):
        form = ArticleForm(
            data={
                "title": "テスト記事",
                "body": "",
                "tags": [self.tag.id],
                "is_pinned": False,
            }
        )

        self.assertFalse(form.is_valid())

    #空白のみの本文を入力した場合、バリデーションエラーになることを確認
    def test_whitespace_only_body(self):
        form = ArticleForm(
            data = {
                "title": "テスト記事",
                "body":"　　　　",
                "tags":[self.tag.id],
                "is_pinned": False,
            }
        )
    
        self.assertFalse(form.is_valid())

    # タグを選択しなくても、バリデーションを通過することを確認
    def test_valid_article_without_tags(self):
        form = ArticleForm(
            data={
                "title": "テスト記事",
                "body": "テスト記事中身",
                "tags": [],
                "is_pinned": False,
            }
        )
    
        self.assertTrue(form.is_valid())

    # タイトルが最大文字数の50文字なら、バリデーションを通過することを確認
    def test_title_max_length(self):
        form = ArticleForm(
            data={
                "title": "A" * 50,
                "body": "テスト記事中身",
                "tags": [self.tag.id],
                "is_pinned": False,
            }
        )

        self.assertTrue(form.is_valid())

    # タイトルが最大文字数を超えた場合、バリデーションエラーになることを確認
    def test_title_over_max_length(self):
        form = ArticleForm(
            data={
                "title": "A" * 51,
                "body": "テスト記事中身",
                "tags": [self.tag.id],
                "is_pinned": False,
            }
        )

        self.assertFalse(form.is_valid())

#モデルテスト
class ArticleModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Python")

    # 記事が正しい内容でDBに保存されることを確認
    def test_create_article(self):
        article = Article.objects.create(
            title="テスト記事",
            body="テスト記事中身",
            is_pinned=False,
        )

        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(article.title, "テスト記事")
        self.assertEqual(article.body, "テスト記事中身")
        self.assertFalse(article.is_pinned)

    # 記事にタグを関連付けて保存できることを確認
    def test_article_can_have_tags(self):
        article = Article.objects.create(
            title="テスト記事",
            body="テスト記事中身",
            is_pinned=False,
        )

        article.tags.add(self.tag)

        self.assertEqual(article.tags.count(), 1)
        self.assertIn(self.tag, article.tags.all())

    # Articleの文字列表現としてタイトルが返されることを確認
    def test_article_str_returns_title(self):
        article = Article.objects.create(
            title="テスト記事",
            body="テスト記事中身",
            is_pinned=False,
        )

        self.assertEqual(str(article), "テスト記事")

    # Tagの文字列表現としてタグ名が返されることを確認
    def test_tag_str_returns_name(self):

        self.assertEqual(str(self.tag), "Python")

#ビューテスト
class ArticleViewTest(TestCase):

    # 記事作成画面を正常に表示できることを確認
    def test_create_view_get(self):

        response = self.client.get("/create/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/article_form.html")

    # ダッシュボードを正常に表示できることを確認
    def test_dashboard_view_get(self):

        response = self.client.get("/dashboard/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/dashboard.html")

    # 正しい入力で記事を作成するとDBに保存されることを確認
    def test_create_view_post_valid_data(self):

        data = {
            "title": "テスト記事",
            "body": "テスト記事中身",
            "tags": [],
            "is_pinned": False,
        }

        response = self.client.post("/create/", data)

        self.assertEqual(Article.objects.count(), 1)

    # POSTした記事の内容が正しくDBに保存されることを確認
    def test_create_view_saves_posted_article_data(self):

        data = {
            "title": "テスト記事",
            "body": "テスト記事中身",
            "tags": [],
            "is_pinned": False,
        }

        response = self.client.post("/create/", data)

        article = Article.objects.get(title="テスト記事")

        self.assertEqual(article.title, "テスト記事")
        self.assertEqual(article.body, "テスト記事中身")

    # 不正な入力では記事が保存されないことを確認
    def test_create_view_post_invalid_data(self):

        data = {
                    "title": "テスト記事",
                    "body": "",
                    "tags": [],
                    "is_pinned": False,
                }

        response = self.client.post("/create/", data)

        self.assertEqual(Article.objects.count(), 0)

    # 不正な入力の場合、入力済みフォームとエラーが再表示されることを確認
    def test_create_view_invalid_form_keeps_errors(self):
        data = {
            "title": "",
            "body": "めちゃくちゃ頑張って書いた記事本文",
            "tags": [],
            "is_pinned": False,
        }

        response = self.client.post("/create/", data)

        form = response.context["form"]

        self.assertIn("title", form.errors)
        self.assertEqual(
            form["body"].value(),
            "めちゃくちゃ頑張って書いた記事本文"
        )

    # 正しい入力で記事を作成した場合、ダッシュボードへリダイレクトされることを確認
    def test_create_view_redirects_to_dashboard(self):
        data = {
            "title": "テスト記事",
            "body": "テスト記事中身",
            "tags": [],
            "is_pinned": False,
        }

        response = self.client.post("/create/", data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/dashboard/")

    # ダッシュボードに保存済み記事のタイトルが表示されることを確認
    def test_dashboard_displays_article_title(self):
        Article.objects.create(
            title="テスト記事",
            body="テスト記事中身",
            is_pinned=False,
        )

        response = self.client.get("/dashboard/")

        self.assertContains(response, "テスト記事")

    # ダッシュボードに複数の保存済み記事がすべて表示されることを確認
    def test_dashboard_displays_multiple_articles(self):
        Article.objects.create(
            title="テスト記事1",
            body="テスト記事中身1",
            is_pinned=False,
        )

        Article.objects.create(
            title="テスト記事2",
            body="テスト記事中身2",
            is_pinned=False,
        )

        response = self.client.get("/dashboard/")

        self.assertContains(response, "テスト記事1")
        self.assertContains(response, "テスト記事2")

    # タグ付きの記事をPOSTした場合、記事とタグが正しく関連付けて保存されることを確認
    def test_create_view_saves_article_with_tags(self):
        tag = Tag.objects.create(name="python")

        data = {
            "title": "テスト記事",
            "body": "テスト記事中身",
            "tags": [tag.id],
            "is_pinned": False,
            }

        response = self.client.post("/create/", data)

        article = Article.objects.get(title="テスト記事")

        self.assertIn(tag, article.tags.all())