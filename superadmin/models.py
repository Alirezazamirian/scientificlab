from django.db import models
from utils.models import GeneralDateModel
from detail_app.models import Ticket


class AdminTicket(GeneralDateModel):
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name='Description')
    status = models.BooleanField(default=True, verbose_name='Status')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='Ticket')

    class Meta:
        verbose_name = 'Admin Ticket'
        verbose_name_plural = 'Admin Ticket'

    def __str__(self):
        return self.ticket.title
