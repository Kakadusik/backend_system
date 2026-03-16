from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from access_control.permissions import HasElementPermission

# имитация базы товаров (для демонстрации)
products = [
    {'id': 1, 'name': 'Product 1', 'owner_id': 1},
    {'id': 2, 'name': 'Product 2', 'owner_id': 2},
    {'id': 3, 'name': 'Product 3', 'owner_id': 1},
]

class MockProductListView(APIView):
    """
    Представление для списка товаров
    """


    permission_classes = [HasElementPermission(element_name='product', action='read')]

    def get_permissions(self):
        # для GET-запроса используем permission на чтение
        if self.request.method == 'GET':
            return [HasElementPermission('product', 'read')]
        # для POST-запроса — на создание
        elif self.request.method == 'POST':
            return [HasElementPermission('product', 'create')]
        return super().get_permissions()

    def get(self, request):
        if request.all_flag:
            result = products
        else:
            result = [p for p in products if p['owner_id'] == request.user.id]
        return Response(result)

    def post(self, request):
        perm = HasElementPermission(element_name='product', action='create')
        if not perm.has_permission(request, self):
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        new_id = max(p['id'] for p in products) + 1 if products else 1
        product = {
            'id': new_id,
            'name': request.data.get('name', 'New Product'),
            'owner_id': request.user.id
        }
        products.append(product)
        return Response(product, status=status.HTTP_201_CREATED)

class MockProductDetailView(APIView):
    """
    Представление для товара
    """

    # permission_classes = [HasElementPermission(element_name='product', action='update')]

    def get_permissions(self):
        # в зависимости от метода возвращаем нужный permission
        if self.request.method in ('PUT', 'PATCH'):
            return [HasElementPermission('product', 'update')]
        elif self.request.method == 'DELETE':
            return [HasElementPermission('product', 'delete')]
        elif self.request.method == 'GET':
            return [HasElementPermission('product', 'read')]
        return super().get_permissions()

    def get_object(self, pk):
        for p in products:
            if p['id'] == pk:
                return p
        return None

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        # проверка объекта (владелец или all_flag)
        self.check_object_permissions(request, product)  # вызовет has_object_permission

        product['name'] = request.data.get('name', product['name'])
        return Response(product)

    def delete(self, request, pk):
        # Для delete используем другой permission 
        perm = HasElementPermission(element_name='product', action='delete')
        if not perm.has_permission(request, self):
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        product = self.get_object(pk)
        if not product:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        if not (request.all_flag or product['owner_id'] == request.user.id):
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        products.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)