from django.test import TestCase
from django.urls import reverse

from .forms import ArticleForm
from .models import Article, Tag


class ArticleFormTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="python")

    # 正しい入力でフォームが有効になることを確認する。基本的な記事を作成できることを保証するため。
    def test_form_with_valid_data_is_valid(self):
        form = ArticleForm(
            data={
                "title": "有効な記事タイトル",
                "body": "有効な記事本文",
                "tags": [self.tag.id],
                "is_pinned": False,
            }
        )

        self.assertTrue(form.is_valid())

    # タグを選択しなくてもフォームが有効になることを確認する。タグが任意という仕様を保証するため。
    def test_form_without_tags_is_valid(self):
        form = ArticleForm(
            data={
                "title": "タグなしの記事",
                "body": "タグを付けずに投稿する記事本文",
                "tags": [],
                "is_pinned": False,
            }
        )

        self.assertTrue(form.is_valid())

    # タイトルが最大文字数の50文字ならフォームが有効になることを確認する。境界値まで入力できることを保証するため。
    def test_form_with_max_length_title_is_valid(self):
        form = ArticleForm(
            data={
                "title": "A" * 50,
                "body": "有効な記事本文",
                "tags": [self.tag.id],
                "is_pinned": False,
            }
        )

        self.assertTrue(form.is_valid())

    # タイトルが空の場合にフォームが無効になることを確認する。タイトルのない記事を防ぐため。
    def test_form_with_empty_title_is_invalid(self):
        form = ArticleForm(
            data={
                "title": "",
                "body": "有効な記事本文",
                "tags": [self.tag.id],
                "is_pinned": False,
            }
        )

        self.assertFalse(form.is_valid())

    # タイトルが空白のみでもフォームが無効になることを確認する。見た目上入力済みでも実質空欄の記事を防ぐため。
    def test_form_with_whitespace_only_title_is_invalid(self):
        form = ArticleForm(
            data={
                "title": "　　　",
                "body": "有効な記事本文",
                "tags": [self.tag.id],
                "is_pinned": False,
            }
        )

        self.assertFalse(form.is_valid())

    # タイトルが51文字ならフォームが無効になることを確認する。最大文字数を超えた記事を防ぐため。
    def test_form_with_over_max_length_title_is_invalid(self):
        form = ArticleForm(
            data={
                "title": "A" * 51,
                "body": "有効な記事本文",
                "tags": [self.tag.id],
                "is_pinned": False,
            }
        )

        self.assertFalse(form.is_valid())

    # 本文が空の場合にフォームが無効になることを確認する。本文のない記事を防ぐため。
    def test_form_with_empty_body_is_invalid(self):
        form = ArticleForm(
            data={
                "title": "有効な記事タイトル",
                "body": "",
                "tags": [self.tag.id],
                "is_pinned": False,
            }
        )

        self.assertFalse(form.is_valid())

    # 本文が空白のみでもフォームが無効になることを確認する。見た目上入力済みでも実質空欄の記事を防ぐため。
    def test_form_with_whitespace_only_body_is_invalid(self):
        form = ArticleForm(
            data={
                "title": "有効な記事タイトル",
                "body": "　　　　",
                "tags": [self.tag.id],
                "is_pinned": False,
            }
        )

        self.assertFalse(form.is_valid())


class ArticleModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="python")

    # 正しい内容の記事が各フィールドを保って保存されることを確認する。Articleの基本的な永続化を保証するため。
    def test_article_with_valid_data_is_saved(self):
        article = Article.objects.create(
            title="有効な記事タイトル",
            body="有効な記事本文",
            is_pinned=False,
        )

        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(article.title, "有効な記事タイトル")
        self.assertEqual(article.body, "有効な記事本文")
        self.assertFalse(article.is_pinned)

    # 記事にタグを関連付けられることを確認する。ArticleとTagの多対多関係が保存されることを保証するため。
    def test_article_associated_with_tag_has_relation(self):
        article = Article.objects.create(
            title="Python学習記録",
            body="Pythonの基本を学習した記録",
            is_pinned=False,
        )

        article.tags.add(self.tag)

        self.assertEqual(article.tags.count(), 1)
        self.assertIn(self.tag, article.tags.all())

    # Articleの文字列表現がタイトルになることを確認する。管理画面などで記事を識別しやすくするため。
    def test_article_string_representation_returns_title(self):
        article = Article.objects.create(
            title="Python学習記録",
            body="Pythonの基本を学習した記録",
            is_pinned=False,
        )

        self.assertEqual(str(article), "Python学習記録")

    # Tagの文字列表現がタグ名になることを確認する。選択肢などでタグを識別しやすくするため。
    def test_tag_string_representation_returns_name(self):
        self.assertEqual(str(self.tag), "python")


