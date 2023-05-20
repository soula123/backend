

#imports
from rest_framework.decorators import api_view
import cx_Oracle
import json
from django.http import JsonResponse
from .models import Database
from django.core import serializers
from AddSchema.models import  Schema  
from django.shortcuts import get_object_or_404, redirect

@api_view(['GET', 'POST'])
def addDb(request):
    if(request.method=='POST'):
        data_in_bytes = request.body
        my_json = data_in_bytes.decode('utf8')
        data = json.loads(my_json)  
        print(data)
        schema = Schema.objects.get(schema_name=data['schema'])
        database_instance = Database(user=data['user'], password=data['password'], dsn=data['DSN'], schema=schema, name=data['name'])
        database_instance.save()
    return JsonResponse({"message":"there is a schema with the same name ! try changning the name !"})


@api_view(['POST'])
def duplicate_row(request, id):
    # Get the original object to duplicate
    original_obj = get_object_or_404(Database, id=id)

    schema = Schema.objects.get(schema_name=original_obj.schema)
    # Create a new object with the same attributes as the original
    new_obj = Database(user=original_obj.user, password=original_obj.password , dsn=original_obj.dsn , schema=schema, name=original_obj.name + "- Copy")
    #new_obj = Database(**original_obj.__dict__)
    #  new_obj.id = None  # Set the ID to None to create a new row in the database
    new_obj.save()

    # Redirect to the detail view of the new object
    return JsonResponse({"message":" Successfully"})

@api_view(['GET', 'POST'])
def test_connection(request, id):
    if request.method == 'POST':
        # Get the data from the request body
       
        data = json.loads(request.body)
        
        # Retrieve database connection data using the given id
        db = Database.objects.get(id=id)
        user = db.user
        password = db.password
        dsn = db.dsn

        try:
            connection = cx_Oracle.connect(f"{user}/{password}@{dsn}")
        except cx_Oracle.DatabaseError:
            return JsonResponse({"message":"not connected"})
        else:
            return JsonResponse({"message":"connected"})

@api_view(['GET'])
def read_all_data(request):
        unserialized_data = Database.objects.all()
        data = serializers.serialize('json', unserialized_data , use_natural_foreign_keys=True)
        return JsonResponse(data, safe=False)
@api_view(['DELETE'])
def delete_env(request ,item_id):
    target = Database.objects.get(pk=item_id)
    target.delete()
    return JsonResponse({"message":"Deleted"})
@api_view(['POST'])
def delete_multiple(request):
    item_list = request.body.decode('utf8')
    item_list = item_list[1:-1].split(",")
    item_list = list(map(int, item_list))
    print(item_list)
    for item in item_list:
        target = Database.objects.get(pk=item)
        target.delete()
    return JsonResponse({"message":"deleted items"})

@api_view(['GET'])
def show_Env(request):
    unserialized_data = Database.objects.all()
    data = serializers.serialize('json', unserialized_data)
    return JsonResponse(data, safe=False)
@api_view(['GET'])
def show_one_env(request,item_id):
    target = Database.objects.get(pk=item_id)
    data = serializers.serialize('json', [target,])
    return JsonResponse(data, safe=False)


@api_view(['POST'])
def edit_env(request,item_id):
    data = json.loads(request.body.decode('utf8'))
    schema = Schema.objects.get(schema_name=data['schema'])
    target = Database.objects.get(pk=item_id)
    target.name = data['name']
    target.user = data['user']
    target.password = data['password']
    target.dsn = data['DSN']
    target.schema = schema
    target.save()
    
    return JsonResponse(data, safe=False)
