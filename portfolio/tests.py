from datetime import date
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import (
    Tag,
    Technology,
    Project,
    ProjectLink,
    Experience,
    Education,
)

class TagModelTests(TestCase):
    def test_tag_unique_name(self):
        Tag.objects.create(name="Django")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Tag.objects.create(name="Django")

class TechnologyModelTests(TestCase):
    def test_str_and_choices(self):
        t = Technology.objects.create(name="Django", level=Technology.ADVANCED)
        self.assertEqual(str(t), "Django (Advanced)")
        self.assertEqual(t.level, Technology.ADVANCED)

class ProjectModelTests(TestCase):
    def test_slug_is_auto_generated_from_title(self):
        p = Project.objects.create(title="Meu Projeto X")
        self.assertEqual(p.slug, "meu-projeto-x")

    def test_end_date_must_be_after_start_or_null(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Project.objects.create(
                    title="Inválido",
                    start_date=date(2024, 1, 10),
                    end_date=date(2024, 1, 1),
                )

    def test_many_to_many_relations(self):
        p = Project.objects.create(title="Site")
        t1 = Technology.objects.create(name="Python")
        t2 = Technology.objects.create(name="Django")
        p.technologies.add(t1, t2)
        self.assertEqual(p.technologies.count(), 2)

class ProjectLinkModelTests(TestCase):
    def test_unique_label_per_project(self):
        p = Project.objects.create(title="Portfólio")
        ProjectLink.objects.create(project=p, label="GitHub", url="https://example.com")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProjectLink.objects.create(project=p, label="GitHub", url="https://ex.com/2")

class ExperienceModelTests(TestCase):
    def test_end_after_start_or_null_and_current_flag(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Experience.objects.create(
                    company="Empresa",
                    role="Dev",
                    start_date=date(2024, 1, 10),
                    end_date=None,
                    is_current=False,
                )
        e = Experience.objects.create(
            company="Empresa",
            role="Dev",
            start_date=date(2024, 1, 10),
            end_date=None,
            is_current=True,
        )
        self.assertIn("Empresa", str(e))

class EducationModelTests(TestCase):
    def test_end_date_after_start(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Education.objects.create(
                    institution="Uni",
                    course="ADS",
                    start_date=date(2024, 1, 10),
                    end_date=date(2024, 1, 1),
                )
        ok = Education.objects.create(
            institution="Uni",
            course="ADS",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 6, 1),
        )
        self.assertIn("Uni", str(ok))
