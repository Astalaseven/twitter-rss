<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
    <link rel=stylesheet type=text/css href="{{ url_for('static', filename='bootstrap-responsive.css') }}">
    <title>
      Twitter-RSS
    </title>

<body>

	<h1>RSS generator for Twitter</h1>

	<form action="/user" method="POST">
	<input type="text" id="username" name="user_data" size="40" placeholder="Enter an username">
	<input type="submit" id="username" value="RSS it!">
	</form>

	<form action="/htag" method="POST">
	<input type="text" id="hashtag" name="user_data" size="40" placeholder="Enter a hashtag">
	<input type="submit" id="hashtag" value="RSS it!">
	</form>

	{% if error %}
    <p class=error><strong>Error:</strong> {{ error }}
  	{% endif %}

</body>

</html>
