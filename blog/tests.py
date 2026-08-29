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