from django.urls import path
from . import views
from . import api
from twilio.rest import Client
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("api",api.Dlist,name='json'),
    path("api/post",api.Dhtviews.as_view(),name='json'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('index/',views.table,name='table'),
    path('myChart/',views.graphique,name='myChart'),
    path ('chart-data/',views.chart_data, name='chart-data'),
    path('chart-data-jour/',views.chart_data_jour,name='chart-data-jour'),
    path('chart-data-semaine/',views.chart_data_semaine,name='chart-data-semaine'),
    path('chart-data-mois/',views.chart_data_mois,name='chart-data-mois'),

    path('home/',views.index,name='home'),
    path('tempbyday/',views.tempbyday,name='TempByDay'),
    path('tempbyweek/',views.tempbyweek,name='TempByWeek'),
    path('tempbymonth/',views.tempbymonth,name='TempByMonth'),

    path('humbyday/',views.humbyday,name='HumByDay'),
    path('humbyweek/',views.humbyweek,name='HumByWeek'),
    path('humbymonth/',views.humbymonth,name='HumByMonth'),
    path('showdata/',views.showdata,name='ShowData'),

    path('', views.index, name='home'),
    path('accounts/login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
