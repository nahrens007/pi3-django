from django import template

register = template.Library()

def page(variable, arg):
    # variable should be the loop counter (i.e., which row is being printed)
    # arg should be the number of rows/elements per page.
    return int(variable/arg) + 1
    
register.filter('page', page)