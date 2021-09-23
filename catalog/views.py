from django.http import request
from django.shortcuts import render

# Create your views here.

from .models import Book, Author, BookInstance, Genre

from django.views import generic

from django.core.mail import send_mail

from django.contrib.auth.backends import BaseBackend

from django.conf import settings


def index(request):
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 5


class BookDetailView(generic.DetailView):
    model = Book


class AuthorsListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author


# add send e-mail confirmation
# set up the subject, message, and user’s email address

subject = "Email Generation"
message = "First Django Application"

user = settings  # request was passed to the method as a parameter for the view
user_email = user.EMAIL_HOST_USER  # pull user’s email out of the user record

# try to send the e-mail – note you can send to multiple users – this just sends
# to one user.
try:
    send_mail(subject, message, from_email='navaneetha.mogulla@gmail.com', recipient_list=[user_email])
    sent = True
except:
    print("Error sending e-mail")


