


#imports
from rest_framework.decorators import api_view
import cx_Oracle
import json
from django.http import JsonResponse
from AddSchema.models import Schema
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .models import Schema
from django.core import serializers


@api_view(['GET', 'POST'])
def add_scheme(request):
    if (request.method=='POST'):
        print(request)
        data_in_bytes = request.body
        my_json = data_in_bytes.decode('utf8')
        data = json.loads(my_json)
        print(data)
        #after retrieving database connection data , the data is saved in variables
        user = data['user']
        password = data['password']
        dsn = data['DSN']
        name =  data['name']
        #connecting with the retrieved data
        connection = cx_Oracle.connect(f"{user}/{password}@{dsn}")
        # Get the schema information using a cursor
        cursor = connection.cursor()
        cursor.execute("""
            SELECT table_name, column_name, data_type
            FROM all_tab_columns
            WHERE owner = :owner
            ORDER BY table_name, column_id
            """, owner=f"{user}".upper())

        # Build the schema dictionary   
        schema = {}
        for table_name, column_name, data_type in cursor:
            if table_name not in schema:
                schema[table_name] = []
            schema[table_name].append((column_name, data_type))
        # Create a new Schema object
        if 'description' in data :
            description = data['description']
            new_schema = Schema(schema_name=name, schema_data=schema , description=description)
        else :
            new_schema = Schema(schema_name=name, schema_data=schema)
        # Save the object to the database
        try:
            new_schema.save()
        except IntegrityError:
            return JsonResponse({"message":"there is a schema with the same name ! try changning the name !"})

        
    #return the schema
    return JsonResponse({"message":"Added !!"})

@api_view(['GET'])
def show_all_schema(request):
    unserialized_data = Schema.objects.all()
    data = serializers.serialize('json', unserialized_data)
    return JsonResponse(data, safe=False)
   # schema_names = list(Schema.objects.values_list('schema_name', 'id'))
   # print(JsonResponse({'schema_names': schema_names}))
   # return JsonResponse({'schema_names': schema_names})
@api_view(['GET'])
def show_schema(request,item_id):
    unserialized_data = Schema.objects.get(pk=item_id)
    data = serializers.serialize('json', [unserialized_data,])
    return JsonResponse(data, safe=False)
@api_view(['GET'])
def show_all_schema_names(request):
    schema_names = list(Schema.objects.values_list('schema_name', 'id'))
    print(JsonResponse({'schema_names': schema_names}))
    return JsonResponse({'schema_names': schema_names})

@api_view(['PUT'])
def update_schema(request):
    data_in_bytes = request.body
    my_json = data_in_bytes.decode('utf8')
    data = json.loads(my_json)
    print(data)
    ids = list(Schema.objects.values_list('id','schema_name'))
    #target = Schema.objects.get(id = data['id'])
    #target.schema_name = data['new_name']
    #target.save()
    print(ids)
    return JsonResponse({"message":"there is a schema with the same name ! try changning the name !"})
@api_view(['DELETE'])
def delete_schema(request ,item_id):
    """data_in_bytes = request.body
    my_json = data_in_bytes.decode('utf8')
    data = json.loads(my_json)
    print(data)
    target = Schema.objects.get(id = data['id'])
    target.delete()"""
    target = Schema.objects.get(pk=item_id)
    target.delete()
    return JsonResponse({"message":"Deleted"})
@api_view(['POST'])
def delete_items(request):
    item_list = request.body.decode('utf8')
    item_list = item_list[1:-1].split(",")
    item_list = list(map(int, item_list))
    print(item_list)
    for item in item_list:
        target = Schema.objects.get(pk=item)
        target.delete()
    return JsonResponse({"message":"Deleted"})

@api_view(['POST'])
def edit_schema(request,item_id):
    data = json.loads(request.body.decode('utf8'))
    
    schema = Schema.objects.get(pk=item_id)
    schema.schema_name = data['name']
    schema.description = data['description']
    
    schema.save()
    print(data)
    return JsonResponse(data, safe=False)