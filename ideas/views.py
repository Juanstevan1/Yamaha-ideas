from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ideas.models import Idea, Program, Team, CommitteeRating  # Importar CommitteeRating
from django.contrib.auth.models import User
from ideas.forms import IdeaForm
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from django.db.models import Q
from ideas.forms import IdeaReviewForm
from ideas.models import Idea, SponsorDecision

@login_required
def select_program(request):
    if request.method == "POST":
        program_id = request.POST.get("program")
        return redirect("register_idea", program_id=program_id)

    programs = Program.objects.all()
    return render(request, "ideas/select_program.html", {"programs": programs})

@login_required
def register_idea(request, program_id):
    program = get_object_or_404(Program, id=program_id)

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['program'] = program.id
        form = IdeaForm(post_data, request.FILES, program=program)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.employee = request.user  # Asignar el usuario autenticado como empleado
            idea.program = program
            print("Prototype file before save:", idea.prototype_file)
            print("Related image before save:", idea.related_image)
            idea.save()
            print("Prototype file after save:", idea.prototype_file.url)
            print("Related image after save:", idea.related_image.url)

            # Notificar a los coordinadores del programa sobre la nueva idea
            coordinators = idea.program.coordinators.all()
            for coordinator in coordinators:
                Notification.objects.create(
                    user=coordinator,
                    related_idea=idea,
                    type='idea_update',
                    message=f"Se ha registrado una nueva idea '{idea.title}' en el programa '{idea.program.name}'."
                )

            messages.success(request, 'La idea fue creada exitosamente.')
            return redirect('dashboard')
        else:
            print(form.errors)  # Depuración de errores
    else:
        form = IdeaForm(program=program)

    return render(request, 'ideas/register_idea.html', {'form': form, 'program': program})

@login_required
def my_ideas(request):
    # Obtener las ideas del empleado actual
    employee_ideas = Idea.objects.filter(employee=request.user)

    # Filtros
    search_query = request.GET.get('search', '').strip()  # Búsqueda por título o descripción
    state_filter = request.GET.get('state', '')  # Filtro por estado

    if search_query:
        employee_ideas = employee_ideas.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
    if state_filter:
        employee_ideas = employee_ideas.filter(state=state_filter)

    # Diccionario de íconos para los estados
    state_icons = {
        "pending": "fas fa-hourglass-start",
        "reviewed_by_coordinator": "fas fa-search",
        "coordinator_rejected": "fas fa-times-circle",
        "committee_in_review": "fas fa-comments",
        "committee_approved": "fas fa-check-circle",
        "committee_rejected": "fas fa-times-circle",
        "sponsor_rejected": "fas fa-thumbs-down",
        "in_progress": "fas fa-cog",
        "completed": "fas fa-check-double",
        "adjustments_required_by_sponsor": "fas fa-edit",
    }

    # Asignar ícono correspondiente a cada idea
    for idea in employee_ideas:
        idea.icon = state_icons.get(idea.state, "fas fa-question-circle")

    # Datos para los filtros
    state_choices = Idea.STATES

    return render(request, 'ideas/user_ideas.html', {
        'ideas': employee_ideas,
        'search_query': search_query,
        'state_filter': state_filter,
        'state_choices': state_choices,
    })

@login_required
def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    # Convertir los datos extras (JSON) en un formato manejable
    extra_data = idea.extra_data or {}

    # Obtener las calificaciones del comité
    committee_ratings = idea.ratings.all()

    return render(request, 'ideas/detail_idea.html', {
        'idea': idea,
        'extra_data': extra_data,
        'coordinator_comments': idea.coordinator_review_comments,
        'committee_ratings': committee_ratings,
    })

@login_required
def edit_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    program = idea.program  # Obtener el programa asociado para cargar sus campos extras
    
    if idea.state == 'completed':
        messages.error(request, "No puedes editar una idea que ya ha sido completada.")
        return redirect('my_ideas')
    
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['program'] = program.id
        form = IdeaForm(post_data, request.FILES, instance=idea, program=program)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.state = 'pending'  # Cambiar el estado a 'pending'
            idea.save()
            messages.success(request, 'La idea fue actualizada exitosamente y está pendiente de revisión.')
            return redirect('my_ideas')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = IdeaForm(instance=idea, program=program)

    return render(request, 'ideas/edit_idea.html', {
        'form': form,
        'program': program,
        'idea': idea,
    })

@login_required
def coordinator_review_ideas(request):
    # Asegurarse de que el usuario tiene el rol de coordinador
    if not request.user.profile.is_coordinator:
        messages.error(request, "No tienes permisos para acceder a esta sección.")
        return redirect('dashboard')

    # Filtros
    query = request.GET.get('q', '')
    state_filter = request.GET.get('state', '')

    # Ideas asociadas a los programas del coordinador
    ideas = Idea.objects.filter(program__coordinators=request.user)

    # Aplicar búsqueda
    if query:
        ideas = ideas.filter(Q(title__icontains=query) | Q(description__icontains=query))

    # Aplicar filtro por estado
    if state_filter:
        ideas = ideas.filter(state=state_filter)

    # Datos para los filtros
    state_choices = Idea.STATES

    # Renderizar la plantilla
    return render(request, 'coordinator/review_ideas.html', {
        'ideas': ideas,
        'query': query,
        'state_filter': state_filter,
        'state_choices': state_choices,
    })

