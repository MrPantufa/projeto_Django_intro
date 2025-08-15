from django.db import models
from django.db.models import Q
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Technology(models.Model):
    BEGINNER = "B"
    INTERMEDIATE = "I"
    ADVANCED = "A"
    LEVEL_CHOICES = (
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (ADVANCED, "Advanced"),
    )

    name = models.CharField(max_length=50, unique=True)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, default=INTERMEDIATE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"


class Project(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    summary = models.CharField(max_length=220, blank=True)
    description = models.TextField(blank=True)
    repo_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, related_name="projects", blank=True)
    technologies = models.ManyToManyField(Technology, related_name="projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=Q(end_date__gte=models.F("start_date")) | Q(end_date__isnull=True) | Q(start_date__isnull=True),
                name="project_end_after_start",
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectLink(models.Model):
    DEMO = "DEMO"
    DOCS = "DOCS"
    OTHER = "OTHER"
    KIND_CHOICES = (
        (DEMO, "Demo"),
        (DOCS, "Docs"),
        (OTHER, "Other"),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="links")
    kind = models.CharField(max_length=8, choices=KIND_CHOICES, default=OTHER)
    label = models.CharField(max_length=60)
    url = models.URLField()

    class Meta:
        ordering = ["project", "kind", "label"]
        unique_together = ("project", "label")

    def __str__(self):
        return f"{self.project.title} · {self.label}"


class Experience(models.Model):
    company = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    technologies = models.ManyToManyField(Technology, related_name="experiences", blank=True)

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.CheckConstraint(
                check=Q(is_current=True) | Q(end_date__isnull=False),
                name="experience_current_or_has_end",
            ),
            models.CheckConstraint(
                check=Q(end_date__gte=models.F("start_date")) | Q(end_date__isnull=True),
                name="experience_end_after_start",
            ),
        ]

    def __str__(self):
        suffix = " (atual)" if self.is_current else ""
        return f"{self.role} · {self.company}{suffix}"


class Education(models.Model):
    institution = models.CharField(max_length=160)
    course = models.CharField(max_length=160)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.CheckConstraint(
                check=Q(end_date__gte=models.F("start_date")) | Q(end_date__isnull=True),
                name="education_end_after_start",
            )
        ]

    def __str__(self):
        return f"{self.course} · {self.institution}"
