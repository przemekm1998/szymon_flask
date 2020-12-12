from api.resources import ISFFTResource


def initialize_routes(api):
    api.add_resource(ISFFTResource, '/')
