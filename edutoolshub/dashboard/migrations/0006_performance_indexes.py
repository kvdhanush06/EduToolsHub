from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0005_alter_notes_options"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="homework",
            index=models.Index(
                fields=["user", "due"],
                name="dashboard_hw_user_due_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="homework",
            index=models.Index(
                fields=["user", "is_finished", "due"],
                name="dashboard_hw_user_done_due_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="todo",
            index=models.Index(
                fields=["user", "is_finished"],
                name="dashboard_todo_user_done_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="notes",
            index=models.Index(
                fields=["user"],
                name="dashboard_notes_user_idx",
            ),
        ),
    ]
