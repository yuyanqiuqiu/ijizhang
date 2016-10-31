# coding:utf-8 

from flask import Flask, request, make_response
import time
import hashlib
import xml.etree.ElementTree as ET
import jieba

TOKEN = 'ijizhang'


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
	if request.method == 'GET':
		query = request.args
		signature = query.get('signature', '')
		timestamp = query.get('timestamp', '')
		nonce = query.get('nonce', '')
		echostr = query.get('echostr', '')

		array = [timestamp, nonce, TOKEN]
		array.sort()

		s = ''.join(array)

		if(hashlib.sha1(s).hexdigest() == signature):
			return make_response(echostr)
		else:
			return 'laile'

	else:
		xml_recv = ET.fromstring(request.data)
		toUserName = xml_recv.find('ToUserName').text
		fromUserName = xml_recv.find('FromUserName').text
		content = xml_recv.find('Content').text

		print fromUserName

		seg_list = jieba.lcut(content)

		s = ','.join(seg_list)

		reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName>" \
						"<FromUserName><![CDATA[%s]]></FromUserName>"\
						"<CreateTime>%s</CreateTime>"\
						"<MsgType><![CDATA[text]]></MsgType>"\
						"<Content><![CDATA[%s]]></Content>"\
						"<FuncFlag>0</FuncFlag></xml>"
		response = make_response(reply % (fromUserName, toUserName, 
								str(int(time.time())), s ))
		response.content_type = 'application/xml'
		return response


if __name__ == '__main__':
	app.run(debug=True)