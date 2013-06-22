<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
    <channel>
        <atom:link href="http://{{server}}/{{descriptor}}.xml" rel="self" type="application/rss+xml" />
        <title>{{title}}</title>
        <link>{{url}}</link>
        <description>twitter-rss of {{descriptor}}</description>
        <language>fr</language>

        {% for tweet in tweets %}
            <item>
            <title>{{tweet.title}}</title>
            <guid>https://twitter.com{{tweet.link}}</guid>
            <link>https://twitter.com{{tweet.link}}</link>
            <pubDate>{{tweet.date}}</pubDate>
            <description><![CDATA[
                {{tweet.author}}: {{tweet.content}}
                {% if tweet.pic %}
                <br><br><img src="{{tweet.pic}}" alt="{{tweet.title}}" />
                {% endif %}]]></description>
            </item>
        {% endfor %}

    </channel>
</rss>