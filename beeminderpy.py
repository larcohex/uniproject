"""
	Beeminder API library.
	Author: Kudayar Pirimbaev
"""


import urllib
import urllib2
import datetime

class Beeminder:


	def __init__ (self, username, this_auth_token):
		"""
			Constructor for Beeminder API class.
			It is your job to take auth_token from server.
		"""
		self.username = username
		self.auth_token = this_auth_token
		self.base_url = "https://www.beeminder.com/api/v1"


	"""
		User attributes:
			username (string) - username
			timezone (string) - timezone
			updated_at (number) - Unix timestamp (in seconds) of the last update to this user or any of their goals or datapoints.
			goals (array) - A list of slugs for each of the user's goals, or an array of goal hashes if diff_since or associations is sent.
			deadbeat (boolean) - True if the user's payment info is out of date, or a an attempted payment has failed.
			deleted_goals (array) - An array of hashes, each with one key/value pair for the id of the deleted goal. Only returned if diff_since is sent.
	"""


	def get_user (self):
		"""
			Get user information
		"""

		url = "%s/users/%s.json" % (self.base_url, self.username)
		values = {
			"auth_token" : self.auth_token
		}
		result = self.call_api (url, values, "GET")
		return result


	"""
		Goal attributes:
			slug (string) - The final part of the URL of the goal, used as an identifier. E.g, if user "alice" has a goal at beeminder.com/alice/weight then the goal's slug is "weight".
			updated_at (number) - Unix timestamp of the last time this goal was updated.
			burner (string) - One of frontburner, backburner. Indicates whether the goal is on the "frontburner" for the user in their gallery or whether the goal has been relegated to the "backburner" (below the fold on the web interface).
			title (string) - The title that the user specified for the goal. E.g., "Weight Loss".
			goaldate (number) - Unix timestamp (in seconds) of the goal date.
			goalval (number) - Goal value - the number the yellow brick road will eventually reach. E.g., 70 kilograms.
			rate (number) - The slope of the (final section of the) yellow brick road.
			graph_url (string) - URL for the goal's graph image. E.g., "http -//static.beeminder.com/alice/weight.png".
			thumb_url (string) - URL for the goal's graph thumbnail image. E.g., "http://static.beeminder.com/alice/weight-thumb.png".
			autodata (string) - The name of automatic data source, if this goal has one. Will be the empty string for manual goals.
			goal_type (string) - One of the following symbols:
				hustler: Do More
				biker: Odometer
				fatloser: Weight loss
				gainer: Gain Weight
				inboxer: Inbox Fewer
				drinker: Do Less
				custom: Full access to the underlying goal parameters
			losedate (number) - Unix timestamp of derailment. When you'll be off the road if nothing is reported.
			panic (number) - Panic threshold. How long before derailment to panic. Default: 54000 (15 hours).
			queued (boolean) - Whether the graph is currently being updated to reflect new data.
			secret (boolean) - Whether you have to be signed in as owner of the goal to view it. Default: false.
			datapublic (boolean) - Whether you have to be signed in as the owner of the goal to view the datapoints. Default: false.
			datapoints (array of Datapoints) - The datapoints for this goal.
			numpts (number) - Number of datapoints.
			pledge (number) - Amount pledged (USD) on the goal.
			initday (number) - Unix timestamp (in seconds) of the start of the yellow brick road.
			initval (number) - The y-value of the start of the yellow brick road.
			curday (number) - Unix timestamp (in seconds) of the end of the yellow brick road, i.e., the most recent (inferred) datapoint.
			curval (number) - The value of the most recent datapoint.
			lastday (number) - Unix timestamp (in seconds) of the last (explicitly entered) datapoint.
			runits (string) - Rate units. One of y, m, w, d, h indicating that the rate of the yellow brick road is yearly, monthly, weekly, daily, or hourly.
			yaw (number) - Good side of the road. I.e., the side of the road (+1/-1 = above/below) that makes you say "yay".
			dir (number) - Direction the road is sloping, usually the same as yaw.
			lane (number) - Where you are with respect to the yellow brick road (2 or more = above the road, 1 = top lane, -1 = bottom lane, -2 or less = below the road).
			mathishard (array of 3 numbers) - The goaldate, goalval, and rate - all filled in. (You specify 2 out of 3 and can check this if you want Beeminder to do the math for you on inferring the third one.)
			headsum (string) - Summary of where you are with respect to the yellow brick road, e.g., "Right on track in the top lane".
			limsum (string) - Summary of what you need to do to eke by, e.g., "+2 within 1 day".
			exprd (boolean) - Exponential road; interpret rate as fractional, not absolute, change.
			kyoom (boolean) - Cumulative; plot values as the sum of all those entered so far, aka auto-summing.
			odom (boolean) - Treat zeros as accidental odometer resets.
			edgy (boolean) - Put the initial point on the road edge instead of centerline.
			noisy (boolean) - Compute road width based on data, not just road rate.
			aggday (string) - How to aggregate points on the same day, eg, min/max/mean.
			steppy (boolean) - Join dots with purple steppy-style line.
			rosy (boolean) - Show the rose-colored dots and connecting line.
			movingav (boolean) - Show moving average line superimposed on the data.
			aura (boolean) - Show turquoise swath, aka blue-green aura.
			frozen (boolean) - Whether the goal is currently frozen and therefore must be restarted before continuing to accept data.
			won (boolean) - Whether the goal has been successfully completed
			lost (boolean) - Whether the goal is currently off track
			contract (dictionary) - Dictionary with two attributes. amount is the amount at risk on the contract, and stepdown_at is a Unix timestamp of when the contract is scheduled to revert to the next lowest pledge amount. null indicates that it is not scheduled to revert.
			road (array) - Array of tuples that can be used to construct the Yellow Brick Road. This field is also known as the road matrix. Each tuple specifies 2 out of 3 of [time, goal, rate]. To construct the road, start with a known starting point (time, value) and then each row of the road matrix specifies 2 out of 3 of {t,v,r} which gives the segment ending at time t. You can walk forward filling in the missing 1-out-of-3 from the (time, value) in the previous row.
			delta_text (string) - The text that describes how far the goal is from each lane of the road - the same as appears to the upper right of a goal's graph. If the goal is on the good side of a given lane, the ? character will appear.
	"""


	def get_goal (self, slug):
		"""
			Get goal according to goal name (slug)
		"""

		url = "%s/users/%s/goals/%s.json" % (self.base_url, self.username, slug)
		values = {
					"auth_token" : self.auth_token
		}
		result = self.call_api (url, values, "GET")
		return result



	def get_all_goals (self):
		"""
			Get all goals
		"""

		url = "%s/users/%s/goals.json" % (self.base_url, self.username)
		values = {
					"auth_token" : self.auth_token
		}
		result = self.call_api (url, values, "GET")
		return result


	def create_goal (self, slug, title, goal_type, goaldate, goalval, rate, initval, panic = 54000, secret = False, datapublic = False, dryrun = False):
		"""
			Create goal
		"""

		url = "%s/users/%s/goals.json" % (self.base_url, self.username);
		if (goal_type == "hustler" or goal_type == "drinker"):
			initval = 0;
		if (goal_type == "hustler" or goal_type == "biker" or goal_type == "fatloser" or goal_type == "gainer" or goal_type == "inboxer" or goal_type == "drinker" or goal_type == "custom"):
			values = {
				"auth_token" : self.auth_token,
				"slug" : slug,
				"title" : title,
				"goal_type" : goal_type, # hustler - Do More, biker - Odometer, fatloser - Weight Loss, gainer - Gain Weight, inboxer - Inbox Fewer, drinker - Do Less, custom - full access
				"goaldate" : goaldate,
				"goalval" : goalval,
				"rate" : rate,
				"initval" : initval,
				"panic" : panic,
				"secret" : secret,
				"datapublic" : datapublic,
				"dryrun" : dryrun
			}
			result = self.call_api (url, values, "POST")
			return result
		return ""


	def update_goal (self, **kwargs):
		"""
			Update goal (uses key-value arguments)
		"""
		url = "%s/users/%s/goals.json" % (self.base_url, self.username)
		values = {
			"auth_token" : self.auth_token
		}
		for k, v in kwargs.iteritems():
			if k == "slug":
				values["slug"] = v
			elif k == "title":
				values["title"] = v
			elif k == "panic":
				values["panic"] = v
			elif k == "secret":
				values["secret"] = v
			elif k == "datapublic":
				values["datapublic"] = v
		result = self.call_api (url, values, "PUT")
		return result


	def update_road (self, **kwargs):
		"""
			Update road (needs 2 or more arguments)
		"""

		url = ""
		values = {
			"auth_token" : self.auth_token
		}
		for k, v in kwargs.iteritems():
			if k == "slug":
				url = "%s/users/%s/goals/%s/dial_road.json" % (self.base_url, self.username, v)
			elif k == "rate":
				values["rate"] = v
			elif k == "goaldate":
				values["goaldate"] = v
			elif k == "goalval":
				values["goalval"] = v
		if url:
			if len (values) >= 3:
				result = self.call_api (url, values, "POST")
				return result
		return ""


	def short_circuit (self, slug):
		"""
			PAY CURRENT PLEDGE and increase its level
		"""

		url = "%s/users/%s/goals/%s/shortcircuit.json" % (self.base_url, self.username, slug)
		values = {
			"auth_token" : self.auth_token
		}
		result = self.call_api (url, values, "POST")
		return result


	def stepdown (self, slug):
		"""
			Decrease pledge level (week delay) SUBJECT TO AKRASIA HORIZON
		"""

		url = "%s/users/%s/goals/%s/stepdown.json" % (self.base_url, self.username, slug)
		values = {
			"auth_token" : self.auth_token
		}
		result = self.call_api (url, values, "POST")
		return result


	def cancel_stepdown (self, slug):
		"""
			Cancel a pending stepdown
		"""

		url = "%s/users/%s/goals/%s/cancel_stepdown.json" % (self.base_url, self.username, slug)
		values = {
			"auth_token" : self.auth_token
		}
		result = self.call_api (url, values, "POST")
		return result


	def refresh_graph (self, slug):
		"""
			Refresh graph
		"""

		url = "%s/users/%s/goals/%s/refresh_graph.json" % (self.base_url, self.username, slug)
		values = {
			"auth_token" : self.auth_token
		}
		result = self.call_api (url, values, "GET")
		return result


	"""
		Datapoint attributes:
			timestamp (number) - The unix time (in seconds) of the datapoint.
			value (number) - The value, e.g., how much you weighed on the day indicated by the timestamp.
			comment (string) - An optional comment about the datapoint.
			id (string) - A unique ID, used to identify a datapoint when deleting or editing it.
			updated_at (number) - The unix time that this datapoint was entered or last updated.
			requestid (string) - If a datapoint was created via the API and this parameter was included, it will be echoed back.
	"""


	def get_datapoints (self, slug):
		"""
			Get all datapoints
		"""
		url = "%s/users/%s/goals/%s/datapoints.json" % (self.base_url, self.username, slug)
		values = {
			"auth_token" : self.auth_token
		}
		result = self.call_api (url, values, "GET")
		return result


	def create_datapoint (self, slug, value, comment = '', sendmail = 'false'):
		"""
			Create point
		"""

		url = "%s/users/%s/goals/%s/datapoints.json" % (self.base_url, self.username, slug)
		values = {
			"auth_token" : self.auth_token,
			"value" : value,
			"comment" : comment,
			"sendmail" : sendmail
		}
		result = self.call_api (url, values, "POST")
		return result


	def update_datapoint (self, **kwargs):
		"""
			Update datapoint
		"""

		args = {}
		values = {
			"auth_token" : self.auth_token
		}
		for k, v in kwargs.iteritems():
			if k == "slug":
				args["slug"] = v
			elif k == "id":
				args["datapoint_id"] = v
			elif k == "timestamp":
				values["timestamp"] = v
			elif k == "value":
				values["value"] = v
			elif k == "comment":
				values["comment"] = v
		if len (args) == 2:
			url = "%s/users/%s/goals/%s/datapoints/%s.json" % (self.base_url, self.username, args["slug"], args["datapoint_id"])
			result = self.call_api (url, values, "PUT")
			return result
		return ""


	def delete_datapoint (self, slug, datapoint_id):
		"""
			Delete datapoint
		"""

		url = "%s/users/%s/goals/%s/datapoints/%s.json" % (self.base_url, self.username, slug, datapoint_id)
		values = {
			"auth_token" : self.auth_token
		}
		result = self.call_api (url, values, "DELETE")
		return result


	# TODO: Charge requests


	def call_api (self, url, values, method = "GET"):
		"""
			Send request
		"""

		result = ""
		data = urllib.urlencode (values)
		if method == "GET":
			print url + "?" + data
			response = urllib2.urlopen (url + "?" + data)
			result = response.read()
		elif method == "POST":
			req = urllib2.Request (url, data)
			response = urllib2.urlopen (req)
			result = response.read()
		elif method == "PUT":
			opener = urllib2.build_opener (urllib2.HTTPHandler)
			request = urllib2.Request (url, data)
			request.get_method = lambda: 'PUT'
			response = urllib2.urlopen (request)
			result = response.read()
		elif method == "DELETE":
			opener = urllib2.build_opener (urllib2.HTTPHandler)
			request = urllib2.Request (url, data)
			request.get_method = lambda: 'DELETE'
			response = urllib2.urlopen (request)
			result = response.read()
		return result