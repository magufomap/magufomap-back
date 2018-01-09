from django.db import models


class Comment(models.Model):
    owner = models.ForeignKey("api.User", null=True, on_delete=models.SET_NULL, related_name="comments")
    poim = models.ForeignKey("api.POIM", on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created_date = models.DateTimeField(null=False, blank=True, auto_now_add=True)

    class Meta:
        ordering = ["-created_date", "id"]

    def __str__(self):
        return "{} comentó {} en {}".format(self.owner, self.comment, self.poim)
