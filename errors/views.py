from django.shortcuts import redirect

# Vista para error 404
def custom_page_not_found_view(request, exception):
    return redirect('home')  # Reemplaza 'home' con el nombre de tu vista o URL para el inicio

# Vista para error 500
def custom_server_error_view(request):
    return redirect('home')

# Vista para error 403
def custom_permission_denied_view(request, exception):
    return redirect('home')

# Vista para error 400
def custom_bad_request_view(request, exception):
    return redirect('home')
