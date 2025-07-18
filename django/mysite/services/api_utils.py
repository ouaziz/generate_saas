import random, string
from django.http import JsonResponse
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


# def generate_unique_code(model, field_name, length=10):
#     while True:
#         code = ''.join(random.choices(string.digits, k=length))
#         if not model.objects.filter(**{field_name: code}).exists():
#             return code


def standard_list_view(queryset, serializer_class, request):
    # serializer = serializer_class(queryset, many=True)
    serializer = serializer_class(queryset, many=True, context={'request': request})
    return JsonResponse({
        "status": "success",
        "message": "Data fetched successfully",
        "data": serializer.data,
    }, status=status.HTTP_200_OK)


def standard_create_view(serializer_class, request):
    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        instance = serializer.save(
            user=request.user
        )
        return JsonResponse({
            "status": "success",
            "message": "Created successfully",
            "id": instance.id,
        }, status=status.HTTP_201_CREATED)
    return JsonResponse({
        "status": "error",
        "message": serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)


def standard_get_object(queryset, serializer_class):
    try:
        # obj = model.objects.get(pk=pk)
        serializer = serializer_class(queryset)
        # instance = get_object_or_404(Model, pk=pk)
        return JsonResponse({
            "status": "success",
            "message": "Data fetched successfully",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)
        
    except queryset.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Data not found",
        }, status=status.HTTP_404_NOT_FOUND)


def standard_update_view(model, pk, serializer_class, request):
    try:
        obj = model.objects.get(pk=pk)
        serializer = serializer_class(obj, data=request.data)
        if serializer.is_valid():
            data = serializer.save(
                user=request.user
            )
            return JsonResponse({
                "status": "success",
                "message": "Updated successfully",
                "id": data.id
            }, status=status.HTTP_200_OK)
        return JsonResponse({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except model.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": f"{model.__name__} not found",
        }, status=status.HTTP_404_NOT_FOUND)

def standard_delete_view(model, pk):
    try:
        obj = model.objects.get(pk=pk)
        obj.delete()
        return JsonResponse({
            "status": "success",
            "message": "Deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
    except model.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": f"{model.__name__} not found",
        }, status=status.HTTP_404_NOT_FOUND)