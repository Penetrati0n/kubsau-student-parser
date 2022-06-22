import os, dotenv, json
dotenv.load_dotenv()

from flask import Flask, request
from services.group_service import GroupService
from services.scrap_service import ScrapService
from services.parse_service import ParseService

default_connection_string = os.getenv('DefaulConnection')
group_service = GroupService(dsn=default_connection_string)

server = Flask(__name__)

@server.route('/students', methods=['GET'])
def get_students():
    if 'group' not in request.args:
        return {'success': False, 'err': {'code': 'no_group_arg_found'}}, 200
    group = request.args['group'].upper()
    group_uuid = group_service.get_group_uuid(group)
    if not group_uuid:
        return {'success': False, 'err': {'code': 'group_not_found'}}, 200
    page_raw = ScrapService.scrap_group(uuid=group_uuid)
    if not page_raw:
        return {'success': False, 'err': {'code': 'group_loading_error'}}, 200
    try:
        students = ParseService.parse_students(page_raw)
    except:
        return {'success': False, 'err': {'code': 'students_parsing_error'}}, 200
    return json.dumps({'success': True, 'result': students}, ensure_ascii=False), 200

@server.route('/groups', methods=['GET'])
def get_groups():
    groups = group_service.get_all_groups()
    return json.dumps({'success': True, 'result': groups}, ensure_ascii=False), 200

server.run(host='0.0.0.0', port=os.getenv('PORT', 8080))
