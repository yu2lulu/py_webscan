from requests_html import HTMLSession
from urllib import parse as urlparse
import optparse
import json
indexURL="http://www.yu2lulu.xyz/"
output=""
session = HTMLSession()

headers={
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}

urls=[]
info=[]
domain=[]

blackitems=[
    'jpg',
    'png',
    'gif',
    'css',
    'js'
]


Usage = 'python3.6 main.py -url http://www.qq.com/ -o host|url '
Parser = optparse.OptionParser(usage=Usage)

def usage():
     Parser.add_option("-u", "--url", dest="url", default="", help=r'扫描的地址')
     Parser.add_option("-o", "--output", dest="output", help=r"输出内容, host:域名信息，url 路径信息")

def fetchURL():
    print("Running....Please Waiting....")
    # 获取url链接入 urls列表中保存
    while len(urls)!=0:
        url=urls[0]
        del urls[0]
        r = session.get(url, headers=headers)
        for item in r.html.absolute_links:
            tmpDict={}
            data=urlparse.urlparse(item)
            tmpDict['scheme']=data[0]
            tmpDict['netloc']=data[1]
            tmpDict['path']=data[2]
            tmpDict['params']=data[3]
            tmpDict['query']=data[4]
            tmpDict['fragment']=data[5]
            tmpDict['url']=item
            if item.endswith("/"):
                tmpDict['suffix']='/'
            else:
                tmpDict['suffix'] =tmpDict['path'].rsplit(".")[-1]


            if tmpDict['suffix'].lower() in blackitems:
                pass
            else:
                if tmpDict['netloc']==info[0]['netloc']:
                    infoNum=len(info)
                    num=0
                    while(num<infoNum):
                        if info[num]['path']==tmpDict['path']:
                            num=infoNum+100000
                        else:
                            num+=1

                    if num==infoNum:
                        info.append(tmpDict)
                        urls.append(item)

                else:
                    domain.append(tmpDict['netloc'])


def printResult():
    if output.lower()=='host':
        for item in set(domain):
            print(item)

    if output.lower()=='url':
        for item in info:
            print(item)

    return

def main():
    # 请求url地址的主机信息
    hostinfo=urlparse.urlparse(indexURL)

    tmp={
        'scheme':hostinfo[0],
        'netloc':hostinfo[1],
        'path':hostinfo[2],
        'params':hostinfo[3],
        'query':hostinfo[4],
        'fragment':hostinfo[5],
        'url':indexURL
    }
    info.append(tmp)
    urls.append(indexURL)
    domain.append(hostinfo[1])

    fetchURL()


    # for line in info:
    #     print(line)

    printResult()



if __name__=="__main__":
    usage()
    (option, args) = Parser.parse_args()
    if option.url==None:
        print(Usage)
        exit()
    if option.output==None:
        print(Usage)
        exit()

    indexURL=option.url
    output=option.output
    # print(option)
    main()