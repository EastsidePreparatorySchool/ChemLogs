from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views, updater

app_name = 'chemlogs'
urlpatterns = [
    path('chemical/<int:chemical_id>/', login_required(views.chemical), name='chemical'),
    path('chemicalSearch/', login_required(views.ChemicalSearch.as_view()), name='chemicalSearch'),
    path('transaction/<int:transaction_id>/', login_required(views.transaction), name='transaction'),
    path('container/<str:container_id>/', login_required(views.container), name='container'),
    path('delete_account/<int:user_id>', views.delete_account, name='deleteAccount'),
    path('exportCSV/<int:export_type>/', login_required(views.exportCSV), name='exportCSV'),
    #path('history/', views.history, name='history') # this content is now in chemicalSearch
    # path('testPage/<int:chemical_id>/', login_required(views.testPage), name='testPage'), # unused
    # path('testChem/<int:chemical_id>/', login_required(views.testChem), name='testChem'), # unused
]