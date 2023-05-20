from django.db import models

class Schema(models.Model):
    id = models.AutoField(primary_key=True)
    schema_name = models.CharField(max_length=255, unique=True)
    schema_data = models.JSONField()
    description = models.TextField(default='no description')
    def __str__(self):
        return self.schema_name
    def natural_key(self):
        return (self.schema_name,)
    class Meta:
        db_table = 'schema'
        
