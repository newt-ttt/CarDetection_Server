from django.db import models

# Create your models here.

class SpeedInstance(models.Model):
    def __str__(self):
        return str(self.id)
    true_date = models.DateTimeField("true_date")
    recorded_at= models.CharField(max_length=32)
    speed = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    direction = models.IntegerField(default=0)
    custom_text = models.CharField(max_length=200)