from django.http import HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.exceptions import PermissionDenied
from elearning.serializers import *
import json
import os
# Create your views here.


@api_view(['POST'])
def login(request):
    input_data = request.data
    login_id = input_data['id']
    login_password = input_data['password']
    users = User.objects.filter(id=login_id)
    if users.exists():
        user = users[0]
        if user.password == login_password:
            request.session['role'] = user.role
            request.session['id'] = user.id
            serializer = UserSerializer(instance=user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def logout(request):
    try:
        del request.session['id']
        del request.session['role']
    except KeyError:
        pass
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    input_data = request.data
    if 'id' in input_data and 'password' in input_data and 'role' in input_data and 'name' in input_data:
        if input_data['role'] in ['TEACHER','STUDENT']:
            existing_user = User.objects.filter(id=input_data['id'])
            if existing_user.exists():
                return Response(status=status.HTTP_409_CONFLICT)
            user = User(id=input_data['id'],password=input_data['password'],name=input_data['name'],role=input_data['role'])
            user.save()
            return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def tree(request):
    if 'role' not in request.session:
        raise PermissionDenied("login first")
    if request.method == 'GET':
        trees = Tree.objects.all()
        if not trees.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tree = trees[0]
            tree_str = tree.tree
            return Response(data=json.loads(tree_str), status=status.HTTP_200_OK)
    else:
        if request.session['role'] != 'TEACHER':
            raise PermissionDenied('user not teacher')
        input_data = json.dumps(request.data)
        trees = Tree.objects.all()
        if not trees.exists():
            tree = Tree(tree=input_data)
            tree.save()
        else:
            tree = trees[0]
            tree.tree = input_data
            tree.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def set_homework_answer(request):
    input_data = request.data
    if 'node_id' not in input_data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if 'role' not in request.session or 'id' not in request.session:
        raise PermissionDenied('login first')
    if request.session['role'] != 'STUDENT':
        raise PermissionDenied('user not student')
    node_homeworks = NodeHomework.objects.filter(node_id=input_data['node_id'])
    if not node_homeworks.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    node_homework = node_homeworks[0]
    input_data['node_homework'] = node_homework.id
    input_data['student'] = request.session['id']
    serializer = HomeworkAnswerSerializer(data=input_data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        msg = serializer.errors
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_homework_answer(request,node_id):
    if 'role' not in request.session or 'id' not in request.session:
        raise PermissionDenied('login first')
    if request.session['role'] != 'STUDENT':
        raise PermissionDenied('user not student')
    node_homeworks = NodeHomework.objects.filter(node_id=node_id)
    if not node_homeworks.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    node_homework = node_homeworks[0]
    node_homeworkanswers = HomeworkAnswer.objects.filter(node_homework=node_homework).filter(student=request.session['id'])
    if not node_homeworkanswers.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    node_homeworkanswer = node_homeworkanswers[0]
    serializer = HomeworkAnswerSerializer(instance=node_homeworkanswer)
    result_data = serializer.data
    result_data.pop('student',None)
    result_data.pop('node_homework',None)
    return Response(result_data,status=status.HTTP_200_OK)


@api_view(['POST'])
def set_homework(request):
    input_data = request.data
    if 'node_id' not in input_data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if 'role' not in request.session or 'id' not in request.session:
        raise PermissionDenied('login first')
    if request.session['role'] != 'TEACHER':
        raise PermissionDenied('user not teacher')
    node_homeworks = NodeHomework.objects.filter(node_id=input_data['node_id'])
    if node_homeworks.exists():
        node_homeworks[0].delete()
    order = 0
    for question in input_data['questions']:
        question['order'] = order
        order = order + 1
    serializer = NodeHomeworkSerializer(data=input_data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_homework(request,node_id):
    if 'role' not in request.session or 'id' not in request.session:
        raise PermissionDenied('login first')
    node_homeworks = NodeHomework.objects.filter(node_id=node_id)
    if not node_homeworks.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    node_homework = node_homeworks[0]
    serializer = NodeHomeworkSerializer(instance=node_homework)
    result_data = serializer.data
    result_data['questions'] = sorted(result_data['questions'],key = lambda k:k['order'])
    return Response(result_data,status=status.HTTP_200_OK)


@api_view(['GET'])
def download_material(request,material_id):
    if 'role' not in request.session or 'id' not in request.session:
        raise PermissionDenied('login first')
    materials = Material.objects.filter(id=material_id)
    if materials.exists():
        material = materials[0]
        response = HttpResponse(status=status.HTTP_200_OK)
        full_path = os.path.join('', str(material.material_file))
        filename, file_extension = os.path.splitext(full_path)
        response['Content-Disposition'] = 'attachment;filename=' + material.material_name + file_extension
        if os.path.exists(full_path):
            response['Content-Length'] = os.path.getsize(full_path)
            content = open(full_path, 'rb').read()
            response.write(content)
            return response
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_materials(request,node_id):
    if 'role' not in request.session or 'id' not in request.session:
        raise PermissionDenied('login first')
    node_materials = NodeMaterial.objects.filter(node_id=node_id)
    if not node_materials.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    node_material = node_materials[0]
    serializer = NodeMaterialSerializer(instance=node_material)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['POST'])
def create_material(request):
    input_data = request.data
    if 'node_id' not in input_data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if 'role' not in request.session or 'id' not in request.session:
        raise PermissionDenied('login first')
    if request.session['role'] != 'TEACHER':
        raise PermissionDenied('user not teacher')
    node_materials = NodeMaterial.objects.filter(node_id=input_data['node_id'])
    if not node_materials.exists():
        node_material = NodeMaterial(node_id=input_data['node_id'])
    else:
        node_material = node_materials[0]
    node_material.save()
    material_name = input_data['material_name']
    material = Material(material_name=material_name,node_material=node_material)
    material.save()
    return Response(status=status.HTTP_201_CREATED)


# @api_view(['PUT'])
# @parser_classes(['FileUploadParser'])
# def upload_material(request,material_id):
#     if 'role' not in request.session or 'id' not in request.session:
#         raise PermissionDenied('login first')
#     if request.session['role'] != 'TEACHER':
#         raise PermissionDenied('user not teacher')
#     material = Material.objects.filter(id=material_id)
#     if not material.exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     material = material[0]
#     upload_file = request.FILES['file']
#     pass
#     material.material_file = upload_file
#     return Response(status=status.HTTP_200_OK)
