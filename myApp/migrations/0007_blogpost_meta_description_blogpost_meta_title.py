from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0006_alter_painpointssection_cta_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='meta_title',
            field=models.CharField(blank=True, help_text='SEO title for search engines (leave blank to use post title)', max_length=70),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='meta_description',
            field=models.CharField(blank=True, help_text='SEO description for search engines (leave blank to use excerpt)', max_length=160),
        ),
    ]
