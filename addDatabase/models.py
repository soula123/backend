from django.db import models
from AddSchema.models import  Schema  
import cx_Oracle
# Create your models here.
class Database(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    dsn = models.CharField(max_length=150 ,default=None)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    name = models.CharField(max_length=50 , unique=True)

    def connect_string(self):
        return (f'{self.user}/{self.password}@{self.dsn}')
       
        
    def __str__(self):
        return self.name
    class Meta:
        db_table='databases'