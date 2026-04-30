import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from appointments.models import Appointment, Feedback
from assessments.models import AssessmentResult
from chat.models import Message
from recommendations.models import CareerRecommendation
from users.models import CustomUser


class DashboardViewTests(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(
            username='student1',
            password='pass12345',
            role='student',
            first_name='Test',
            last_name='Student',
        )
        self.counselor = CustomUser.objects.create_user(
            username='counselor1',
            password='pass12345',
            role='counselor',
            first_name='Test',
            last_name='Counselor',
        )

        self.assessment_result = AssessmentResult.objects.create(
            student=self.student,
            score=8,
            total_questions=10,
            percentage=80,
            answers={'1': 'a'},
            career_scores={'Engineer': 4},
        )

        CareerRecommendation.objects.create(
            student=self.student,
            assessment_result=self.assessment_result,
            recommended_career='Software Engineer',
            confidence_score=87,
            description='Build software systems and products.',
            skills_required='Python,Problem Solving',
            roadmap=['Learn Python', 'Build Projects'],
        )

        self.appointment = Appointment.objects.create(
            student=self.student,
            counselor=self.counselor,
            date=timezone.localdate() + datetime.timedelta(days=1),
            time_slot='10:00',
            status='pending',
            notes='Need guidance for internships',
        )

        Message.objects.create(
            sender=self.counselor,
            receiver=self.student,
            content='Hello student',
            is_read=False,
        )
        Message.objects.create(
            sender=self.student,
            receiver=self.counselor,
            content='Hello counselor',
            is_read=False,
        )

    def test_dashboard_redirect_student(self):
        self.client.login(username='student1', password='pass12345')
        response = self.client.get(reverse('dashboard:redirect'))
        self.assertRedirects(response, reverse('dashboard:student'))

    def test_dashboard_redirect_counselor(self):
        self.client.login(username='counselor1', password='pass12345')
        response = self.client.get(reverse('dashboard:redirect'))
        self.assertRedirects(response, reverse('dashboard:counselor'))

    def test_student_dashboard_page_loads(self):
        self.client.login(username='student1', password='pass12345')
        response = self.client.get(reverse('dashboard:student'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_assessments'], 1)
        self.assertEqual(response.context['total_recommendations'], 1)
        self.assertEqual(response.context['pending_appointments'], 1)

    def test_student_dashboard_data_endpoint(self):
        self.client.login(username='student1', password='pass12345')
        response = self.client.get(reverse('dashboard:student_data'))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['totals']['assessments'], 1)
        self.assertEqual(payload['totals']['recommendations'], 1)
        self.assertEqual(len(payload['appointments']), 1)

    def test_counselor_dashboard_page_loads(self):
        self.client.login(username='counselor1', password='pass12345')
        Feedback.objects.create(
            appointment=self.appointment,
            student=self.student,
            counselor=self.counselor,
            rating=5,
            comment='Very helpful.',
        )

        response = self.client.get(reverse('dashboard:counselor'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pending_appointments_count'], 1)
        self.assertEqual(response.context['unread_messages'], 1)

    def test_counselor_dashboard_data_endpoint(self):
        self.client.login(username='counselor1', password='pass12345')
        response = self.client.get(reverse('dashboard:counselor_data'))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['totals']['pending'], 1)
        self.assertEqual(payload['totals']['unread_messages'], 1)

    def test_student_cannot_access_counselor_json(self):
        self.client.login(username='student1', password='pass12345')
        response = self.client.get(reverse('dashboard:counselor_data'))
        self.assertEqual(response.status_code, 403)

    def test_student_dashboard_linked_endpoints(self):
        self.client.login(username='student1', password='pass12345')

        self.assertEqual(self.client.get(reverse('assessments:start')).status_code, 200)
        self.assertEqual(self.client.get(reverse('appointments:book')).status_code, 200)
        self.assertEqual(self.client.get(reverse('appointments:my_appointments')).status_code, 200)
        self.assertEqual(self.client.get(reverse('recommendations:list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('dashboard:resume_builder')).status_code, 200)
        self.assertEqual(self.client.get(reverse('chat:inbox')).status_code, 200)

    def test_counselor_dashboard_linked_endpoints(self):
        self.client.login(username='counselor1', password='pass12345')

        self.assertEqual(self.client.get(reverse('appointments:manage')).status_code, 200)
        self.assertEqual(self.client.get(reverse('chat:inbox')).status_code, 200)
        self.assertEqual(self.client.get(reverse('users:edit_profile')).status_code, 200)

        response = self.client.post(
            reverse('appointments:update', args=[self.appointment.pk]),
            {'status': 'confirmed'},
        )
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'confirmed')
