from django.urls import path
from . import views
from . import api
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path("api",api.Dlist,name='json'),
    path("api/post",api.Dlist,name='json'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('index/',views.table,name='index'),
    path('myChartTemp/',views.graphiqueTemp,name='myChartTemp'),
    path('myChartHum/', views.graphiqueHum, name='myChartHum'),
    path('chart-data/', views.chart_data, name='chart-data'),
    path('authen/', auth_views.LoginView.as_view(template_name='authen.html'), name='authen'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('table/', views.table, name='table'),
    path('chart-data-jour/',views.chart_data_jour,name='chart-data-jour'),
    path('chart-data-semaine/',views.chart_data_semaine,name='chart-data-semaine'),
    path('chart-data-mois/',views.chart_data_mois,name='chart-data-mois'),
    path('', views.home, name='home'),
    path('incidents/', views.incidents_view, name='incidents'),
     path('incidents/json/', views.incidents_to_json, name='incidents_json'),
    path('gestion_utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('manage-admins/', views.manage_admins, name='manage_admins'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sensors/api/sensor-data/', api.Dlist, name='dlist')
   

]