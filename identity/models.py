from django.db import models

class Contact(models.Model):
   """
   Contact model
   """
   phone_number = models.CharField(max_length=20, null=True, blank=True)
   email = models.EmailField(max_length=50, null=True, blank=True)
   linked_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
   LINK_PRECEDENCE_CHOICES = [
       ("primary", "primary"),
       ("secondary", "secondary")
   ]
   link_precedence = models.CharField(
       max_length=10,
       choices=LINK_PRECEDENCE_CHOICES,
       default="primary"
   )
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   deleted_at = models.DateTimeField(null = True)
