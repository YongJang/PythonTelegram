
import feedparser
import urllib.parse

keyword = ["인공지능","빅데이터","영화","경제"]

for n in range(0,len(keyword)):
    d = feedparser.parse('http://newssearch.naver.com/search.naver?where=rss&query=' + urllib.parse.quote(keyword[n].encode("utf-8")) + '&field=0')

    print (d['feed']['title'])

    print (d['feed']['link'])

    print (d.feed.subtitle)

    print (len(d['entries']))

    print (d['entries'][0]['title'])

    print (d.entries[0]['link'])


    for post in d.entries:
        print ("======== Entries =========")
        print (post.title + ":" + post.link + "\n")
        print (post.published + ":" + post.summary + "\n")

    for post in d.feed:
        print ("======= Feed ==========")
        print (post.title + ":" + post.link + "\n")
        print (post.published + ":" + post.summary + "\n")

    print (d.version)

    print (d.headers.get('content-type'))
