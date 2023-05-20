from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import cx_Oracle
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Traitement , TraitementTable
from django.core import serializers
from django.http import JsonResponse
from addDatabase.models import Database
from AddSchema.models import Schema
#       @csrf_exempt
@api_view(['GET', 'POST'])
def copy_data(request):
    print(request)
    if(request.method == 'GET'):
        print(request.GET)
    if(request.method == 'POST'):
        print(type(request.body))
        data_in_bytes = request.body
        my_json = data_in_bytes.decode('utf8')
        print(my_json)
        data = json.loads(my_json)
        print(data)
        """table = data['tables'][0]['name']
        colones = data['tables'][0]['colones']
        print(type(data['tables']))
        print(table)
        column_names = ', '.join(colones)
        where_clause = data['tables'][0]['whereclause']
        column = f"{where_clause[0]['colone']} {where_clause[0]['op']} {where_clause[0]['value']}"
        sqlquery=f"Select {column_names} From {table} Where {column}"
        print(sqlquery)"""
    """
    connection = cx_Oracle.connect('root/root@172.17.0.2:1521/ORCLCDB')
    target_connection = cx_Oracle.connect('root/root@172.17.0.3:1521/ORCLCDB')
    curr = connection.cursor()
    target_curr = target_connection.cursor()
    curr.execute(sqlquery)
    results = curr.fetchall()
    # Print the results
    for row in results:
        print(row)
        target_curr.execute(f"INSERT INTO {table} ({column_names}) VALUES {row}")
        print(f"INSERT INTO {table} ({column_names}) VALUES {row}")
        target_connection.commit();

    # Close the cursor and database connection
    curr.close()
    target_curr.close()
    connection.close()
    target_connection.close()"""
    return JsonResponse({"message": "Data copied successfully"})

        
# urls.py






@api_view(['GET'])
def show_all_traitement(request):
    unserialized_data = Traitement.objects.all()
    data = serializers.serialize('json', unserialized_data,use_natural_foreign_keys=True)
    return JsonResponse(data, safe=False)



@api_view(['GET'])
def show_traitement(request,item_id):
    unserialized_data = Traitement.objects.get(pk=item_id)
    data = serializers.serialize('json', [unserialized_data,])
    return JsonResponse(data, safe=False)


@api_view(['GET'])
def show_all_traitement_names(request):
    traitement_names = list(Traitement.objects.values_list('traitement_name', 'id'))
    
    return JsonResponse({'trait_names': traitement_names})




@api_view(['GET'])
def get_traitements(request):
    unserialized_data = Traitement.objects.all()
    data = serializers.serialize('json', unserialized_data)
    return JsonResponse(data, safe=False)


@api_view(['DELETE'])
def delete_Trait_id(request ,id):
    target = Traitement.objects.get(pk=id)
    target.delete()
    return JsonResponse({"message":"treatement Deleted"})


@api_view(['GET'])
def get_traitementsTable(request , id ):
    unserialized_data = TraitementTable.objects.filter(traitement=id)
    data = serializers.serialize('json', unserialized_data)
    return JsonResponse(data, safe=False)

@api_view(['DELETE'])
def delete_Trait(request ,item_id):
    target = TraitementTable.objects.get(pk=item_id)
    target.delete()
    return JsonResponse({"message":"Deleted"})

@api_view(['POST'])
def add_to_traitementTable(request):
    data = json.loads(request.body.decode('utf8'))
    print(data)
    trait_instance = Traitement.objects.get(id=data['traitement'])
    newTrait = TraitementTable(table_name=data['table_name'],Columns=data['columns'],Filter=data['filter'],traitement=trait_instance)
    newTrait.save()
    return JsonResponse(data, safe=False)

@api_view(['POST'])
def add_traitement(request):
    data = json.loads(request.body.decode('utf8'))
    print(data)
    schema_instance = Schema.objects.get(id=data['schema'])
    newTrait = Traitement(name=data['name'],schema=schema_instance)
    newTrait.save()
    return JsonResponse({"message":"Added   "})

@api_view(['POST'])
def execute_traitement(request):
    data = json.loads(request.body.decode('utf8'))
    print(data)
    related_queries = TraitementTable.objects.filter(traitement=data['traitement'])
    source_db = Database.objects.get(id=data['env_source'])
    target_db = Database.objects.get(id=data['env_target'])
    print(source_db.connect_string())
    print(target_db.connect_string())
    for i in related_queries :
        Columns = ', '.join(i.Columns)
        Table = i.table_name
        if i.Filter != None and i.Filter:
            Filters = ' '.join(i.Filter)
            SqlRequest = f"Select {Columns} From {Table} Where {Filters}"
            print(SqlRequest)
        else:
            SqlRequest = f"Select {Columns} From {Table}"
            print(SqlRequest)
        connection = cx_Oracle.connect(source_db.connect_string())
        target_connection = cx_Oracle.connect(target_db.connect_string())
        curr = connection.cursor()
        target_curr = target_connection.cursor()
        curr.execute(SqlRequest)
        results = curr.fetchall()
        for row in results:
            print(row)
            print(f"INSERT INTO {Table} ({Columns}) VALUES {row}")
            if Columns != "*":
                target_curr.execute(f"INSERT INTO {Table} ({Columns}) VALUES {row}")
            else:
                target_curr.execute(f"INSERT INTO {Table} VALUES {row}")
            target_connection.commit()
        curr.close()
        target_curr.close()
        connection.close()
        target_connection.close()

    return JsonResponse({"message": "test"})