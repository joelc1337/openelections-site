import csv
import json
import StringIO
import webapp2

from google.appengine.ext import ndb

def csv_string_to_dict(csv_data):
    precinct_to_votes = {}
    is_header = True
    f = StringIO.StringIO(csv_data)
    rows = csv.reader(f, delimiter=',')
    for row in rows:
        if is_header:
          is_header = False
          continue
        office = row[2]
        if office != 'President':
          continue
        county = row[0]
        precinct = row[1]
        key = county + '__' + precinct
        entry = precinct_to_votes.get(key, {})
        precinct_to_votes[key] = entry
        entry['county'] = county
        entry['precinct'] = precinct

        precinct_votes = entry.get('votes', {})
        entry['votes'] = precinct_votes

        candidate = row[5]
        votes = int(row[6])
        if candidate in precinct_votes:
          precinct_votes[candidate] += votes
        else:
          precinct_votes[candidate] = votes
    return precinct_to_votes

class PrecinctVotes(ndb.Model):
    precinct = ndb.StringProperty()
    county = ndb.StringProperty()
    votes = ndb.JsonProperty()

class UploadHandler(webapp2.RequestHandler):
    def post(self):
        csv_data = self.request.POST.get('csv_file').file.read()
        precinct_to_votes = csv_string_to_dict(csv_data)
        for key in precinct_to_votes:
            entry = precinct_to_votes[key]
            precinct_id = precinct_to_votes['county'] + '__' + precinct_to_votes['precinct']
            # TODO: create PrecinctVotes objects (set id, county, percinct, & votes)
            # and save with .put()
        self.response.out.write('Upload successful')

class PrecinctHandler(webapp2.RequestHandler):
    def get(self):
        results = []
        # TODO: Use PrecinctVotes.query() to get all precints and then append
        # to the results list as a dictionary (use to_dict())
        self.response.out.write(json.dumps(results))
        self.response.headers.add_header('Content-Type', 'application/json')

app = webapp2.WSGIApplication([
    ('/upload', UploadHandler),
    ('/precincts', PrecinctHandler)
], debug=True)
