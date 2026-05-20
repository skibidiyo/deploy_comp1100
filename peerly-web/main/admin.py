from django.contrib import admin

from .models import StudentProfile, Classmate, Course


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'degree', 'year', 'created_at')
	search_fields = ('user__email', 'degree')
	readonly_fields = ('created_at', 'updated_at')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ('code', 'title', 'enrolled_classmates')
	search_fields = ('code', 'title')


@admin.register(Classmate)
class ClassmateAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'course', 'degree_name', 'action_state', 'is_online', 'display_order')
	list_filter = ('course', 'action_state', 'is_online')
	search_fields = ('full_name', 'degree_name', 'course__code')
	ordering = ('course', 'display_order', 'full_name')
