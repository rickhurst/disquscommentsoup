# convert exported disqus comments into their own custom format
# this might be useful if you have moved blog software or URL scheme
# and want to reimport existing comments
import sys

from bs4 import BeautifulSoup
from django.template import Template, Context
from django.conf import settings
settings.configure()


class thread(object):
    ''' Thread class holds attributes for a post, including comments '''
    pass


class comment(object):
    ''' Comment class holds attributes for comment '''
    pass

def process_uri(uri):
    # The following processing is specific to my task
    # of changing e.g 2010-06-01-foo-bar.html to 2010/06/01/foo-bar
    uri = uri.replace('.html', '')
    uri_as_list = list(uri)
    uri_as_list[4] = '/'
    uri_as_list[7] = '/'
    uri_as_list[10] = '/'
    uri = "".join(uri_as_list)
    return uri

def to_gmt(date_str):
    ''' convert from YYYY-MM-DDTHH:MM:SSZ to YYYY-MM-DD HH:MM:SS '''
    date_as_list = list(date_str)
    date_as_list[10] = ' '
    date_as_list[19] =''
    return "".join(date_as_list)

try:
    soup = BeautifulSoup(open(sys.argv[1]), "xml")
except IndexError:
    print 'No file specified'
    sys.exit(0)

try:
    host = sys.argv[2]
except IndexError:
    print "No host specified"
    sys.exit(0)

#print soup.prettify()
threads = {}

# loop through threads to get id and uri
for thread_tag in soup.find_all('thread'):
    t = thread()
    t.id = thread_tag['dsq:id']
    t.comments = []

    if(thread_tag.id):
        t.slug = thread_tag.id.contents[0]
        t.uri = process_uri(t.slug)
        t.title = thread_tag.title.contents[0]
        t.date_time = thread_tag.createdAt.contents[0]
        t.date_gmt = to_gmt(t.date_time)
        print t.title
        threads[t.id] = t

# loop through posts to find comments and associate with
# thread
c_id = 0

for post in soup.find_all('post'):
    if post.thread:
        c_id = c_id + 1
        thread_id = post.thread['dsq:id']
        print 'thread id' + thread_id
        c = comment()
        c.message = post.message.contents[0]
        try:
            c.email = post.author.email.contents[0]
        except IndexError:
            c.email = ''
            pass

        c.name = post.author.find('name').contents[0]
        c.ipaddress = post.ipAddress.contents[0]
        #c.date_time = 
        c.date = post.createdAt.contents[0]
        c.date_gmt = to_gmt(c.date)

        c.id = c_id

        threads[thread_id].comments.append(c)


# for thread_id,thread in threads.items():
#     print thread.id + ' ' + thread.uri
#     print thread.comments
#     for comment in thread.comments:
#         try:
#             print comment.email[0]
#         except IndexError:
#             pass
#         #print comment.name[0]
#         #print comment.ipaddress[0]
#         #print comment.message[0]

# for rendering of output xml using django templates, see:-
# http://stackoverflow.com/questions/98135/how-do-i-use-django-templates-without-the-rest-of-django
# >>> from django.template import Template, Context
# >>> from django.conf import settings
# >>> settings.configure()
# >>> t = Template('My name is {{ my_name }}.')
# >>> c = Context({'my_name': 'Daryl Spitzer'})
# >>> t.render(c)
print threads

f = open('import_template.xml')
t = Template(f.read())
c = Context({
    'threads': threads,
    'host': host,
    })
output = t.render(c)
print output

output = output.encode('ascii', 'ignore')
f_out = open('output.xml', 'w')
f_out.write(output)




