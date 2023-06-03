from django.db import models

class Contact(models.Model):
   phone_number = models.CharField(max_length=20, null=True)
   email = models.EmailField(max_length=50, null=True)
   linked_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
   PRIMARY = "PRI"
   SECONDARY = "SEC"
   LINK_PRECEDENCE_CHOICES = [
       (PRIMARY, "primary"),
       (SECONDARY, "secondary")
   ]
   link_precedence = models.CharField(
       max_length=3,
       choices=LINK_PRECEDENCE_CHOICES,
       default=PRIMARY
   )
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   deleted_at = models.DateTimeField(null = True)
