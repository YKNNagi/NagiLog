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

    # 正しい記事を入力した場合、バリデーションを通過することを確認
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