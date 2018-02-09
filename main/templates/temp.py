@permission_required('main.add_reservation', 'login', raise_exception=True)
def reserve(request):
    title = "Add reservation"

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            staff = request.user
            customer = Customer(
                first_name=form.cleaned_data.get('first_name'),
                middle_name=form.cleaned_data.get('middle_name'),
                last_name=form.cleaned_data.get('last_name'),
                contact_no=form.cleaned_data.get('contact_no'),
                email_address=form.cleaned_data.get('email'),
                address=form.cleaned_data.get('address'),
            )
            customer.save()
            reservation = Reservation(
                customer=customer,
                staff=staff,
                reservation_date_time=timezone.now(),
                expected_arrival_date_time=form.cleaned_data.get('expected_arrival_date_time'),
                expected_departure_date_time=form.cleaned_data.get('expected_departure_date_time'),
            )
            reservation.save()
            return redirect('reservations')
    else:
        form = ReservationForm()
    return render(
        request,
        'reserve.html', {
            'title': title,
            'form': form,
        }
    )
