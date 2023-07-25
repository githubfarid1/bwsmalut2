from django.db import models
# Create your models here.
class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    defcode = models.CharField(max_length=20, unique=True)
    link = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name
    
class Bundle(models.Model):
    id = models.IntegerField(primary_key=True)
    box_number = models.SmallIntegerField()
    bundle_number = models.SmallIntegerField()
    code = models.CharField(max_length=20)
    title = models.TextField()
    year = models.CharField(max_length=4)
    orinot = models.CharField(max_length=10)
    description = models.CharField(max_length=255)

    department = models.ForeignKey(
        Department,
        db_column='department_id',
        on_delete=models.CASCADE,
        related_name="bundles"
    )        
    def __str__(self) -> str:
        return f'{self.box_number}_{self.bundle_number}'

class Doc(models.Model):
    id = models.IntegerField(primary_key=True)
    doc_number = models.SmallIntegerField()
    doc_count = models.SmallIntegerField()
    orinot = models.CharField(max_length=10)
    doc_type = models.CharField(max_length=20)
    description = models.TextField()
    filesize = models.IntegerField()
    page_count = models.SmallIntegerField()

    bundle = models.ForeignKey(
        Bundle,
        db_column='bundle_id',
        on_delete=models.CASCADE, 
        related_name='docs'
    )        
