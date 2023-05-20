from django.db import models
from AddSchema.models import  Schema    

# Create your models here.
class Traitement(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Traitement'
    
class TraitementTable(models.Model):
    id = models.AutoField(primary_key=True)
    advanced = models.BooleanField(default=False)
    table_name = models.CharField(max_length=255)
    Columns = models.JSONField()
    Filter = models.JSONField(null=True, blank=True, default=None)
    traitement = models.ForeignKey(Traitement, on_delete=models.CASCADE)
    AdvancedQuery = models.CharField(max_length=255 ,null=True, blank=True)
    def __str__(self):
        return self.table_name
    class Meta:
        db_table = 'TraitementTable'
        