from django.contrib import admin
from .models import StudySession, Goal, StudyNote

admin.site.register(StudySession)
admin.site.register(Goal)
admin.site.register(StudyNote)