from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
	# response = "THIS IS DONE"
	return render(request, 'basic/index.html')

def register(request):
    # this is done
    results = User.objects.basic_validator(request.POST)
    if results['status']:
        request.session['id']= results['newUser'].id
        return redirect('/success')
    else:
        for tag, error in results['errors'].items():
            messages.error(request, error)
        return redirect('/')
    return redirect('/')

def login(request):
    results = User.objects.login_validator(request.POST)
    if results['status']:
        request.session['id'] = results['user'].id
    else:
        for tag, error in results['errors'].items():
            messages.error(request, error)
        return redirect('/')
    return redirect('/success')

def success(request):
    pass_ID = request.session['id']
    user = User.objects.filter(id = pass_ID)
    poster = user[0]
    print(poster.first_name)
    faved = Quote.objects.filter(faved_by = pass_ID)
    not_faved = Quote.objects.exclude(faved_by = pass_ID)
    context = {
        "quotes": not_faved,
        "fave_quotes": faved,
        "name": poster.first_name
    }
    return render(request, 'basic/success.html', context)

def uShow(request, id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        quotes = Quote.objects.filter(posted_by = id)
        print(quotes)
        count = quotes.count()
        print(count)
        context = {
            'user': User.objects.get(id = id),
            'count': count,
            'quotes': quotes
        }

        return render(request, 'basic/user.html', context)

def rev_create(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['id'])
        id = user.id
        # book_id = request.session['book_id']
        # print(book_id)
        quote = Quote.objects.quote_validator(id, request.POST)
        if quote['status'] == False:
            for tag, error in quote['errors'].items():
                messages.error(request, error)
        return redirect('/success')
def fav_btn(request):
    id = request.session['id']
    set = Quote.objects.faveQuote(id, request.POST)
    print(set)
    return redirect('/success')
def unfav_btn(request):
    id = request.session['id']
    unset = Quote.objects.unfaveQuote(id, request.POST)
    return redirect('/success')

def logout(request):
    request.session['id'] = None
    return redirect('/')

#########################################################################  above completed  #############################################################
