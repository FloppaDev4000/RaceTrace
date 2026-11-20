from django.db import models

class Race(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    # data fields
    title = models.CharField(max_length=100, blank=True, default="")
    dateRan = models.DateField()
    location = models.CharField(max_length=200, blank=True, default="")
    distanceKm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    # calendar source fields
    source = models.CharField(max_length=100)
    sourceId = models.CharField(max_length=100, blank=True, default="")
    sourceUrl = models.URLField(blank=True, default="")

    # no 2 races should have the same source and ID
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["source", "sourceId"], name="unique_race_per_source")
        ]


class Result(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="results", null=True, blank=True) # need to remove this field

    # source fields
    source = models.CharField(max_length=100, blank=True, default="")
    url = models.URLField()

    # raw scraped
    rawTitle = models.CharField(max_length=200, blank=True, default="")
    rawDate = models.DateField(null=True, blank=True)


class Match(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    # foreign key connections
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="match", null=True, blank=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="match", null=True, blank=True)

    # for manual admin decisions
    score = models.IntegerField()
    explanation = models.CharField(max_length=100, blank=True, default="")

    class Status(models.TextChoices):
        PROPOSED = "proposed"
        CONFIRMED = "confirmed"
        REJECTED = "rejected"

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PROPOSED)
    decidedBy = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)
    decidedAt = models.DateField(null=True, blank=True)

    # no 2 matches may connect same result to same race
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["race", "result"], name="unique_match_pair")
        ]