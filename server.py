import json
from sanic import Sanic
from urllib import parse
from tools.weibo import weibo
app = Sanic('qqbot')


@app.websocket('/qqbot')
async def qqbot(request, ws):
    """QQ机器人"""
    while True:
        data = await ws.recv()
        data = json.loads(data)
        print(json.dumps(data, indent=4, ensure_ascii=False))
        # if 判断是群消息且文本消息不为空
        
        #  标准格式
        # if data.get('message_type') == 'group' and data.get('raw_message'):
        #     raw_message = data['raw_message']
        #     msg = raw_message[::-1]
        #     ret = {
        #         'action': 'send_group_msg',
        #         'params': {
        #             'group_id': data['group_id'],
        #             'message': msg,
        #         }
        #     }
        #     await ws.send(json.dumps(ret))
        
        # 加群欢迎
        if data.get('post_type') and data.get('notice_type') == 'group_increase':
            qq_num = data.get('user_id')
            msg = f'[CQ:at,qq={qq_num}]主动用QQ或微信加你的都是想骗你掏钱的,群仅提供交流.新人如果没有Python基础,可以看点击群文件--完全不会Python点这里里面有配置视频 ヾ(≧O≦)〃嗷~ \n目前被骗总金额: 9000+，警钟长鸣！'
            ret = {
                'action': 'send_group_msg',
                'params': {
                    'group_id': data['group_id'],
                    'message': msg,
                }
            }
            await ws.send(json.dumps(ret))
        # 看看谁跑了
        elif data.get('post_type') and data.get('notice_type') == 'group_decrease':
            qq_num = data.get('user_id')
            msg = f'[CQ:at,qq={qq_num}]不知道为啥退群了.╮（╯＿╰）╭'
            ret = {
                'action': 'send_group_msg',
                'params': {
                    'group_id': data['group_id'],
                    'message': msg,
                }
            }
            await ws.send(json.dumps(ret)) 
        # 关键字
        elif data.get('post_type') == 'message' and data.get('message_type') == 'group':
            if '[CQ:at,qq=改成你的qq号]' in data.get('raw_message'):
                key_word = data.get('raw_message').split('[CQ:at,qq=改成你的qq号]')[-1]
                
                search_dic = {
                    'b站.': r'b站搜索结果如下: https://search.bilibili.com/all?keyword={key_word}',
                    'pip': r'修改pip源指令: pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple',
                    '提问的智慧': r'不知道怎么提问点这里 https://lug.ustc.edu.cn/wiki/doc/smart-questions/',
                    'ps1':r'set-executionpolicy remotesigned',
                    #'热搜':f'{"".join(weibo())}',
                    #'pandas.': r'https://pandas.pydata.org/docs/search.html?q={key_word}#',
                    #'numpy.': r'https://numpy.org/doc/stable/search.html?q={key_word}#',
                }
                if key_word in search_dic.keys():
                    for k,v in search_dic.items():
                        if k in key_word:
                            if k.endswith('.'):
                                search_word = key_word.split(k)[-1]
                                search_word = parse.quote(search_word, encoding='utf-8')
                                msg = v.replace('{key_word}',search_word)
                            else:
                                msg = v

                            ret = {
                                'action': 'send_group_msg',
                                'params': {
                                    'group_id': data['group_id'],
                                    'message': msg,
                                }
                            }
                            await ws.send(json.dumps(ret))
                            break
                else:
                    msg = '我听不懂。等我慢慢进化'
                    ret = {
                        'action': 'send_group_msg',
                        'params': {
                            'group_id': data['group_id'],
                            'message': msg,
                        }
                    }    
    
    

if __name__ == '__main__':
    app.run(debug=True, auto_reload=True)
