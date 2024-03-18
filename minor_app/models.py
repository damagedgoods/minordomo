from django.db import models

class Message(models.Model):
    text = models.CharField(max_length=200)
    date = models.DateTimeField("date")
    update_id = models.IntegerField(default=0)

    def __str__(self):
        return "in "+str(self.date)+", "+self.text+" was said"
