from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import BooleanBlock, TextBlock, StructBlock, CharBlock, PageChooserBlock, RichTextBlock

class QuestionList(Page):
    questions = StreamField(
        [
            ("question", PageChooserBlock(page_type="questions.QuestionItem")),
        ],
        null=False,
        blank=False,
    )

    content_panels = Page.content_panels + [
        FieldPanel("questions"),
    ]

class QuestionItem(Page):
    question = models.CharField(max_length=255)
    answers = StreamField(
        [
            ("answer", RichTextBlock()),
            ("is_correct", BooleanBlock(required=True)),
        ], null=True, blank=True, max_num=5, min_num=2
    )

    content_panels = Page.content_panels + [
        FieldPanel("question"),
        FieldPanel("answer"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("question"),
        FieldPanel("answers"),
    ]