from django.db import models

class Config(models.Model):
    refresh_seconds = models.IntegerField(default=30, verbose_name="Intervallo di aggiornamento in secondi")

    def __str__(self):
        return f"Configurazione intervallo di aggiornamento di {self.refresh_seconds} s"

    class Meta:
        verbose_name = "Configuration"


class Server(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    owner = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"


# Services associated to a server and checked by port
class Service(models.Model):
    SERVICE_TYPES = [
        ('CUSTOM', '--- Manuale ---'),
        ('HTTP', 'HTTP - 80'),
        ('HTTPS', 'HTTPS - 443'),
        ('FTP', 'FTP - 21'),
        ('DNS', 'DNS - 53'),
        ('SSH', 'SSH - 22'),
    ]

    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='services')
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPES, default='CUSTOM', verbose_name="Tipo Servizio")

    name = models.CharField(max_length=20, blank=True, verbose_name="Nome Servizio")
    port = models.IntegerField(blank=True, null=True, verbose_name="Porta")

    def save(self, *args, **kwargs):
        predefined = {
            'HTTP': ('HTTP', 80),
            'HTTPS': ('HTTPS', 443),
            'FTP': ('FTP', 21),
            'DNS': ('DNS', 53),
            'SSH': ('SSH', 22),
        }

        if self.service_type in predefined:
            self.name, self.port = predefined[self.service_type]

        if self.service_type == 'CUSTOM':
            if not self.name:
                self.name = 'Custom'
            if not self.port:
                self.port = 0

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} ({self.port})"