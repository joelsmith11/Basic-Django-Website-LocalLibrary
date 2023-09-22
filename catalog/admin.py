from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)


class BookInline(admin.TabularInline):
    model = Book
    extra = 0

# define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    inlines = [BookInline]


# register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance

    extra = 0


# Register the Book and BookInstance classes using decorators
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):

    list_display = ('display_title', 'status', 'borrower', 'due_back', 'id')

    list_filter = ('status', 'due_back')

    fieldsets = (
        ('General Information', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

