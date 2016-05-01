import feedparser

d = feedparser.parse('http://newssearch.naver.com/search.naver?where=rss&query=%C0%CE%B0%F8%C1%F6%B4%C9&field=0')

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
