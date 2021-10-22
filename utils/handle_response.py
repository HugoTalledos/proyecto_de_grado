from flask import make_response

def successResponse(success, data):
  return { 'success': success, 'data': data }

def errorResponse(status, error):
  return make_response({ 'success': False, 'error': error }, status)