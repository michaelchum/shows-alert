# Create your views here.

# Import HttpResponse object from django.http module
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.forms import UserForm, UserProfileForm

from rango.models import TvShows, Episode, UserProfile
from django.contrib.auth.models import User

# Import stuff for authentication (login)
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required

# Each view takes at least one argument, a HttpRequest object which is also from django.http module
# By convention, it is named request
# Each view must return a HttpResponse object

# We loop through each category returned, and create a URL attribute.
# This attribute stores an encoded URL (e.g. spaces replaced with underscores).
def encodeURL(show_list):
	for show in show_list:
		show.url = show.show_name.replace(' ', '_')
	return

# Change underscores in the category name to spaces.
# URLs don't handle spaces well, so we encode them as underscores.
# We can then simply replace the underscores with spaces again to get the name.

def encode_url(name):
	return name.replace(' ', '_')

def decode_url(name):
	return name.replace('_', ' ')

def get_category_list():
	cat_list = TvShows.objects.all()

	encodeURL(cat_list)

	return cat_list

def get_category_list(max_results=0, starts_with=''):
	cat_list = []
	if starts_with:
		cat_list = TvShows.objects.filter(show_name__startswith=starts_with)
	else:
		cat_list = TvShows.objects.all()

	if max_results > 0:
		if len(cat_list) > max_results:
			cat_list = cat_list[:max_results]

	for cat in cat_list:
		#cat.added = cat.users.count()
		cat.url = encode_url(cat.show_name)

	return cat_list

def suggest_category(request):
	context = RequestContext(request)
	cat_list = []
	starts_with = ''
	if request.method == 'GET':
		starts_with = request.GET['suggestion']
	else:
		starts_with = request.POST['suggestion']

	cat_list = get_category_list(8, starts_with)

	return render_to_response('rango/category_list.html', {'cat_list': cat_list }, context)
	
def index(request):
	# Request the context of the request
	# The context contains information such as the client's machine details for example.
	context = RequestContext(request)

	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary which will be passed to the template engine
	show_list = TvShows.objects.order_by('-likes')[:10]
	episodes = Episode.objects.order_by('-creation_date')[:10]
	encodeURL(show_list)
	context_dict = {'show_list': show_list, 'episodes': episodes}

	# Get the category list and display on page for sidebar
	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list

	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier
	# Note that the first parameter is the template we wish to use.
	return render_to_response('rango/index.html', context_dict, context)


def about(request):
	context = RequestContext(request)
	context_dict = {'boldmessage': "Rango says: Here is the about page."}

	# Get the category list and display on page for sidebar
	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list
	return render_to_response('rango/about.html', context_dict, context)

def shows_list(request):
	context = RequestContext(request)
	show_list = get_category_list()

	context_dict = {'show_list': show_list}

	try:
		up = UserProfile.objects.get(user=request.user)
		context_dict['up'] = up
	except:
		up = None

	if up:
		user_show_list = up.show_list.all()
		context_dict['user_show_list'] = user_show_list

	# Get the category list and display on page for sidebar
	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list

	return render_to_response('rango/shows_list.html', context_dict, context)

def show(request, show_name_url):
	# Request our context from the request passed to us.
	context = RequestContext(request)

	show_name = decode_url(show_name_url)

	context_dict = {'show_name': show_name}
	context_dict['show_name_url'] = show_name_url

	try:
		# Find the category with the given name.
		# Raises an exception if the category doesn't exist.
		# We also do a case insensitive match.
		show = TvShows.objects.get(show_name=show_name)
		context_dict['show'] = show
		show.added = show.users.count()
		context_dict['number_added'] = show.added
		show.save
	except TvShows.DoesNotExist:
		# We get here if the category does not exist.
		# Will trigger the template to display the 'no category' message.
		pass

	# Get the category list and display on page for sidebar
	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list

	# Go render the response and return it to the client.
	return render_to_response('rango/show.html', context_dict, context)

def register(request):
	context = RequestContext(request)

	registered = False

	# If HTTP POST, process the form data
	if request.method == 'POST':
		# Input the raw post information into the forms
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		# If the two forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database.
			user = user_form.save()

			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()

			# Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves, we set commit=False.
			# This delays saving the model until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False) # We don't commmit to the database yet
			profile.user = user

			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and put it in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			# Now we save the UserProfile model instance.
			profile.save()

			# Update our variable to tell the template registration was successful.
			registered = True

		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
		else:
			print user_form.errors, profile_form.errors

	# Not a HTTP POST, we render our form using two ModelForm instances.
	# These forms will be blank, ready for user input.
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	# Render the template depending on the context.
	return render_to_response(
		'rango/register.html',
		{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
		context)

def user_login(request):
	context = RequestContext(request)

	# If HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		username = request.POST['username']
		password = request.POST['password']

		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)

		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user is not None:
			# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				login(request, user)
				return HttpResponseRedirect('/rango/')
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your ShowsAlert account is disabled.")
		else:
			# Bad login details were provided. So we can't log the user in.
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login credentials.")

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render_to_response('rango/login.html', {}, context)

#login_required() decorator ensures only logged in users can access the view

@login_required
def my_list(request):
	context = RequestContext(request)

	cat_list = get_category_list()
	context_dict = {'cat_list': cat_list}
	
	up = UserProfile.objects.get(user=request.user)

	if up:
		user_show_list = up.show_list.all()
		context_dict['user_show_list'] = user_show_list

	return render_to_response('rango/my_list.html', context_dict, context)

@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)

	# Take the user back to the homepage.
	return HttpResponseRedirect('/rango/')

@login_required
def add_show(request):
	context = RequestContext(request)
	show_id = None

	if request.method == 'GET':
		show_id = request.GET['show_id']

	up = UserProfile.objects.get(user=request.user)

	added = 0
	if show_id:
		show = TvShows.objects.get(id=int(show_id))
		if show:
			added = show.added + 1
			show.added =  added
			show.users.add(request.user)
			up.show_list.add(show)
			show.save()
			up.save()

	cat_list = get_category_list()
	context_dict = {'cat_list': cat_list}

	show_list = get_category_list()
	context_dict['show_list'] = show_list
	context_dict['user_show_list'] = up.show_list.all()
	context_dict['up'] = up
	
	return render_to_response('rango/sub_shows_list.html', context_dict, context)


@login_required
def like_category(request):
	context = RequestContext(request)
	cat_id = None
	if request.method == 'GET':
		cat_id = request.GET['category_id']

	likes = 0
	if cat_id:
		category = TvShows.objects.get(id=int(cat_id))
		if category:
			likes = TvShows.likes + 1
			category.likes =  likes
			category.save()

	return HttpResponse(likes)




