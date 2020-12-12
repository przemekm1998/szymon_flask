import json
import os

import werkzeug
from flask import Response
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename

from api.tools import perform_istft


class ISFFTResource(Resource):
    """ ISFFT api resource """

    @property
    def req_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('audio', type=werkzeug.datastructures.FileStorage,
                            location='files')

        return parser

    def post(self):
        args = self.req_parser.parse_args()
        audio = args['audio']
        filename = secure_filename(audio.filename)
        path = os.path.join('files', filename)
        audio.save(path)

        data = perform_istft(path)

        return Response(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
