from django.urls import path
import stateAPI.views

urlpatterns = [
    path('state/<uuid:cir_id', CircuitView.as_view()),
    path('othercircuits/<str:state>', GetCircuit.as_view()),
    path('role/', GetUserType.as_view())
]
