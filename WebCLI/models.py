from django.db import models
from django.contrib.auth.models import User


class Algorithm_type(models.Model):
    type_name = models.TextField()

    def __str__(self):
        return self.type_name


class Molecule(models.Model):
    name = models.TextField()
    structure = models.TextField()

    def __str__(self):
        return self.name


class Algorithm(models.Model):
    name = models.TextField()
    public = models.BooleanField()
    molecule = models.ForeignKey(Molecule, on_delete=models.CASCADE)
    algorithm_type = models.ForeignKey(Algorithm_type, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article_link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('algorithm_details', args=[str(self.pk)])

    def __str__(self):
        return self.name

class Algorithm_version(models.Model):
    algorithm_id = models.ForeignKey(Algorithm, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField()
    algorithm = models.TextField()
    iterations = models.IntegerField(null=True)
    measurements = models.IntegerField(null=True)
    circuit_depth = models.IntegerField(null=True)
    accuracy = models.FloatField(null=True)