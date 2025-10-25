from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Donor, Request
from .forms import DonorForm, CustomUserCreationForm, CustomAuthenticationForm ,DonationHistoryForm
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Donor, DonationHistory

# --- Home ---
def home(request):
    return render(request, 'blood/home.html')


# --- Register ---
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blood/register.html', {'form': form})


# --- Login ---
def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'blood/login.html', {'form': form})


# --- Logout ---
def user_logout(request):
    logout(request)
    return redirect('login')


# --- Dashboard ---
@login_required
def dashboard(request):
    user = request.user
    try:
        donor_profile = Donor.objects.get(user=user)
    except Donor.DoesNotExist:
        donor_profile = None

    # শুধুমাত্র available=True থাকা donor exclude current user
    donors = Donor.objects.filter(available=True).exclude(user=user)

    my_requests = Request.objects.filter(requester=user) if 'Request' in globals() else []

    context = {
        'donor_profile': donor_profile,
        'donors': donors,
        'my_requests': my_requests,
    }
    return render(request, 'blood/dashboard.html', context)


# --- Donor Section ---

@login_required
def donor_list(request):
    blood_group = request.GET.get('blood_group')

    if blood_group:
        donors = Donor.objects.filter(available=True, blood_group=blood_group)
    else:
        donors = Donor.objects.filter(available=True)

    return render(request, 'blood/donor_list.html', {'donors': donors, 'selected_group': blood_group})


@login_required
def donor_requests(request):
    try:
        donor = Donor.objects.get(user=request.user)
    except Donor.DoesNotExist:
        return redirect('profile')
    requests = donor.requests.all()
    return render(request, 'blood/donor_requests.html', {'requests': requests})


# --- Request Section ---
@login_required
def request_donor(request, donor_id):
    donor = Donor.objects.get(id=donor_id)
    if request.method == 'POST':
        reason = request.POST['reason']
        req = Request.objects.create(
            donor=donor,
            requester=request.user,
            reason=reason
        )

        # Send email to donor
        subject = "New Blood Request Received"
        message = f"Hello {donor.user.username},\n\nYou have received a new blood request from {request.user.username}.\nReason: {reason}\n\nPlease check your dashboard to respond."
        recipient = donor.user.email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=True)

        return render(request, 'blood/request_sent.html', {'donor': donor})
    return render(request, 'blood/request_form.html', {'donor': donor})

@login_required
def create_donor_profile(request):
    # যদি donor already থাকে, redirect directly to profile
    if Donor.objects.filter(user=request.user).exists():
        return redirect('profile')

    if request.method == "POST":
        blood_group = request.POST.get('blood_group')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        profile_pic = request.FILES.get('profile_pic')

        # Validate required fields
        if not blood_group or not phone or not department:
            return render(request, 'blood/create_donor.html', {
                'error': "Please fill in all required fields!"
            })

        # Create donor profile
        donor = Donor.objects.create(
            user=request.user,
            blood_group=blood_group,
            phone=phone,
            department=department,
            profile_pic=profile_pic
        )
        return redirect('profile')

    return render(request, 'blood/create_donor.html')




@login_required
def profile(request):
    """
    Donor profile view
    - যদি donor না থাকে → redirect to create_donor_profile
    - যদি থাকে → show profile
    """
    try:
        donor_profile = Donor.objects.get(user=request.user)
    except Donor.DoesNotExist:
        return redirect('create_donor_profile')

    # =========================
    # Update donation info automatically
    # =========================
    # 1. Last donation date
    last_donation = DonationHistory.objects.filter(donor=donor_profile).order_by('-date').first()
    donor_profile.last_donation_date = last_donation.date if last_donation else None

    # 2. Total donation count
    donor_profile.donation_count = DonationHistory.objects.filter(donor=donor_profile).count()
    # =========================

    return render(request, 'blood/profile.html', {'donor_profile': donor_profile})

@login_required
def toggle_availability(request):
    try:
        donor = Donor.objects.get(user=request.user)
        donor.available = not donor.available
        donor.save()
        return JsonResponse({'status': 'success', 'available': donor.available})
    except Donor.DoesNotExist:
        return JsonResponse({'status': 'error'})


@login_required
def respond_request(request, req_id, status):
    try:
        req = Request.objects.get(id=req_id, donor__user=request.user)
    except Request.DoesNotExist:
        return redirect('donor_requests')

    if status in ['Approved', 'Rejected']:
        req.status = status
        req.save()

        # Send email to requester
        subject = f"Your Blood Request has been {status}"
        message = f"Hello {req.requester.username},\n\nYour blood request to {req.donor.user.username} has been {status.lower()}.\n\nThank you for using Campus Blood!"
        recipient = req.requester.email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=True)

    return redirect('donor_requests')


@login_required
def edit_profile(request):
    donor_profile = get_object_or_404(Donor, user=request.user)

    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES, instance=donor_profile)
        if form.is_valid():
            donor = form.save(commit=False)
            # Manual donation_count update
            donation_count = request.POST.get('donation_count')
            if donation_count is not None:
                try:
                    donor.donation_count = int(donation_count)
                except ValueError:
                    donor.donation_count = donor.donation_count 
            donor.save()
            return redirect('profile')
    else:
        form = DonorForm(instance=donor_profile)

    return render(request, 'blood/edit_profile.html', {
        'form': form,
        'donor_profile': donor_profile  
    })


@login_required
def add_donation(request):
    donor = get_object_or_404(Donor, user=request.user)
    
    if request.method == 'POST':
        form = DonationHistoryForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = donor
            donation.save()  # signal auto update করবে donation_count & last_donation_date
            return redirect('profile')
    else:
        form = DonationHistoryForm()
    
    return render(request, 'blood/add_donation.html', {'form': form})
