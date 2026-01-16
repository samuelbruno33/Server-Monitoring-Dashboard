from django.db import models

class Server(models.Model):
    # Server identification
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    owner = models.CharField(max_length=100)
    
    ports_to_check = models.CharField(max_length=200, blank=True, null=True)

    # Status fields
    is_online = models.BooleanField(default=False)
    last_checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Displays the name in the Admin panel
        return f"{self.name} ({self.ip_address})"