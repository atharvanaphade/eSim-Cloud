from django.urls import path
from stateAPI import views

urlpatterns = [
    path('state/<uuid:cir_id', views.CircuitView.as_view()),
    path('othercircuits/<str:state>', views.GetCircuit.as_view()),
    path('role/', views.GetUserType.as_view())
]
