from django.urls import path

from . import views

app_name = 'chemlogs'
urlpatterns = [
    path('testPage/<int:chemical_id>/', views.testPage, name='testPage'), # unused
    path('chemical/<int:chemical_id>/', views.chemical, name='chemical'),
    path('testChem/<int:chemical_id>/', views.testChem, name='testChem'),
    path('chemicalSearch/', views.ChemicalSearch.as_view(), name='chemicalSearch'),
    path('transaction/<int:transaction_id>/', views.transaction, name='transaction'),
    path('history/', views.history, name='history') # unimplemented
]