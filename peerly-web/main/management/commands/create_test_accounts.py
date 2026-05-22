from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import PeerlyUser
from main.models import StudentProfile, Course
import random

class Command(BaseCommand):
    help = 'Create test user accounts with student profiles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of test accounts to create (default: 50)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing test accounts before creating new ones',
        )

    def handle(self, *args, **options):
        count = options['count']
        clear = options['clear']

        if clear:
            PeerlyUser.objects.filter(email__startswith='testuser').delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing test accounts'))

        # Sample data
        first_names = ['Alex', 'Sarah', 'David', 'Emma', 'James', 'Olivia', 'Michael', 'Sophia', 'Daniel', 'Ava',
                       'John', 'Isabella', 'Chris', 'Mia', 'Ryan', 'Emily', 'Kevin', 'Charlotte', 'Brian', 'Harper',
                       'Liam', 'Amelia', 'Noah', 'Ella', 'Oliver', 'Grace', 'Benjamin', 'Chloe', 'Elijah', 'Avery',
                       'Lucas', 'Lily', 'Mason', 'Hannah', 'Logan', 'Scarlett', 'Jackson', 'Violet', 'Aiden', 'Layla']
        
        last_names = ['Chen', 'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez',
                      'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson',
                      'Martin', 'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis']
        
        degrees = [
            'Bachelor of Computer Science',
            'Bachelor of Engineering',
            'Bachelor of Science',
            'Bachelor of Arts',
            'Bachelor of Commerce',
            'Bachelor of Information Technology',
            'Bachelor of Mathematics',
            'Bachelor of Physics',
            'Bachelor of Chemistry',
            'Bachelor of Business Administration'
        ]
        
        years = ['1', '2', '3', '4', '5', 'postgrad']
        
        interests_pool = [
            'Coding', 'Web Development', 'Machine Learning', 'Game Development', 'Mobile Apps',
            'Data Science', 'UI/UX Design', 'Project Management', 'Startups', 'Entrepreneurship',
            'Hiking', 'Volleyball', 'Basketball', 'Soccer', 'Tennis', 'Swimming', 'Running',
            'Live Music', 'Concerts', 'Art', 'Photography', 'Videography', 'Filmmaking',
            'Cooking', 'Baking', 'Travel', 'Reading', 'Writing', 'Meditation', 'Yoga',
            'Gaming', 'Anime', 'Movies', 'TV Shows', 'Podcasts', 'Podcasting', 'Dancing',
            'Theater', 'Debate', 'Public Speaking', 'Volunteering', 'Community Service'
        ]
        
        courses_data = [
            ('COMS1000', 'Introduction to Computer Science'),
            ('COMS2000', 'Data Structures and Algorithms'),
            ('COMS3000', 'Operating Systems'),
            ('COMS3200', 'Network Security'),
            ('MATH1051', 'Calculus and Linear Algebra'),
            ('MATH2000', 'Discrete Mathematics'),
            ('PHYS1101', 'Physics 1'),
            ('CHEM1051', 'Chemistry 1'),
            ('BIOL1060', 'Biology for Engineers'),
            ('ENGG1100', 'Engineering Computing'),
        ]
        
        # Create or get courses
        courses = []
        for code, title in courses_data:
            course, created = Course.objects.get_or_create(code=code, defaults={'title': title})
            courses.append(course)

        created_count = 0
        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            full_name = f'{first_name} {last_name}'
            email = f'testuser{i+1}@student.uq.edu.au'

            # Check if user already exists
            if PeerlyUser.objects.filter(email=email).exists():
                self.stdout.write(f'User {email} already exists, skipping...')
                continue

            # Create user
            user = PeerlyUser.objects.create_user(
                email=email,
                password='TestPassword123!',
                full_name=full_name,
                is_email_verified=True
            )

            # Create student profile
            profile = StudentProfile.objects.create(
                user=user,
                degree=random.choice(degrees),
                year=random.choice(years),
                bio=f'Hi! I\'m {full_name}, a student at UQ. {"Currently struggling with distributed systems but loving the challenge. Looking for someone to grab coffee with and maybe tackle some LeetCode or go on a weekend hike!" if random.random() > 0.5 else "Passionate about learning and meeting new people. Let\'s collaborate on projects and have fun!"}',
                interests=random.sample(interests_pool, k=random.randint(3, 6)),
                classes=random.sample([c.code for c in courses], k=random.randint(2, 4))
            )

            created_count += 1
            self.stdout.write(f'Created user {created_count}: {email} - {full_name}')

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} test accounts!')
        )
