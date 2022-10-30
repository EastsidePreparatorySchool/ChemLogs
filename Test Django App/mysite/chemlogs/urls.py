from django.urls import path

from . import views

app_name = 'chemlogs'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('testPage/<int:chemical_id>/', views.testPage, name='testPage'),
    path('testPage2/<int:chemical_id>/', views.testPage2, name='testPage2'),
    path('testChem/<int:chemical_id>/', views.testChem, name='testChem'),
    path('chemical/<int:chemical_id>/', views.chemical, name='chemical'), # note chemical_id is the database-given id, not cas
    path('chemicalSearch/', views.ChemicalSearch.as_view(), name='chemicalSearch')
]