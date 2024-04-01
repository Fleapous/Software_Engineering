from django.urls import path
from .views import AdSpaceList, CreateAdSpace, GetAdSpace, UpdateAdSpace, DeleteAdSpace

urlpatterns = [
    path('get-all-adspaces/', AdSpaceList.as_view(), name='get-all-adspaces'),
    path('create-adspace/', CreateAdSpace.as_view(), name='create-adspace'),
    path('adspace/<int:pk>/', GetAdSpace.as_view(), name='get-adspace'),
    path('adspace/<int:pk>/update/', UpdateAdSpace.as_view(), name='update-adspace'),
    path('adspace/<int:pk>/delete/', DeleteAdSpace.as_view(), name='delete-adspace'),
]
