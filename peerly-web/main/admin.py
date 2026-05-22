from django.contrib import admin

from .models import StudentProfile, Classmate, Course, Community, CommunityMembership, StudySession, DiscoverAction


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


class CommunityMembershipInline(admin.TabularInline):
	model = CommunityMembership
	extra = 0
	readonly_fields = ('user', 'joined_at')
	can_delete = True


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'creator', 'member_count', 'created_at')
	search_fields = ('name', 'category')
	readonly_fields = ('created_at',)
	inlines = [CommunityMembershipInline]

	def member_count(self, obj):
		return obj.members.count()
	member_count.short_description = 'Members'


@admin.register(CommunityMembership)
class CommunityMembershipAdmin(admin.ModelAdmin):
	list_display = ('user', 'community', 'joined_at')
	list_filter = ('community',)
	search_fields = ('user__email', 'community__name')
	readonly_fields = ('joined_at',)


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
	list_display = ('title', 'course_code', 'scheduled_at', 'host', 'attendee_count')
	list_filter = ('course_code',)
	search_fields = ('title', 'course_code', 'host__email')
	readonly_fields = ('created_at',)

	def attendee_count(self, obj):
		return obj.attendees.count()
	attendee_count.short_description = 'Attendees'


@admin.register(DiscoverAction)
class DiscoverActionAdmin(admin.ModelAdmin):
	list_display = ('user', 'target_user', 'action_type', 'created_at')
	list_filter = ('action_type',)
	search_fields = ('user__email', 'target_user__email')
