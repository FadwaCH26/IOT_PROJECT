from django.core.mail import send_mail
from django.db import models
from datetime import datetime
# Create your models here.
from django.db import models
from django.utils.html import strip_tags
class Dht11(models.Model):
    temp = models.FloatField(null=True)
    hum = models.FloatField(null=True)
    dt = models.DateTimeField(auto_now_add=True,null=False)

    def __str__(self):
        return str(self.temp)

    def save(self, *args, **kwargs):
        if self.temp > 30:
            from DHT.views import sendtele,sendwhatsap
            sendtele(self)
            sendwhatsap()
            # Inline HTML template enclosed in single quotes
            html_message = f'''
                        <html>
                        <head>
                            <title>🚨 Urgent Alert: Temperature Abnormality Detected! 🚨</title>
                        </head>
                        <body>
                            <p>️🌡️ Current Temperature : {self.temp}</p>
                            <p>⏰ Anomaly detected in the machine at : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                        </body>
                        </html>
                    '''
            plain_message = strip_tags(html_message)
            send_mail(
                'temperature is above normal : ' + str(self.temp),
                plain_message,
                'fadwacharai26@gmail.com',
                ['fadwacharai8@gmail.com','IsraeChourak51@gmail.com '],
                fail_silently=False,
            )
        return super().save(*args, **kwargs)