@login_required
def coordinator_review_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    # Definir los estados permitidos para el coordinador
    allowed_states = ['reviewed_by_coordinator', 'coordinator_rejected', 'pending']

    if request.method == 'POST':
        # Actualizar el estado de la idea y agregar comentarios del coordinador
        comments = request.POST.get('coordinator_review_comments', '')
        new_state = request.POST.get('state', idea.state)
        if new_state in allowed_states:  # Validar que el estado asignado es permitido
            idea.coordinator_review_comments = comments
            idea.state = new_state
            idea.save()

            # Notificar al empleado sobre la revisión del coordinador
            Notification.objects.create(
                user=idea.employee,
                related_idea=idea,
                type='idea_update',
                message=f"Tu idea '{idea.title}' ha sido '{idea.get_state_display()}' por el coordinador."
            )

            messages.success(request, 'La idea ha sido actualizada.')
        else:
            messages.error(request, 'El estado seleccionado no es válido para su rol.')
        return redirect('coordinator_review_ideas')

    # Renderizar la idea con los datos actuales (incluyendo archivos e imágenes)
    return render(request, 'coordinator/review_idea.html', {
        'idea': idea,
        'allowed_states': allowed_states,  # Pasar los estados permitidos al template
    })


@login_required
def committee_review_ideas(request):
    # Filtros para ideas revisadas por el coordinador
    query = request.GET.get('q', '')
    state_filter = request.GET.get('state', 'reviewed_by_coordinator')
    ideas = Idea.objects.filter(
        Q(state='reviewed_by_coordinator') | Q(state='committee_in_review') | Q(state='coordinator_rejected'),
        program__committee_members=request.user
    )
    
    if query:
        ideas = ideas.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    if state_filter:
        ideas = ideas.filter(state=state_filter)
    
    # Ideas ya revisadas por el miembro del comité
    reviewed_ideas = Idea.objects.filter(
        ratings__committee_member=request.user
    ).distinct()

    # Datos para los filtros
    state_choices = Idea.STATES

    return render(request, 'committe/committee_review_ideas.html', {
        'ideas': ideas,
        'reviewed_ideas': reviewed_ideas,
        'query': query,
        'state_filter': state_filter,
        'state_choices': state_choices,
    })

@login_required
def committee_review_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id, program__committee_members=request.user)
    allowed_states = ['committee_approved', 'committee_rejected']
    # Limpiar el valor del campo para evitar 'None' o espacios
    if not idea.committee_feedback:
        idea.committee_feedback = ""
    else:
        idea.committee_feedback = idea.committee_feedback.strip()

    if request.method == 'POST':
        comments = request.POST.get('committee_feedback', '')
        rating = request.POST.get('committee_rating', None)

        # Guardar la calificación del comité
        CommitteeRating.objects.update_or_create(
            committee_member=request.user,
            idea=idea,
            defaults={'rating': rating, 'comments': comments}
        )

        # Verificar si todos los miembros del comité han revisado la idea
        if idea.all_committee_reviews_complete():
            new_state = idea.calculate_committee_decision()
            idea.state = new_state
            idea.save()

            # Notificar al empleado y a los coordinadores sobre la decisión del comité
            Notification.objects.create(
                user=idea.employee,
                related_idea=idea,
                type='idea_update',
                message=f"Tu idea '{idea.title}' ha sido '{idea.get_state_display()}' por el comité."
            )

            coordinators = idea.program.coordinators.all()
            for coordinator in coordinators:
                Notification.objects.create(
                    user=coordinator,
                    related_idea=idea,
                    type='idea_update',
                    message=f"La idea '{idea.title}' ha sido '{idea.get_state_display()}' por el comité."
                )

            messages.success(request, 'La idea ha sido evaluada correctamente.')
        else:
            messages.success(request, 'Tu evaluación ha sido registrada.')

        return redirect('committee_review_ideas')

    return render(request, 'committe/committee_review_idea.html', {
        'idea': idea,
        'allowed_states': allowed_states,
    })


@login_required
def committee_view_idea(request, idea_id):
    """
    Vista para mostrar los detalles de la idea, junto con las calificaciones y comentarios del comité.
    """
    idea = get_object_or_404(Idea, id=idea_id, program__committee_members=request.user)
    committee_ratings = CommitteeRating.objects.filter(idea=idea)

    return render(request, 'committe/committee_view_idea.html', {
        'idea': idea,
        'committee_ratings': committee_ratings,
    })


@login_required
def coordinator_assign_team(request):
    query = request.GET.get('q', '')
    ideas = Idea.objects.filter(
        Q(state='committee_approved') | Q(state='adjustments_required_by_sponsor')
    ).exclude(team__isnull=False)  # Excluir ideas con equipo asignado

    if query:
        ideas = ideas.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    teams = Team.objects.all()

    return render(request, 'coordinator/assign_team.html', {
        'ideas': ideas,
        'query': query,
        'teams': teams,
    })


