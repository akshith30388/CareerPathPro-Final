import json
from collections import defaultdict

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from students.models import CounselorAssignment, StudentSubmission, TopicAnalysis
from users.models import StudentProfile


class CounselorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        counselor_id = self.scope["url_route"]["kwargs"]["counselor_id"]

        if not user or not user.is_authenticated or int(user.id) != int(counselor_id):
            await self.close()
            return

        self.counselor_id = int(counselor_id)
        self.group_name = f"counselor_{self.counselor_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        assigned_students = await self._get_assigned_students()
        await self.send(text_data=json.dumps({"type": "assigned_students", "students": assigned_students}))

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return
        payload = json.loads(text_data)
        message_type = payload.get("type")

        if message_type == "ping":
            await self.send(text_data=json.dumps({"type": "pong"}))

    async def student_assigned(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "student_assigned",
                    "student_id": event.get("student_id"),
                    "student_name": event.get("student_name"),
                    "assigned_at": event.get("assigned_at"),
                }
            )
        )

    async def assignment_submitted(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "assignment_submitted",
                    "student_id": event.get("student_id"),
                    "student_name": event.get("student_name"),
                    "score": event.get("score"),
                    "percentage": event.get("percentage"),
                    "assignment_title": event.get("assignment_title"),
                    "submitted_at": event.get("submitted_at"),
                }
            )
        )

    async def student_profile_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "student_profile_update",
                    "student_id": event.get("student_id"),
                    "student_name": event.get("student_name"),
                }
            )
        )

    @database_sync_to_async
    def _get_assigned_students(self):
        assignments = (
            CounselorAssignment.objects.filter(counselor_id=self.counselor_id, is_active=True)
            .select_related("student")
            .order_by("-assigned_at")
        )
        students_payload = []
        for assignment in assignments:
            student = assignment.student
            profile = StudentProfile.objects.filter(user=student).first()
            latest_submission = (
                StudentSubmission.objects.filter(student=student, is_submitted=True)
                .select_related("assignment")
                .order_by("-completed_at")
                .first()
            )
            topic_labels = defaultdict(list)
            if latest_submission:
                for analysis in TopicAnalysis.objects.filter(submission=latest_submission):
                    topic_labels[analysis.strength_level].append(analysis.topic)

            students_payload.append(
                {
                    "id": student.id,
                    "name": student.get_full_name() or student.username,
                    "email": student.email,
                    "phone": student.phone,
                    "profile_photo": student.profile_picture.url if student.profile_picture else "",
                    "city": profile.city if profile else "",
                    "last_active": student.last_login.isoformat() if student.last_login else "",
                    "latest_score": latest_submission.total_score if latest_submission else None,
                    "latest_percentage": latest_submission.percentage if latest_submission else None,
                    "latest_assignment": latest_submission.assignment.title if latest_submission else "",
                    "strong_topics": topic_labels["strong"],
                    "average_topics": topic_labels["average"],
                    "weak_topics": topic_labels["weak"],
                    "assigned_at": assignment.assigned_at.isoformat(),
                }
            )
        return students_payload


class StudentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        student_id = self.scope["url_route"]["kwargs"]["student_id"]

        if not user or not user.is_authenticated or int(user.id) != int(student_id):
            await self.close()
            return

        self.student_id = int(student_id)
        self.group_name = f"student_{self.student_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return
        payload = json.loads(text_data)
        if payload.get("type") == "ping":
            await self.send(text_data=json.dumps({"type": "pong"}))

    async def counselor_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "counselor_message",
                    "message": event.get("message", ""),
                    "sent_at": event.get("sent_at"),
                }
            )
        )

    async def session_scheduled(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "session_scheduled",
                    "session_date": event.get("session_date"),
                    "session_time": event.get("session_time"),
                    "message": event.get("message", ""),
                }
            )
        )

