import datetime

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from .models import Book, Author, BookInstance, Genre, Language
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from catalog.forms import RenewBookForm
from catalog.models import Author

from django.views.generic.edit import CreateView, UpdateView, DeleteView


def index(request):
    """View function for home page of site"""

    # Generate counts of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # get number of available books
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # get number of author
    # note that 'all()' is implied by default
    num_authors = Author.objects.count()

    # to get the number of history books, we need to go through the Genre
    # object, then the name, and use iexact for case insensitive
    num_books_history = Book.objects.filter(genre__name__iexact='history').count()

    # Number of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_author': num_authors,
        'num_books_history': num_books_history,
        'num_visits': num_visits
    }

    # render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/index.html', context=context)


class BookListView(generic.ListView):
    model = Book

    paginate_by = 10

    context_object_name = 'book_list'  # my own name for the list as a template variable

    # template_name = 'books/my_temp_name_list.html'  # specify your own template name and location

    # we can change the query set and the context data returned using the examples found
    # here: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Generic_views


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    context_object_name = 'author_list'


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )


class LoanedBooksByUserLibrarianListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan to a staff user."""
    permission_required = 'catalog.can_mark_returned'

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user_staff.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    # get_object_or_404 returns the specified object from a model based on the primary
    # key, or raises a 404 if it doesn't exist
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a post, then process the form data
    if request.method == 'POST':

        # Create a new form instance and populate it with the data from the request
        form = RenewBookForm(request.POST)

        # Check if th form is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to new URL
            return HttpResponseRedirect(reverse('staff-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'

    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': datetime.date.today()}


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'

    model = Author
    fields = '__all__'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'

    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'

    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']


class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'

    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']


class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'

    model = Book
    success_url = reverse_lazy('books')
