import base64
import json
import urllib.parse
import urllib3
import json
from qiniu import Auth, put_file, etag
import qiniu.config
from qiniu import CdnManager

# 账户ak，sk【七牛云配置项1】
access_key = ''
secret_key = ''

node = [{
    "add":"202.202.202.202",
    "aid":0,
    "host":"www.tencent.com",
    "id":"86cd9afe-09ca-4e35-a914-edf5d73c2fc7",
    "net":"ws",
    "path":"/RKZeGQ",
    "port":443,
    "ps":"Hostloc",
    "tls":"tls",
    "type":"none",
    "v":2
},{
    "add":"101.101.101.101",
    "aid":0,
    "host":"www.aliyun.com",
    "id":"fd7e791c-3dbe-rh48-a842-233deab6c67b",
    "net":"ws",
    "path":"/XwMad4IwhS",
    "port":443,
    "ps":"MJJ",
    "tls":"tls",
    "type":"none",
    "v":2
}]

def get_optimization_ip():
    # https://github.com/ddgth/cf2dns
    # 以下是测试KEY，要用最新的，自己去买。我不是宣传，你也可以用测试KEY
    KEY = 'o1zrmHAF'
    try:
        http = urllib3.PoolManager()
        headers = headers = {'Content-Type': 'application/json'}
        data = {"key": KEY}
        data = json.dumps(data).encode()
        response = http.request('POST','https://api.hostmonit.com/get_optimization_ip',body=data, headers=headers)
        # 根据网络修改'CM'字段.【CM移动、CU联通、CT电信】
        return json.loads(response.data.decode('utf-8'))["info"]["CM"][0]['ip']
    except Exception as e:
        print(e)
        return None
    
def upload_file_to_qiniu():
    q = Auth(access_key, secret_key)
    #要上传的空间【七牛云配置项2】
    bucket_name = '你的七牛云空间名'
    #上传后保存的文件名
    key = 'node'
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    #要上传文件的本地路径
    localfile = './node'
    ret, info = put_file(token, key, localfile, version='v2') 
    print(ret)

def refresh_cache():
    auth = qiniu.Auth(access_key=access_key, secret_key=secret_key)
    cdn_manager = CdnManager(auth)

    # 需要刷新的文件链接【七牛云配置项3】
    urls = [
        'http://xxx.zxxxx.xxxx/node', # 你的文件上传后得到的访问地址
    ]
    # URL刷新链接
    refresh_url_result = cdn_manager.refresh_urls(urls)
    
    print(refresh_url_result)
    
if __name__ == '__main__':
    # 获得IP
    IP = get_optimization_ip()
    node_url = ''
    # 生成
    for i in node:
        i['add'] = IP
        json_string = json.dumps(i)
        encodestr = base64.b64encode(bytes(str(json_string).encode('utf-8')))
        node_url += "vmess://" + str(encodestr,'utf-8') +"\r\n"
    with open("node","w") as f:
        f.write(str(base64.b64encode(bytes(str(node_url).encode('utf-8'))),'utf-8'))
    #上传
    upload_file_to_qiniu()
    # 刷新缓存
    refresh_cache()
    