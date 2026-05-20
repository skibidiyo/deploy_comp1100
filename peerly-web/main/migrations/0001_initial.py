from django.db import migrations, models
from django.utils import timezone


def seed_classmates(apps, schema_editor):
    Course = apps.get_model('main', 'Course')
    Classmate = apps.get_model('main', 'Classmate')

    course, _ = Course.objects.get_or_create(
        code='COMS3200',
        defaults={
            'title': 'Computer Communication Networks',
            'enrolled_classmates': 124,
        },
    )

    if Classmate.objects.filter(course=course).exists():
        return

    created_at = timezone.now()
    classmates = [
        {'full_name': 'Sarah Chen', 'degree_name': 'Bachelor of Computer Science', 'avatar_initials': 'SC', 'avatar_gradient': 'linear-gradient(135deg, #8B5CF6 0%, #F9A8D4 100%)', 'is_online': True, 'action_state': 'connect', 'display_order': 1},
        {'full_name': 'James Wilson', 'degree_name': 'B. Engineering (Honours)', 'avatar_initials': 'JW', 'avatar_gradient': 'linear-gradient(135deg, #1F2937 0%, #F59E0B 100%)', 'is_online': True, 'action_state': 'going', 'display_order': 2},
        {'full_name': 'Elena Rodriguez', 'degree_name': 'B. Information Tech', 'avatar_initials': 'ER', 'avatar_gradient': 'linear-gradient(135deg, #F59E0B 0%, #FDE68A 100%)', 'is_online': False, 'action_state': 'connect', 'display_order': 3},
        {'full_name': 'David Park', 'degree_name': 'Bachelor of Mathematics', 'avatar_initials': 'DP', 'avatar_gradient': 'linear-gradient(135deg, #111827 0%, #60A5FA 100%)', 'is_online': True, 'action_state': 'connect', 'display_order': 4},
        {'full_name': 'Maya Gupta', 'degree_name': 'B. Data Science', 'avatar_initials': 'MG', 'avatar_gradient': 'linear-gradient(135deg, #2563EB 0%, #7DD3FC 100%)', 'is_online': False, 'action_state': 'going', 'display_order': 5},
        {'full_name': 'Sam Thompson', 'degree_name': 'B. Science / B. Arts', 'avatar_initials': 'ST', 'avatar_gradient': 'linear-gradient(135deg, #374151 0%, #9CA3AF 100%)', 'is_online': True, 'action_state': 'connect', 'display_order': 6},
        {'full_name': 'Chloe Liang', 'degree_name': 'B. Interaction Design', 'avatar_initials': 'CL', 'avatar_gradient': 'linear-gradient(135deg, #EA580C 0%, #FDBA74 100%)', 'is_online': True, 'action_state': 'connect', 'display_order': 7},
        {'full_name': 'Marcus Bennett', 'degree_name': 'B. Software Engineering', 'avatar_initials': 'MB', 'avatar_gradient': 'linear-gradient(135deg, #16A34A 0%, #86EFAC 100%)', 'is_online': False, 'action_state': 'going', 'display_order': 8},
    ]

    Classmate.objects.bulk_create([
        Classmate(course=course, created_at=created_at, **classmate) for classmate in classmates
    ])


def remove_seed_classmates(apps, schema_editor):
    Course = apps.get_model('main', 'Course')
    Course.objects.filter(code='COMS3200').delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('enrolled_classmates', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['code']},
        ),
        migrations.CreateModel(
            name='Classmate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('degree_name', models.CharField(max_length=255)),
                ('avatar_initials', models.CharField(max_length=4)),
                ('avatar_gradient', models.CharField(max_length=120)),
                ('accent_color', models.CharField(default='#7C3AED', max_length=20)),
                ('is_online', models.BooleanField(default=False)),
                ('action_state', models.CharField(choices=[('connect', 'Connect'), ('going', 'Going')], default='connect', max_length=20)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='classmates', to='main.course')),
            ],
            options={'ordering': ['display_order', 'full_name']},
        ),
        migrations.RunPython(seed_classmates, remove_seed_classmates),
    ]
