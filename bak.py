from cpgmgt_client_object import CPGMgt_Client_Object
from flask import jsonify, request,Response,abort
from flask.ext.login import api_login_required
from api import api, compile_exception_msg
from dbus import DBusException

@api.route('/network/wifimode', methods=['GET'])
@api_login_required
def network_wifimode():
    if request.method == "GET":
        client = CPGMgt_Client_Object()
        try:
            reply = client.method_call_native("/com/cisco/cpg/WiFiMode", None, "Get", str("mode"))
        except DBusException as inst:
            return compile_exception_msg(inst), 500
        return jsonify({'mode':reply}) 
    elif request.method == "PUT":
        client = CPGMgt_Client_Object()
        req_json = request.get_json(force=True)
        try:
            mode =  str(req_json['mode'])
            reply = client.method_call_native("/com/cisco/cpg/WiFiMode", None, "Set","mode", mode)
        except DBusException as inst:
            return compile_exception_msg(inst), 500
        return Response(status = 200)
    else :
        abort(404)

@api.route('/network/wifimode', methods=['PUT'])
@api_login_required
def set_network_wifimode():
    client = CPGMgt_Client_Object()
    req_json = request.get_json(force=True)
    try:
        mode =  str(req_json['mode'])
        reply = client.method_call_native("/com/cisco/cpg/WiFiMode", None, "Set","mode", mode)
    except DBusException as inst:
        return compile_exception_msg(inst), 500
    return Response(status = 200)
