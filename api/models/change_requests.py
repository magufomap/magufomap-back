from django.db import models

from api.choices import change_requests as choices


class ChangeRequest(models.Model):
    owner = models.ForeignKey("api.User", null=True, on_delete=models.SET_NULL, related_name="change_requests")
    poim = models.ForeignKey("api.POIM", on_delete=models.CASCADE, related_name="change_requests")
    change = models.TextField()
    status = models.CharField(max_length=3, null=False, choices=choices.STATUSES, default=choices.PENDING)
    created_date = models.DateTimeField(null=False, blank=True, auto_now_add=True)

    class Meta:
        ordering = ["-created_date", "id"]

    def __str__(self):
        return "{} propuso el cambio [ {} ] en {} [Estado {}]".format(self.owner, self.change, self.poim, self.status)
