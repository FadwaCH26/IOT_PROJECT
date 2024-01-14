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
                            <title>🔔Alerte de Temperature</title>
                        </head>
                        <body>
                            <h2>température dépasse la normale</h2>
                            <p>🔥The temperature has exceeded the normal range:</p>
                            <p>Temperature Value: {self.temp}</p>
                            <p>⏰ Anomaly detected in the machine at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                        </body>
                        </html>
                    '''
            plain_message = strip_tags(html_message)
            send_mail(
                'température dépasse la normale,' + str(self.temp),
                plain_message,
                'fadwacharai26@gmail.com',
                ['fadwacharai8@gmail.com','israechourak8@gmail.com'],
                fail_silently=False,
            )
        return super().save(*args, **kwargs)