from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import BooleanBlock, StructBlock, PageChooserBlock, RichTextBlock

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.utils import timezone

from datetime import timedelta

class QuestionListIndex(Page):
    parent_page_types = ["home.LandingPage"]
    is_creatable = False

    default_instructions = RichTextField(max_length=255, verbose_name="Instruções padrão", null=True, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        if request.method == "POST":
            question_list_id = request.POST.get("list_id")
            question_list = QuestionList.objects.get(id=question_list_id)
            list_submission = question_list.start_list(request)
            if list_submission:
                return redirect(list_submission)
            context["error"] = "Você já está fazendo uma prova"

        context["lists"] = QuestionList.objects.live()
        active_submissions = QuestionListSubmission.get_active_submissions(request.user)
        if active_submissions:
            active_list = active_submissions[0].questionsList
            context["active_list"] = active_list
            
        return context
    
    def start_list(request, question_list_id):
        question_list = QuestionList.objects.get(id=question_list_id)
        submission = QuestionListSubmission.objects.create(user=request.user, questionsList=question_list, answers={})
        return submission

    content_panels = Page.content_panels + [
        FieldPanel("default_instructions"),
    ]

    @method_decorator(login_required)
    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

class QuestionList(Page):
    parent_page_types = ["questions.QuestionListIndex"]

    questions = StreamField(
        [
            ("question", PageChooserBlock(page_type="questions.QuestionItem")),
        ],
        null=True,
        blank=True,
    )

    duration = models.IntegerField(verbose_name="Duração em minutos", default=120)

    instructions = RichTextField(max_length=255, verbose_name="Instruções", null=True, blank=True)
    
    def start_list(self, request):
        existing_submissions = QuestionListSubmission.get_active_submissions(request.user)
        if existing_submissions:
            return False
        submission = QuestionListSubmission.objects.create(user=request.user, questionsList=self, answers={})
        return submission

    content_panels = Page.content_panels + [
        FieldPanel("questions"),
        FieldPanel("duration"),
        FieldPanel("instructions"),
    ]

    def context(self, request):
        context = super().get_context(request)
        return context

    class Meta:
        verbose_name = "Lista de Questões"

    @property
    def list_size(self):
        return len(self.questions)

    @method_decorator(login_required)
    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

class QuestionItem(Page):
    parent_page_types = ["questions.QuestionList", "questions.QuestionListIndex"]
    question = RichTextField(max_length=255, verbose_name="Enunciado da questão")
    answers = StreamField(
        [
            (
                "option", StructBlock([
                    ("answer", RichTextBlock()),
                    ("is_correct", BooleanBlock(default=False, required=False)),
                ])
            )
        ], null=True, blank=True, max_num=5, min_num=2, verbose_name="Alternativas"
    )

    content_panels = Page.content_panels + [
        FieldPanel("question"),
        FieldPanel("answers"),
    ]

    class Meta:
        verbose_name = "Questão"

    @method_decorator(login_required)
    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

class QuestionListSubmission(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    questionsList = models.ForeignKey("questions.QuestionList", on_delete=models.CASCADE)
    answers = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_finished = models.BooleanField(default=False)
    
    def is_active(self):
        duration = self.questionsList.duration
        return not self.is_finished and self.created_at + timedelta(minutes=duration) > timezone.now()
    
    @staticmethod
    def get_active_submissions(user):
        user_submissions = QuestionListSubmission.objects.filter(user=user)
        active_user_submissions = [submission for submission in user_submissions if submission.is_active]
        return active_user_submissions

    def __str__(self):
        return f"{self.user.email} - {self.list.title}"
