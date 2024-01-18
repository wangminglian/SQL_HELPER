from http import HTTPStatus
from dashscope import Generation
import dashscope

dashscope.api_key = 'sk-dd4b044f7967499aa3d7f9bfdceaabf9'

with open('E:\思特奇\学习笔记\数仓任务\关于上线七站八所运营报表的需求.sql','r',encoding='utf8') as f:
    sql = '\n'.join(f.readlines())

print(sql)
def call_with_messages():
    messages = [{'role': 'system', 'content': '你是达摩院的生活助手机器人。'},
                {'role': 'user', 'content': f'${sql}，介绍一下这个SQL的表关联关系'}]
    gen = Generation()
    response = gen.call(
        Generation.Models.qwen_v1,
        messages=messages,
        result_format='message', # set the result is message format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s'%(
            response.request_id, response.status_code,
            response.code, response.message
        ))

if __name__ == '__main__':
    call_with_messages()