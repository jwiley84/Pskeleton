So.

I want to display:

quotes.objects.all() EXCEPT where faved_by = request.session['id']

On the faved by side, I ONLY want to dislay quotes.objects.all() where faved_by = request.session['id']