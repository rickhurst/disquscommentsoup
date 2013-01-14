# convert exported disqus comments into their own custom format
# this might be useful if you have moved blog software or URL scheme
# and want to reimport existing comments

from bs4 import BeautifulSoup
soup = BeautifulSoup(open('rickontheroad-2013-01-09T08-27-21.191539-all.xml'), "xml")


class thread(object):
    ''' Thread class holds attributes for a post, including comments '''
    pass


class comment(object):
    ''' Comment class holds attributes for comment '''
    pass


print soup.prettify()
threads = {}

# loop through threads to get id and uri
for thread_tag in soup.find_all('thread'):
    t = thread()
    t.id = thread_tag['dsq:id']
    t.comments = []

    if(thread_tag.id):
        t.uri = thread_tag.id.contents

        threads[t.id] = t

# loop through posts to find comments and associate with
# thread
for post in soup.find_all('post'):
    if post.thread:
        thread_id = post.thread['dsq:id']
        print 'thread id' + thread_id
        c = comment()
        c.message = post.message.contents
        c.email = post.author.email.contents
        c.name = post.author.find('name').contents
        c.ipaddress = post.ipAddress.contents

        threads[thread_id].comments.append(c)

        #print c.__dict__

#print threads['122686389'].__dict__
for thread_id,thread in threads.items():
    print thread.id + ' ' + thread.uri[0]
    #print thread.comments
    for comment in thread.comments:
        try:
            print comment.email[0]
        except IndexError:
            pass
        print comment.name[0]
        print comment.ipaddress[0]
        print comment.message[0]

