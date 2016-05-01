import feedparser

d = feedparser.parse('http://newssearch.naver.com/search.naver?where=rss&query=%C0%CE%B0%F8%C1%F6%B4%C9&field=0')

print (d['feed']['title'])

print (d['feed']['link'])
