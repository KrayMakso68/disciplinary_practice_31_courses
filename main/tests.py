from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from main.models import Category, CustomUser, Note


class CorporateHierarchyModelTests(TestCase):
    def setUp(self):
        self.branch = Category.objects.create(
            title="Центральный филиал",
            type=Category.COURSE_TYPE,
            slug="central-branch"
        )
        self.dept = Category.objects.create(
            title="Отдел разработки",
            type=Category.GROUP_TYPE,
            parent=self.branch,
            slug="dev-dept"
        )
        self.team = Category.objects.create(
            title="Команда бэкенда",
            type=Category.UNIT_TYPE,
            parent=self.dept,
            slug="backend-team"
        )

        self.lead = CustomUser.objects.create_user(
            username="teamlead",
            first_name="Алексей",
            last_name="Смирнов",
            surname="Игоревич",
            role=CustomUser.TEAM_LEAD,
            rang="Lead",
            category=self.team
        )

        self.employee = CustomUser.objects.create_user(
            username="employee1",
            first_name="Дмитрий",
            last_name="Иванов",
            surname="Сергеевич",
            role=CustomUser.EMPLOYEE,
            rang="Middle",
            category=self.team
        )

    def test_mptt_hierarchy(self):
        descendants = list(self.branch.get_descendants())
        self.assertEqual(len(descendants), 2)
        self.assertIn(self.dept, descendants)
        self.assertIn(self.team, descendants)

    def test_user_get_fio(self):
        fio = self.lead.get_FIO()
        self.assertEqual(fio, "Смирнов А.И.")

    def test_note_creation_and_types(self):
        note = Note.objects.create(
            cadet=self.employee,
            type=Note.TYPE_ACHIEVEMENT,
            who_gave=self.lead,
            text="Успешный релиз новой функциональности без сбоев"
        )
        self.assertEqual(note.cadet, self.employee)
        self.assertEqual(note.type, "Достижение")
        self.assertTrue(note.check_active)
        self.assertIsNotNone(note.date)
        self.assertTrue(timezone.is_aware(note.date) or isinstance(note.date, timezone.datetime))

    def test_role_permissions(self):
        # Regular employee role is 1, leadership is > 1
        self.assertFalse(self.employee.role > CustomUser.EMPLOYEE)
        self.assertTrue(self.lead.role > CustomUser.EMPLOYEE)
