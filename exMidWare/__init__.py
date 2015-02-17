__author__ = 'blaczom'

class exOpMid(object):
  def process_request(self, request):
    request.session["lastErr"] = []
