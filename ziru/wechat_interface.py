import itchat
import pymysql

def query_mysql(m_str):
    str_list = m_str.split(' ')
    if len(str_list)<2:
        return '查询文字的格式不正确！'
    query = 'SELECT * FROM ziroom WHERE ziroom.%s AND ziroom.metro_dist like"%s"' % \
            (str_list[1], str_list[0])
    npos = query.find('"')
    query2 = query[:npos + 1] + '%' + query[npos + 1:-1] + '%' + query[-1]

    try:
        cursor.execute(query2)
    except:
        return '查询文字的格式不正确！'

    data = cursor.fetchall()
    return data

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    #只处理发给自己的字符串
    if msg['ToUserName'] == 'filehelper':
        str_tuple = query_mysql(msg['Content'])
        if isinstance(str_tuple, str):
            itchat.send(str_tuple, toUserName='filehelper')
        else:
            for s in str_tuple:
                s1 = list(s)
                s1[7] = str(s1[7]) #第七个元素为价格，应转成字符串
                s1.pop(0)  #删掉第一个索引
                itchat.send(" ".join(s1), toUserName='filehelper')


if __name__ == '__main__':
    db = pymysql.connect("localhost", "xxx", "xxx", "db", use_unicode=True, charset="utf8")
    cursor = db.cursor()


    itchat.auto_login(hotReload=True)
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    itchat.run()


