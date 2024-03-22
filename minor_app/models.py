from django.db import models

class Message(models.Model):
    text = models.CharField(max_length=200)
    date = models.DateTimeField("date")
    update_id = models.IntegerField(default=0)
    read_status = models.BooleanField(default=False)

    def __str__(self):
        return "in "+str(self.date)+", "+self.text+" was said"

class Report(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.message.text +" "+self.content