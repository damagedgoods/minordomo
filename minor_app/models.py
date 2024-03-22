from django.db import models
from django.utils.text import slugify

class Message(models.Model):
    text = models.CharField(max_length=200)
    date = models.DateTimeField("date")
    update_id = models.IntegerField(default=0)
    read_status = models.BooleanField(default=False)
    slug = models.SlugField(default="")

    def __str__(self):
        return "in "+str(self.date)+", "+self.text+" was said"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.text)
        super(Message, self).save(*args, **kwargs)    
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})  # new        

class Report(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.message.text +" "+self.content