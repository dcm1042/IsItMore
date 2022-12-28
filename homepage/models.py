from django.db import models

# Create your models here.


class Pairs(models.Model):

    option1 = models.TextField(db_column='Option1', blank=True, null=True)  # Field name made lowercase.
    option2 = models.TextField(db_column='Option2', blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    votes1 = models.IntegerField(db_column='Votes1')  # Field name made lowercase.
    votes2 = models.IntegerField(db_column='Votes2')  # Field name made lowercase.

    class Meta:
        app_label = 'homepage'
        managed = False
        db_table = 'Pairs'
