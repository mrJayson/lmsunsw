import sys
from django.conf import settings
from django.db import connection
from django.utils import termcolors

# function used during debug to determine number of db queries
# use debug toolbar instead


class QueryPrintingMiddleware(object):
    start = None

    def process_request(self, request):
        if settings.DEBUG:
            self.start = len(connection.queries)

    def process_response(self, request, response):
        if settings.DEBUG and 'runserver' in sys.argv and self.start is not None:
            red = termcolors.make_style(opts=('bold',), fg='red')
            yellow = termcolors.make_style(opts=('bold',), fg='yellow')

            count = len(connection.queries) - self.start
            output = '# queries: %s' % count
            output = output.ljust(15)

            # add some colour
            if count > 100:
                output = red(output)
            elif count > 10:
                output = yellow(output)

            # runserver just prints its output to sys.stderr, so follow suite
            sys.stderr.write(output)

        return response