# -*- coding: UTF-8 -*-
import requests as req
import json,time,random

Acc=open('ACCOUNT.txt','r')
account=json.loads(Acc.read())
Acc.close()
redirect_uri = r'https://login.microsoftonline.com/common/oauth2/nativeclient'

log_list=[0]
###########################
# config选项说明
# 0：关闭  ， 1：开启
# api_rand：是否随机排序api （开启随机抽取12个，关闭默认初版10个）。默认1开启
# rounds: 轮数，即每次启动跑几轮。
# rounds_delay: 是否开启每轮之间的随机延时，后面两参数代表延时的区间。默认0关闭
# api_delay: 是否开启api之间的延时，默认0关闭
# app_delay: 是否开启账号之间的延时，默认0关闭
########################################
config = {
         'api_rand': 1,
         'rounds': 3,
         'rounds_delay': [1,10,60],
         'api_delay': [1,2,6],
         'app_delay': [0,30,60],
         }
api_list = [
           r'https://graph.microsoft.com/v1.0/me/',
           r'https://graph.microsoft.com/v1.0/users',
           r'https://graph.microsoft.com/v1.0/me/people',
           r'https://graph.microsoft.com/v1.0/groups',
           r'https://graph.microsoft.com/v1.0/me/contacts',
           r'https://graph.microsoft.com/v1.0/me/drive/root',
           r'https://graph.microsoft.com/v1.0/me/drive/root/children',
           r'https://graph.microsoft.com/v1.0/drive/root',
           r'https://graph.microsoft.com/v1.0/me/drive',
           r'https://graph.microsoft.com/v1.0/me/drive/recent',
           r'https://graph.microsoft.com/v1.0/me/drive/sharedWithMe',
           r'https://graph.microsoft.com/v1.0/me/calendars',
           r'https://graph.microsoft.com/v1.0/me/events',
           r'https://graph.microsoft.com/v1.0/sites/root',
           r'https://graph.microsoft.com/v1.0/sites/root/sites',
           r'https://graph.microsoft.com/v1.0/sites/root/drives',
           r'https://graph.microsoft.com/v1.0/sites/root/columns',
           r'https://graph.microsoft.com/v1.0/me/onenote/notebooks',
           r'https://graph.microsoft.com/v1.0/me/onenote/sections',
           r'https://graph.microsoft.com/v1.0/me/onenote/pages',
           r'https://graph.microsoft.com/v1.0/me/messages',
           r'https://graph.microsoft.com/v1.0/me/mailFolders',
           r'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
           r'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
           r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
           r"https://graph.microsoft.com/v1.0/me/messages?$filter=importance eq 'high'",
           r'https://graph.microsoft.com/v1.0/me/messages?$search="hello world"',
           r'https://graph.microsoft.com/beta/me/messages?$select=internetMessageHeaders&$top',
           ]

#微软access_token获取
def getmstoken():
    #try:except?
    headers={
            'Content-Type':'application/x-www-form-urlencoded'
            }
    data={
         'grant_type': 'refresh_token',
         'refresh_token': ms_token,
         'client_id':client_id,
         'client_secret':client_secret,
         'redirect_uri':redirect_uri,
         }
    for retry_ in range(4):
        html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token',data=data,headers=headers)
        if html.status_code < 300:
            print('微软密钥获取成功')
            break
        else:
            if retry_ == 3:
                print('微软密钥获取失败\n')
    jsontxt = json.loads(html.text)
    return jsontxt['access_token']
    
#延时
def timeDelay(xdelay):
    if config[xdelay][0] == 1:
        time.sleep(random.randint(config[xdelay][1],config[xdelay][2]))

#调用函数
def runapi():
    timeDelay('api_delay')
    global access_token
    headers={
            'Authorization': 'bearer ' + access_token,
            'Content-Type': 'application/json'
            }
    #重试
    for b in range(len(apilist)):
        for retry_ in range(4):
            apiget=req.get(api_list[apilist[b]],headers=headers)
            if apiget.status_code == 200:
                print('    第'+str(apilist[b])+"号api调用成功")
                break
            else:
                if retry_ == 3:
                    log_list=log_list+1
                    print('    pass')
                    
#一次性获取access_token，降低获取率
client_id=account['client_id']
client_secret=account['client_secret']
ms_token=account['ms_token']
access_token=getmstoken()

#随机api序列
fixed_api=[0,1,5,6,20,21]
#保证抽取到outlook,onedrive的api
ex_api=[2,3,4,7,8,9,10,22,23,24,25,26,27,13,14,15,16,17,18,19,11,12]
#额外抽取填充的api
fixed_api.extend(random.sample(ex_api,6))
random.shuffle(fixed_api)
final_list=fixed_api

#实际运行
print("如果api数量少于规定值，则是api赋权没有弄好，或者是onedrive还没有初始化成功。前者请重新赋权，后者请稍等几天")
print('共 '+str(config['rounds'])+' 轮') 
for r in range(1,config['rounds']+1):
    timeDelay('rounds_delay')
    timeDelay('app_delay')
    client_id=account['client_id']
    client_secret=account['client_secret']
    ms_token=account['ms_token']
    print('\n'+'第'+str(r)+'轮 '+time.asctime(time.localtime(time.time()))+'\n')
    if config['api_rand'] == 1:
        print("已开启随机顺序,共十二个api,自己数")
        apilist=final_list
    else:
        print("原版顺序,共十个api,自己数")
        apilist=[5,9,8,1,20,24,23,6,21,22]
    runapi()
   