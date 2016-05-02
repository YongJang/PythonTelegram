
import feedparser
import urllib.parse

keyword = "인공지능"

d = feedparser.parse('http://newssearch.naver.com/search.naver?where=rss&query=' + urllib.parse.quote(keyword.encode("utf-8")) + '&field=0')

print (d['feed']['title'])

print (d['feed']['link'])

print (d.feed.subtitle)

print (len(d['entries']))

print (d['entries'][0]['title'])

print (d.entries[0]['link'])


for post in d.entries:
    print (post.title + ":" + post.link + "\n")
    print (post.published + ":" + post.summary + "\n")

print (d.version)

print (d.headers.get('content-type'))
