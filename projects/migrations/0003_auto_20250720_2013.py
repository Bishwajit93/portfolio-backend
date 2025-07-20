from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20250720_2011'),
        ('auth', '0012_alter_user_first_name_max_length'),  # your 'auth' migration number may vary
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='experiences',
                to='auth.user'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skill',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='skills',
                to='auth.user'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='projects',
                to='auth.user'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='education',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='educations',
                to='auth.user'
            ),
            preserve_default=False,
        ),
    ]
