from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swapfood.room', related_name='messages')),
            ],
        ),
        migrations.CreateModel(
            name='FoodPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='food_photos/')),
                ('latitude', models.FloatField(null=True, blank=True)),  
                ('longitude', models.FloatField(null=True, blank=True)),  
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),  
                ('location', models.CharField(max_length=255)),  
                ('radius', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),

                # Added user field as a ForeignKey
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,  # Deletes FoodPosts if the user is deleted
                    to=settings.AUTH_USER_MODEL,  
                    related_name='food_posts'  # Allows querying food posts by user
                )),
            ],
        ),
        migrations.CreateModel(
            name='UserOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
