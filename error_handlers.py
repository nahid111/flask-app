def error_handler(app):

    @app.errorhandler(Exception)
    def handle_exception(e):
        if e.__class__.__name__ == 'NotFound':
            return {'success': False, 'error': 'Not Found'}, 404
        if e.__class__.__name__ == 'DoesNotExist':
            return {'success': False, 'error': 'Data Not Found'}, 404
        if e.__class__.__name__ == 'ValidationError':
            return {'success': False, 'error': str(e)}, 400
        if e.__class__.__name__ == 'NotUniqueError':
            return {'success': False, 'error': 'Duplicate Field Value Entered'}, 400
        if e.__class__.__name__ == 'KeyError':
            return {'success': False, 'error': str(e) + ' field is missing'}, 400

        print('\x1b[91m' + e.__class__.__name__ + ': ' + str(e) + '\x1b[0m')
        return {'success': False, 'error': 'Something Went Wrong'}, 500
