import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse


def create_question(question_text, days):
    """
    Create a question with given question_text and set pub_date
    as given number of days offset to now(negative for question published
    in the past, and positive for questions that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


# Question model test cases:
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns false for questions
        with pub_date in future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns false for questions
        with pub_date older than a day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns true for questions
        with pub_date within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


# Index View Test cases :
class QuestionIndexViewTests(TestCase):

    def test_no_question(self):
        """
        If no questions exists, an appropriate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available, babe")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with pub_date in the past
        are displayed on the index page.
        """
        create_question(question_text='Past Question Example', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past Question Example>']
                                 )

    def test_future_question(self):
        """
        Question with pub_date in the future
        are not displayed on the index page.
        """
        create_question(question_text="Future Question Example", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 []
                                 )

    def future_and_past_question(self):
        """
        Even if future and past questions exists
        only past questions should display on index page
        """
        create_question(question_text="Future Question Example", days=30)
        create_question(question_text="Past Question Example", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past Question Example>']
                                 )

    def two_past_question(self):
        """
        When 2 questions with pub_date in past exists both
        of the questions should display on index page.
        """
        create_question(question_text="Past Question Example 1", days=-30)
        create_question(question_text="Past Question Example 2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past Question Example 1>',
                                     '<Question: Past Question Example 2>']
                                 )
