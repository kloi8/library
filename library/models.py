from django.db import models
from django.contrib.auth.models import User
class Discipline(models.Model):
    name = models.CharField(max_length=120)
    def __str__(self): return self.name
class SchoolClass(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self): return self.name
class Material(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title
class Profile(models.Model):
    ROLE_CHOICES = (('student','Ученик'),('teacher','Преподаватель'),('admin','Администратор'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    # school_class = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, blank=True)
    # Только для учеников
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Класс ученика"
    )

    # Только для преподавателей
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Предмет преподавателя"
    )

    def __str__(self): return f"{self.user.username} ({self.role})"
