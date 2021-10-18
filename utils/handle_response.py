def successResponse(success, data):
  return { 'success': success, 'data': data }

def errorResponse(status, error):
  return { 'success': False, 'status': status, 'error': error }