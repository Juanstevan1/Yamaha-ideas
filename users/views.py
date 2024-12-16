from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from ideas.models import Idea, Program
from notifications.models import Notification
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib.messages import get_messages

@login_required
def dashboard_view(request):
    # Obtener roles del usuario desde el perfil
    roles = request.user.profile.roles.values_list('name', flat=True)

    # Calcular indicadores generales
    ideas = Idea.objects.filter(employee=request.user)

    # Contar estados
    pending_ideas = ideas.filter(state='pending').count()
    reviewed_ideas = ideas.filter(state='reviewed_by_coordinator').count()
    committee_approved = ideas.filter(state='committee_approved').count()
    rejected_ideas = ideas.filter(state__in=['coordinator_rejected', 'committee_rejected', 'sponsor_rejected']).count()
    in_progress_ideas = ideas.filter(state='in_progress').count()
    completed_ideas = ideas.filter(state='completed').count()

    # Promedio de calificaciones del comité
    committee_ratings = ideas.filter(ratings__isnull=False).aggregate(avg_rating=Avg('ratings__rating'))['avg_rating'] or 0

    # Equipos asignados
    assigned_teams = ideas.filter(team__isnull=False).distinct().count()

    # Última idea propuesta
    last_idea = ideas.order_by('-creation_date').first()

    # Notificaciones no leídas
    unread_notifications = list(Notification.objects.filter(user=request.user, read=False))

    # Datos personalizados del usuario para el template
    user_data = {
        'name': request.user.get_full_name() or request.user.username,
        'email': request.user.email,
        'roles': list(roles),
        'ideas_count': ideas.count(),
        'last_idea_title': last_idea.title if last_idea else 'N/A',
        'pending_ideas': pending_ideas,
        'reviewed_ideas': reviewed_ideas,
        'approved_ideas': committee_approved,
        'rejected_ideas': rejected_ideas,
        'in_progress_ideas': in_progress_ideas,
        'completed_ideas': completed_ideas,
        'committee_ratings': round(committee_ratings, 1),
        'assigned_teams': assigned_teams,
        'notifications': unread_notifications,
    }

    # Opciones por rol
    role_actions = {
        'Empleado': [
            {'label': 'Registrar Idea', 'url': '/ideas/select-program', 'icon': 'fas fa-lightbulb', 'btn_class': 'btn-danger'},
            {'label': 'Mis Ideas', 'url': '/ideas/my-ideas', 'icon': 'fas fa-list', 'btn_class': 'btn-primary'},
        ],
        'Coordinador': [
            {'label': 'Revisar Ideas por empleados', 'url': '/ideas/coordinator/review', 'icon': 'fas fa-user-check', 'btn_class': 'btn-warning'},
            {'label': 'Revisar Ideas aprobadas por comité', 'url': '/ideas/coordinator/assign_team/', 'icon': 'fas fa-users', 'btn_class': 'btn-info'},
        ],
        'MiembrodelComite': [
            {'label': 'Evaluar Ideas', 'url': '/ideas/committee/review', 'icon': 'fas fa-balance-scale', 'btn_class': 'btn-info'},
        ],
        'Sponsor': [
            {'label': 'Aprobar Propuestas', 'url': '/ideas/sponsor/review', 'icon': 'fas fa-check-circle', 'btn_class': 'btn-success'},
        ],
    }

    # Acciones dinámicas basadas en roles
    actions = {}
    for role in roles:
        actions[role] = role_actions.get(role, [])

    # Renderizar el template con los datos
    return render(request, 'users/dashboard.html', {
        'user_data': user_data,
        'actions': actions,
    })


def login_view(request):
    # Elimina cualquier mensaje persistente
    storage = get_messages(request)
    for _ in storage:
        pass

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirige al dashboard después de iniciar sesión
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')




