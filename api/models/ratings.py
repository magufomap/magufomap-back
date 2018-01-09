from django.db import models

from api.choices import ratings as choices


class Rating(models.Model):
    owner = models.ForeignKey("api.User", null=True, on_delete=models.SET_NULL, related_name="ratings")
    poim = models.ForeignKey("api.POIM", on_delete=models.CASCADE, related_name="ratings")
    vote = models.IntegerField(choices=choices.VOTES, null=False)

    class Meta:
        unique_together = ("owner", "poim")

    def __str__(self):
        return "{} votó {} en {}".format(self.owner, self.vote, self.poim)
