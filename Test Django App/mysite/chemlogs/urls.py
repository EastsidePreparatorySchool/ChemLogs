from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views, updater

app_name = 'chemlogs'
urlpatterns = [
    path('testPage/<int:chemical_id>/', login_required(views.testPage), name='testPage'), # unused
    path('chemical/<int:chemical_id>/', views.chemical, name='chemical'),
    path('testChem/<int:chemical_id>/', login_required(views.testChem), name='testChem'),
    path('chemicalSearch/', views.ChemicalSearch.as_view(), name='chemicalSearch'),
    path('transaction/<int:transaction_id>/', views.transaction, name='transaction'),
    path('container/<str:container_id>/', views.container, name='container'),
    #path('history/', views.history, name='history') # this content is now in chemicalSearch
]