@login_required
def coordinator_assign_team_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    team_members = User.objects.filter(profile__roles__name='Empleado')  # Filtrar empleados

    # Obtener calificaciones y comentarios del comité
    committee_ratings = CommitteeRating.objects.filter(idea=idea)

    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        selected_members = request.POST.getlist('team_members')  # Obtener miembros seleccionados

        if not team_name or not selected_members:
            messages.error(request, 'Debe asignar un nombre y al menos un miembro al equipo.')
        else:
            # Crear o actualizar el equipo
            team, created = Team.objects.update_or_create(
                idea=idea,
                defaults={'name': team_name},
            )
            team.members.set(User.objects.filter(id__in=selected_members))
            team.save()

            idea.state = 'in_progress'
            idea.save()

            # Notificar a los miembros del equipo asignado
            for member in team.members.all():
                Notification.objects.create(
                    user=member,
                    related_idea=idea,
                    type='team_assignment',
                    message=f"Has sido asignado al equipo '{team.name}' para la idea '{idea.title}'."
                )

            # Notificar al empleado sobre el avance de su idea
            Notification.objects.create(
                user=idea.employee,
                related_idea=idea,
                type='idea_update',
                message=f"Tu idea '{idea.title}' está ahora en progreso con el equipo '{team.name}'."
            )

            messages.success(request, 'El equipo fue asignado exitosamente.')
            return redirect('coordinator_assign_team')

    return render(request, 'coordinator/assign_team_detail.html', {
        'idea': idea,
        'team_members': team_members,
        'sponsor_comment': idea.sponsor_adjustment_comments,
        'committee_ratings': committee_ratings,  # Enviar datos del comité
    })


@login_required
def sponsor_review_list(request):
    query = request.GET.get('q', '')
    state_filter = request.GET.get('state', 'in_progress')
    ideas = Idea.objects.filter(state='in_progress')

    if query:
        ideas = ideas.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if state_filter:
        ideas = ideas.filter(state=state_filter)

    state_choices = Idea.STATES

    return render(request, 'sponsor/review_list.html', {
        'ideas': ideas,
        'query': query,
        'state_filter': state_filter,
        'state_choices': state_choices,
    })

@login_required
def sponsor_review_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    if request.method == 'POST':
        decision = request.POST.get('decision')
        comments = request.POST.get('comments')

        if not decision:
            messages.error(request, 'Debe seleccionar una decisión.')
        else:
            # Crear o actualizar la decisión del Sponsor
            SponsorDecision.objects.update_or_create(
                idea=idea,
                sponsor=request.user,
                defaults={
                    'decision': decision,
                    'comments': comments,
                }
            )

            # Actualizar estado de la idea basado en la decisión
            if decision == 'approved':
                idea.state = 'completed'
            elif decision == 'rejected':
                idea.state = 'sponsor_rejected'
            elif decision == 'adjustments_required':
                idea.state = 'adjustments_required_by_sponsor'
                idea.sponsor_adjustment_comments = comments
            idea.save()

            # Notificar al empleado y a los coordinadores
            Notification.objects.create(
                user=idea.employee,
                related_idea=idea,
                type='idea_update',
                message=f"Tu idea '{idea.title}' ha sido '{idea.get_state_display()}' por el sponsor."
            )

            coordinators = idea.program.coordinators.all()
            for coordinator in coordinators:
                Notification.objects.create(
                    user=coordinator,
                    related_idea=idea,
                    type='idea_update',
                    message=f"La idea '{idea.title}' ha sido '{idea.get_state_display()}' por el sponsor."
                )

            messages.success(request, 'La decisión fue registrada exitosamente.')
            return redirect('sponsor_review_list')

    # Obtener decisión existente si ya existe
    sponsor_decision = SponsorDecision.objects.filter(idea=idea, sponsor=request.user).first()

    return render(request, 'sponsor/review_detail.html', {
        'idea': idea,
        'sponsor_decision': sponsor_decision,
    })


@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'coordinator/team_detail.html', {
        'team': team,
        'sponsor_comment': team.idea.sponsor_adjustment_comments,
    })

@login_required
def team_edit_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    program = idea.program  # Obtener el programa asociado para cargar sus campos extras
    team = idea.team  # Obtener el equipo asociado a la idea

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['program'] = program.id
        form = IdeaForm(post_data, request.FILES, instance=idea, program=program)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.state = 'in_progress'  # Cambiar el estado a 'in_progress'
            idea.save()

            # Notificar al coordinador sobre la actualización de la idea por el equipo
            coordinators = idea.program.coordinators.all()
            for coordinator in coordinators:
                Notification.objects.create(
                    user=coordinator,
                    related_idea=idea,
                    type='idea_update',
                    message=f"El equipo '{team.name}' ha actualizado la idea '{idea.title}'."
                )

            messages.success(request, 'La idea fue actualizada exitosamente y está en progreso.')
            return redirect('team_detail', team_id=team.id)
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = IdeaForm(instance=idea, program=program)

    return render(request, 'coordinator/team_edit_idea.html', {
        'form': form,
        'program': program,
        'idea': idea,
        'team': team,
    })