class ArticleCreateViewTest(TestCase):
    def setUp(self):
        # 保存と遷移のテストで同じ正常入力を使い、各テストの違いを結果の確認へ集中させる。
        self.valid_post_data = {
            "title": "有効な記事タイトル",
            "body": "有効な記事本文",
            "tags": [],
            "is_pinned": False,
        }

    # GETで記事作成画面と対応テンプレートが返ることを確認する。投稿フォームへ正常にアクセスできることを保証するため。
    def test_create_page_on_get_returns_success(self):
        response = self.client.get("/create/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/article_form.html")

    # 正常なPOSTで記事数と入力内容が保存されることを確認する。Create処理がデータを欠落なく永続化することを保証するため。
    def test_create_with_valid_data_saves_article(self):
        self.client.post("/create/", self.valid_post_data)

        self.assertEqual(Article.objects.count(), 1)
        article = Article.objects.get(title="有効な記事タイトル")
        self.assertEqual(article.title, "有効な記事タイトル")
        self.assertEqual(article.body, "有効な記事本文")

    # 不正なPOSTで記事が保存されないことを確認する。入力エラーによる不完全な記事作成を防ぐため。
    def test_create_with_invalid_data_does_not_save_article(self):
        data = {
            "title": "本文が空の記事",
            "body": "",
            "tags": [],
            "is_pinned": False,
        }

        self.client.post("/create/", data)

        self.assertEqual(Article.objects.count(), 0)

    # 不正なPOSTでエラーと入力済み本文が保持されることを確認する。修正時に本文を入力し直す負担を防ぐため。
    def test_create_with_invalid_data_preserves_errors_and_input(self):
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
            "めちゃくちゃ頑張って書いた記事本文",
        )

    # 正常なPOST後にDashboardへリダイレクトされることを確認する。再送信を避けて保存後の一覧へ移動するため。
    def test_create_with_valid_data_redirects_to_dashboard(self):
        response = self.client.post("/create/", self.valid_post_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/dashboard/")

    # タグ付きのPOSTで記事とタグが関連付けられることを確認する。選択した分類が保存時に失われないことを保証するため。
    def test_create_with_tags_saves_tag_relation(self):
        tag = Tag.objects.create(name="python")
        data = {
            "title": "Python学習記録",
            "body": "Pythonの基本を学習した記録",
            "tags": [tag.id],
            "is_pinned": False,
        }

        self.client.post("/create/", data)
        article = Article.objects.get(title="Python学習記録")

        self.assertIn(tag, article.tags.all())


class DashboardViewTest(TestCase):
    # GETでDashboardと対応テンプレートが返ることを確認する。記事一覧へ正常にアクセスできることを保証するため。
    def test_dashboard_on_get_returns_success(self):
        response = self.client.get("/dashboard/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/dashboard.html")

    # 複数の保存済み記事がすべて表示されることを確認する。一覧から記事が欠落しないことを保証するため。
    def test_dashboard_with_multiple_articles_displays_all_titles(self):
        Article.objects.create(
            title="Python学習記録",
            body="Pythonの基本を学習した記録",
            is_pinned=False,
        )
        Article.objects.create(
            title="Django学習記録",
            body="Djangoのフォームを学習した記録",
            is_pinned=False,
        )

        response = self.client.get("/dashboard/")

        self.assertContains(response, "Python学習記録")
        self.assertContains(response, "Django学習記録")

class ArticleUpdateViewTest(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title="更新前の記事タイトル",
            body="更新前の記事本文",
            is_pinned=False,
        )

    # 既存記事の編集画面をGETした場合、正常に表示されることを確認する。Update画面へアクセスできることを保証するため。
    def test_update_page_on_get_returns_success(self):
        response = self.client.get(
            reverse("update", args=[self.article.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/article_form.html")

    # 編集画面に既存記事の内容が表示されることを確認する。編集前の内容を保持した状態から変更できることを保証するため。
    def test_update_page_displays_existing_article_data(self):
        response = self.client.get(
            reverse("update", args=[self.article.id])
        )

        form = response.context["form"]

        self.assertEqual(
            form["title"].value(),
            "更新前の記事タイトル",
        )

        self.assertEqual(
            form["body"].value(),
            "更新前の記事本文",
        )

    # 正しい内容をPOSTした場合、既存記事が更新されることを確認する。新規記事を作らず対象記事を書き換えられることを保証するため。
    def test_update_with_valid_data_updates_article(self):
        data = {
            "title": "更新後の記事タイトル",
            "body": "更新後の記事本文",
            "tags": [],
            "is_pinned": False,
        }

        self.client.post(
            reverse("update", args=[self.article.id]),
            data,
        )

        self.article.refresh_from_db()

        self.assertEqual(
            self.article.title,
            "更新後の記事タイトル",
        )
        self.assertEqual(
            self.article.body,
            "更新後の記事本文",
        )
        self.assertEqual(Article.objects.count(), 1)

    # 正しい内容をPOSTした場合、Dashboardへリダイレクトされることを確認する。更新後の再送信を避けて一覧へ戻れることを保証するため。
    def test_update_with_valid_data_redirects_to_dashboard(self):
        data = {
            "title": "更新後の記事タイトル",
            "body": "更新後の記事本文",
            "tags": [],
            "is_pinned": False,
        }

        response = self.client.post(
            reverse("update", args=[self.article.id]),
            data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/dashboard/")

    # 不正な内容をPOSTした場合、既存記事が更新されないことを確認する。入力エラーによって保存済みの記事が壊れることを防ぐため。
    def test_update_with_invalid_data_does_not_change_article(self):
        data = {
                    "title": "",
                    "body": "更新しようとした記事本文",
                    "tags": [],
                    "is_pinned": False,
                }

        self.client.post(
            reverse("update", args=[self.article.id]),
            data,
        )

        self.article.refresh_from_db()

        self.assertEqual(
            self.article.title,
            "更新前の記事タイトル",
        )

        self.assertEqual(
            self.article.body,
            "更新前の記事本文",
        )

    # 存在しない記事IDへアクセスした場合、404になることを確認する。存在しない記事を編集できないことを保証するため。
    def test_update_with_missing_article_returns_404(self):
        response = self.client.get(
            reverse("update", args=[9999])
        )

        self.assertEqual(response.status_code, 404)