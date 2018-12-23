# -*- coding: utf-8 -*-

'''
修改记录：
20171007：增加分享关键词，以便把格式不规范的分享也整理出来
'''

import codecs
import os
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.parser import parse
import re

#-----------------------------------------------------------------------
#-----------------------配置信息----------------------------------------

#需要整理的QQ号
# '448064184':u'快乐人生',\
vip_qq_ids = ['28505355', '987422909', '2429246562', '3367537735', '914444602', '448693981', '8025709', '2932642365','408684144']

#QQ号和QQ昵称的对应关系
vip_qq_name_id = {'28505355':u'北京数学哥',
                  '987422909':u'妈妈爱牛牛',\
                  '2429246562':u'青岛—小禾苗',\
                  '3367537735':u'后知后觉已十年-上海',\
                  '448693981':u'河南-蔚蓝',\
                  '8025709':u'古龙水2只票-北京',\
                  '2932642365':u'北京小白',\
                  '408684144':u'江苏-顺势牛牛',\
                  '914444602':u'北京飘落的长发'}     
#QQ群信息
#group_name = r"顺势投资核心组(477653766)"
group_name = r"顺势投资核心组"

#指定原始QQ群消息历史记录所在位置
qq_record_file_path = "h:/08t2ff/02QQ/20171007/"
#qq_record_file_path = "h:/08t2ff/02QQ/20170820_test/4/"


#QQ留言时间段，为了防止重复记录消息，起始时间在这里手写指定
start_date = "20170924"
end_date = ""

#-----------------------------------------------------------------------

def get_time_and_id(msg):
    time = ""
    id = ""
    line_pattern = re.compile("(\d){4}-(\d){2}-(\d){2}.+\)")
    time_pattern = re.compile("(\d){4}-(\d){2}-(\d){2} (\d){2}:(\d){2}:(\d){2}")
    id_pattern = re.compile("(?<=\()\d+(?=\))")
    
    if line_pattern.search(msg):
        line = line_pattern.search(msg).group()
        if time_pattern.search(line):
            time = parse(time_pattern.search(line).group())
        if id_pattern.search(line):
            id = id_pattern.search(line).group()
    
    return time, id


def get_one_file_msgs(qq_record_file):
    file = codecs.open(qq_record_file, "r", "utf-8")
    lines = file.readlines()

    #获取所有消息记录
    msg_record = []
    msg = ''
    time = []
    id = []
    
    for line in lines:        
        msg = msg + line
        if '\r\n' == line:            
            msg_record.append(msg)
            tmp_time, tmp_id = get_time_and_id(msg)
            time.append(tmp_time)
            id.append(tmp_id)
            msg = ''   
    
    file.close()
    return time, id, msg_record


# 遍历指定目录，显示目录下的所有文件名
def get_all_qq_msgs(filepath):
    global end_date
    files =  os.listdir(filepath)   
    data = {'time':[], 'id':[], 'msg':[]}
    all_df = DataFrame(data)
    
    #合并所有消息记录文件
    for file in files:
        if group_name in file:            
            print(r"开始处理:%s\n" % file)
            time, id, msg = get_one_file_msgs(filepath+file)            
            data = {'time':time, 'id':id, 'msg':msg}
            #生成Dataframe
            df = DataFrame(data)
            all_df = pd.concat([all_df, df])               
            #去除重复
            all_df.drop_duplicates(['time', 'id'], inplace=True)
            #排序
            all_df.sort_values(by='time')
    
    #选取需要的时间段
    all_df = all_df.dropna()
    #print(all_df)
    sel_df = all_df[all_df.time >= parse(start_date)]
    #print(sel_df['time'].get_values())
    end_datetime = sel_df['time'].get_values()[-1]
    end_date = pd.to_datetime(str(end_datetime)).strftime("%Y%m%d")
    #print(end_date)
    
    #获取所有消息文字
    all_msgs = sel_df['msg'].get_values().tolist()
    
    return all_msgs

def save_all_msgs(all_msgs):
    global start_date
    global end_date
    fenxiang_list = []
    print(u"保存所有人消息...")

    #所有群消息汇总，以utf-8格式存入txt文件
    output_file = "顺势投资核心组[477653766]消息汇总(" + start_date + "-" + end_date + ")" + ".txt"
    file=codecs.open(qq_record_file_path+output_file, "w", "utf-8")
    for msg in all_msgs:
        file.write(msg)
        if "我的分享" in msg \
            or "我来分享" in msg \
            or "分享一个" in msg \
            or "分享完毕" in msg \
            or "分享结束" in msg:
            time, id = get_time_and_id(msg)
            if id not in fenxiang_list:
                fenxiang_list.append(id)
    file.close()   
        
    print(u"保存完成")
    print(fenxiang_list)
    return fenxiang_list

def save_share_story(shared_ids, all_msgs):
    global start_date
    global end_date
    
    all_share = ''
    
    print(u"开始整理财富故事分享...")

    #财富故事汇，以utf-8格式存入txt文件    
    output_file = "顺势投资核心组[477653766]财富故事汇(" + start_date + "-" + end_date + ")" + ".txt"
    file=codecs.open(qq_record_file_path+output_file, "w", "utf-8")
    
    for id in shared_ids:
        print("开始整理%s的分享" % id)
        state = 'end'
        one_share = ''
        one_share1 = ''
        #整理某个人的分享
        for msg in all_msgs:
            time, tmp_id = get_time_and_id(msg)  # @UnusedVariable
            if id == tmp_id:            
                if "我的分享" in msg or "我来分享" in msg or "分享一个" in msg:
                    state = 'begin'                
                    one_share += msg
                    one_share1 = msg
                    if "分享完毕" in msg or "分享结束" in msg:
                        state = 'end'
                elif "分享完毕" in msg or "分享结束" in msg:
                    one_share += msg
                    state = 'end'
                else:
                    if state == 'begin':
                        one_share += msg
                    else:
                        pass
                    
        #汇总所有人分享
        if "分享格式" not in one_share:
            if state == 'end':
                all_share += one_share
            else:
                all_share += one_share1           
                        
    file.write(all_share)
    file.close()
    print(u"财富故事完成")
    return

def save_msg_of_one_id(in_qqid, all_msgs):
    global start_date
    global end_date
    qqid = in_qqid
    print(u"开始整理"+vip_qq_name_id[qqid] + "(" + qqid + ")" + "的留言...")

    #以utf-8格式存入txt文件
    output_file = qq_record_file_path + u"单人消息记录[" + vip_qq_name_id[qqid] + "]" + "(" + start_date + "-" + end_date + ")" + ".txt"
    file=codecs.open(output_file, "w", "utf-8")
    for msg in all_msgs:
        #选取特定人的消息，以qq号为参数
        if qqid in msg:
            file.write(msg)
    file.close()
    print(u"完成")
    return

def save_vip_msg():
    all_msgs = get_all_qq_msgs(qq_record_file_path)
    fenxiang_list = save_all_msgs(all_msgs)
    
    save_share_story(fenxiang_list, all_msgs)

    for id in vip_qq_ids:
        save_msg_of_one_id(id, all_msgs)
    
    return

save_vip_msg()