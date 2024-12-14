from django.conf.urls import handler404, handler500, handler403, handler400
from errors.views import (
    custom_page_not_found_view,
    custom_server_error_view,
    custom_permission_denied_view,
    custom_bad_request_view,
)

# Asignación de manejadores de errores
handler404 = 'errors.views.custom_page_not_found_view'
handler500 = 'errors.views.custom_server_error_view'
handler403 = 'errors.views.custom_permission_denied_view'
handler400 = 'errors.views.custom_bad_request_view'

# Rutas normales de la aplicación
from django.urls import path, include

urlpatterns = [
    path('', include('yamaha_ideas.urls')),  # Ruta para la app principal
    path('errors/', include('errors.urls')),  # Opcional: rutas específicas de la app errors
]