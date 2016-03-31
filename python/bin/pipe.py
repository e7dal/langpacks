import base64
import json
import sys
import traceback
from algorithm import apply
from six.moves import input

# TODO import the algorithm apply method so this doesn't crash

FIFO_PATH = '/tmp/algoout'

def main():
    while True:
        try:
            line = input()
        except EOFError:
            break

        request = json.loads(line)
        response = get_response(request)

        # Add final newline delimeter and flush stdout before writing back response
        sys.stdout.write('\n')
        sys.stdout.flush()

        with open(FIFO_PATH, 'w') as f:
            f.write(json.dumps(response))
            f.write('\n')


def get_response(request):
    try:
        result = call_algorithm(request)
        if isinstance(result, bytearray):
            content_type = 'binary'
            result = base64.b64encode(result)
        else:
            content_type = 'json'

        response = {
            'result': result,
            'metadata': {
                'content_type': content_type
            }
        }
    except Exception as e:
        _, _, exc_traceback = sys.exc_info()

        response = {
            'message': str(e),
            'stacktrace': traceback.format_exc(exc_traceback)
        }

    return response

def call_algorithm(request):
    if request['content_type'] in ['text', 'json']:
        data = request['data']
    elif request['content_type'] == 'binary':
        data = bytearray(base64.b64decode(request['data']))
    else:
        raise Exception("Invalid content_type: {}".format(request['content_type']))

    return apply(data)

if __name__ == '__main__':
    main()
