from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='problems.problem')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problem_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='problemvote',
            constraint=models.UniqueConstraint(fields=('problem', 'student'), name='unique_problem_student_vote'),
        ),
    ]