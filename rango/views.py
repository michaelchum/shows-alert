# Create your views here.

# Import HttpResponse object from django.http module
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

# Import the Category model
from rango.models import Category, Page

# Import stuff for authentication (login)
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from rango.bing_search import run_query

# Each view takes at least one argument, a HttpRequest object which is also from django.http module
# By convention, it is named request
# Each view must return a HttpResponse object

# We loop through each category returned, and create a URL attribute.
# This attribute stores an encoded URL (e.g. spaces replaced with underscores).
def encodeURL(category_list):
	for category in category_list:
		category.url = category.name.replace(' ', '_')
	return

# Change underscores in the category name to spaces.
# URLs don't handle spaces well, so we encode them as underscores.
# We can then simply replace the underscores with spaces again to get the name.
def decodeURL(category_name_url):
	return category_name_url.replace('_', ' ')

def encode_url(name):
	return name.replace(' ', '_')

def decode_url(name):
	return name.replace('_', ' ')

def get_category_list():
	cat_list = Category.objects.all()

	encodeURL(cat_list)

	return cat_list

def get_category_list(max_results=0, starts_with=''):
	cat_list = []
	if starts_with:
		cat_list = Category.objects.filter(name__startswith=starts_with)
	else:
		cat_list = Category.objects.all()

	if max_results > 0:
		if len(cat_list) > max_results:
			cat_list = cat_list[:max_results]

	for cat in cat_list:
		cat.url = encode_url(cat.name)

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
	category_most_likes = Category.objects.order_by('-likes')[:5]
	categories = Category.objects.order_by('-views')[:5]
	pages = Page.objects.order_by('-views')[:5]
	context_dict = {'categories_likes': category_most_likes, 'categories': categories, 'pages': pages}
	encodeURL(category_most_likes)
	encodeURL(categories)

	# Get the category list and display on page
	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list

	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier
	# Note that the first parameter is the template we wish to use.
	return render_to_response('rango/index.html', context_dict, context)


def about(request):
	context = RequestContext(request)
	context_dict = {'boldmessage': "Rango says: Here is the about page."}
	return render_to_response('rango/about.html', context_dict, context)

def category(request, category_name_url):
	# Request our context from the request passed to us.
	context = RequestContext(request)

	category_name = decode_url(category_name_url)

	cat_list = get_category_list()

	# Create a context dictionary which we can pass to the template rendering engine.
	# We start by containing the name of the category passed by the user.
	context_dict = {'category_name': category_name}

	context_dict['cat_list'] = cat_list
	context_dict['category_name_url'] = category_name_url

	try:
		# Find the category with the given name.
		# Raises an exception if the category doesn't exist.
		# We also do a case insensitive match.
		category = Category.objects.get(name=category_name)
		context_dict['category'] = category
		# Retrieve all the associated pages.
		# Note that filter returns >= 1 model instance.
		pages = Page.objects.filter(category=category).order_by('-views')
		context_dict['pages'] = pages
	except Category.DoesNotExist:
		# We get here if the category does not exist.
		# Will trigger the template to display the 'no category' message.
		pass

	# Go render the response and return it to the client.
	return render_to_response('rango/category.html', context_dict, context)

def add_category(request):
	# Get the context from the request.
	context = RequestContext(request)

	# A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new category to the database.
			form.save(commit=True)

			# Now call the index() view.
			# The user will be shown the homepage.
			return index(request)
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = CategoryForm()

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render_to_response('rango/add_category.html', {'form': form}, context)

def add_page(request, category_name_url):
	context = RequestContext(request)

	category_name = decodeURL(category_name_url)
	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			# This time we cannot commit straight away.
			# Not all fields are automatically populated!
			page = form.save(commit=False)

			# Retrieve the associated Category object so we can add it.
			cat = Category.objects.get(name=category_name)
			page.category = cat

			# Also, create a default value for the number of views.
			page.views = 0

			# With this, we can then save our new model instance.
			page.save()

			# Now that the page is saved, display the category instead.
			return category(request, category_name_url)
		else:
			print form.errors
	else:
		form = PageForm()

	return render_to_response( 'rango/add_page.html',
		{'category_name_url': category_name_url,
		'category_name': category_name, 'form': form},
		context)

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
				return HttpResponse("Your Rango account is disabled.")
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
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)

	# Take the user back to the homepage.
	return HttpResponseRedirect('/rango/')

@login_required
def like_category(request):
	context = RequestContext(request)
	cat_id = None
	if request.method == 'GET':
		cat_id = request.GET['category_id']

	likes = 0
	if cat_id:
		category = Category.objects.get(id=int(cat_id))
		if category:
			likes = category.likes + 1
			category.likes =  likes
			category.save()

	return HttpResponse(likes)




