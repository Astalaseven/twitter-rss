<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='static.css') }}">
    <title>
      Twitter-RSS
    </title>

<body>

	<h1>RSS generator for Twitter</h1>

	<form action="/user" method="POST">
	<input type="text" id="username" name="user_data" size="40" placeholder="Enter an username">
	<input type="submit" id="userIt" value="RSS it!">
	</form>

	<form action="/htag" method="POST">
	<input type="text" id="hashtag" name="user_data" size="40" placeholder="Enter a hashtag">
	<input type="submit" id="htagIt" value="RSS it!">
	</form>

	{% if err %} <p class=error><strong>Error:</strong> </p> <p>{{ err }}</p> {% endif %}

</body>
	
	<footer>
		<p><a href="https://github.com/Astalaseven/twitter-rss">Source code on GitHub</a></p>
	</footer>

</html>
