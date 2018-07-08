
# coding: utf-8

from __future__ import division
from numpy.random import randn
import random 
import numpy as np
import os
import matplotlib.pyplot as plt
np.random.seed(12345)
from pandas import Series, DataFrame
import pandas
import pandas as pd
import csv
import time
import datetime


addstr = '\uFF0B'
substr = '\u2212'
mulstr = '\u00D7'
divstr = '\u00F7'

'''
生成加法表
'''

def get_add99_table():
    sn = 0
    sn_list = []
    adder1 = []
    adder2 = []
    expression = []
    sum_rslt = []
    for i in range(1, 10):
        for j in range(i, 10):
            adder1.append(i)
            adder2.append(j)
            expression.append(str(i)+addstr+str(j)+"=")
            sum_rslt.append(i+j)    
            sn_list.append(sn)
            sn = sn + 1           
    
    clmn = ['sn', 'expression', 'result']
    dict_data = {'sn': sn_list,                    'expression': expression,                    'result': sum_rslt}
    table = DataFrame(dict_data, columns=clmn)

    return table

'''
生成凑10加法表
'''
def get_add10_table():
    sn5 = [i for i in range(1, 5)]  
    sn10 = [i for i in range(1, 10)]
    exp5 = [str(sn)+addstr+"( )=5? " for sn in sn5]
    exp10 = [str(sn)+addstr+"( )=10? " for sn in sn10]
    resl5 = [(5-sn) for sn in sn5] 
    resl10 = [(10-sn) for sn in sn10] 
    
    
    sn = [i for i in range(len(sn5 + sn10))]
    expression = exp5 + exp10
    result = resl5 + resl10
    #print(sn, expression, result)
    
    clmn = ['sn', 'expression', 'result']
    dict_data = {'sn': sn,                    'expression': expression,                    'result': result}
    add10_table = DataFrame(dict_data, columns=clmn)
    
    return add10_table

'''
生成连加运算表
'''
def get_lianjia_table():
    
    sn10 = [i for i in range(2, 11)]  
    exp10 =[]
    resl10 = []
    for sn in sn10:
        tmp_sn = [str(i) for i in range(1, sn+1)]
        tmp_exp = '+'.join(tmp_sn) + "=?"
        exp10.append(tmp_exp)
        tmp_sn = [i for i in range(1, sn+1)]
        resl10.append(sum(tmp_sn))  
    sn = [i for i in range(len(sn10))] 
    expression = exp10
    result = resl10    
    clmn = ['sn', 'expression', 'result']
    dict_data = {'sn': sn,                    'expression': expression,                    'result': result}
    lianjia_table = DataFrame(dict_data, columns=clmn)
    return lianjia_table


'''
生成乘法表
'''
def get_mul99_table():
    sn = 0
    sn_list = []
    op1 = []
    op2 = []
    expression = []
    rslt = []
    for i in range(1, 10):
        for j in range(i, 10):
            op1.append(i)
            op2.append(j)
            expression.append(str(i)+mulstr+str(j)+"=")
            rslt.append(i*j)    
            sn_list.append(sn)
            sn = sn + 1           
    
    clmn = ['sn', 'expression', 'result']
    dict_data = {'sn': sn_list,                    'expression': expression,                    'result': rslt}
    table = DataFrame(dict_data, columns=clmn)
    
    return table

def get_mul99h_table():
    sn = 0
    sn_list = []
    op1 = []
    op2 = []
    expression = []
    rslt = []
    for i in range(1, 10):
        for j in range(1, i+1):
            op1.append(i)
            op2.append(j)
            expression.append(str(j)+mulstr+str(i)+"=")
            rslt.append(i*j)    
            sn_list.append(sn)
            sn = sn + 1           
    
    clmn = ['sn', 'expression', 'result']
    dict_data = {'sn': sn_list,                    'expression': expression,                    'result': rslt}
    table = DataFrame(dict_data, columns=clmn)
    
    return table

'''
生成平方表
'''
def get_pingfang_table(n):    
    sn10 = [i for i in range(1, n+1)]  
    exp10 =[]
    resl10 = []
    for sn in sn10:       
        tmp_exp = str(sn)+ mulstr + str(sn) + "=?"
        exp10.append(tmp_exp)       
        resl10.append(sn*sn)  
    sn = [i for i in range(len(sn10))] 
    expression = exp10
    result = resl10    
    clmn = ['sn', 'expression', 'result']
    dict_data = {'sn': sn,                    'expression': expression,                    'result': result}
    _table = DataFrame(dict_data, columns=clmn)
    return _table


def print_lines():
    print(100*'-')
    return


'''
从命令行读取数字
'''

def get_inputstr(expr):
    input_str = input(expr)
    while input_str.isdigit() is False:
        print(u"请输入数字，如要退出，请输入字母q")

        if input_str == 'q':
            print(u"计算结束")
            return input_str           
        else:            
            input_str = input(expr)   
    
    return input_str

'''
将计算结果存入csv文件
'''
def calc_record_to_csv(columns, record_dict, file):
    with open(file, 'a+') as csvfile:
        fieldnames = columns
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if 0 == os.path.getsize(file):                 
            writer.writeheader()
            
        writer.writerow(record_dict)       
        
    csvfile.close()

'''
计算并记录时间和对错结果
'''
def calc_and_record(user, table, calc_type, seq='random'):        
    sn = table.sn.copy()
    if seq == 'random':    
        random.shuffle(sn)
    num = len(sn)
    
    clmn = ['time', 'correct']    
    idx = table.sn
    rec = DataFrame(index=idx, columns=clmn)
    
    total_start = time.time()     
    for tab_idx in sn.values.tolist():
        row_expression = table.ix[tab_idx, 'expression']
        row_sn = table.ix[tab_idx, 'sn']
        row_result = table.ix[tab_idx, 'result']
        one_start = time.time()  
        input_str = get_inputstr(row_expression)         
        if input_str == 'q':
            return
        
        adder2 = int(input_str)
        if adder2 != row_result:            
            correct_tmp = False
        else:
            correct_tmp = True        
        rec.ix[row_sn, 'correct'] = correct_tmp
            
        one_end = time.time() 
        one_time = one_end - one_start        
        rec.ix[row_sn, 'time'] = one_time        
    
    total_end = time.time()
    total_time = total_end - total_start
    avg_time = total_time / num
    rate = rec[rec.correct == True].correct.count() / num 
    rec_time = datetime.datetime.now()
    
    #时间结果存入CSV文件    
    t_columns = ['date'] + table.sn.values.tolist() + ['avg_time']
    t_rec = [rec_time.strftime('%Y-%m-%d %H:%M:%S')] + rec['time'].values.tolist() + [avg_time]
    t_row = dict(zip(t_columns, t_rec))
       
    t_file = user + "_" + calc_type + "_time" ".csv"
    calc_record_to_csv(t_columns, t_row, t_file)
    t_history = pd.read_csv(t_file)
    
    #正确率结果存入csv文件
    c_columns = ['date'] + table.sn.values.tolist() + ['avg_corr_rate']
    c_rec = [rec_time.strftime('%Y-%m-%d %H:%M:%S')] + rec['correct'].values.tolist() + [rate]
    c_row = dict(zip(c_columns, c_rec))
       
    c_file = user + "_" + calc_type + seq + "_corr" ".csv"
    calc_record_to_csv(c_columns, c_row, c_file)
    c_history = pd.read_csv(c_file)
    
    #打印错题
    print_lines()
    if False in rec.correct.values:
        print(u"以下题目答错，请再仔细算算看：")
        for sn, corr in zip(rec.index.values, rec.correct.values):
            if corr is True:
                continue
            print(table.ix[sn, 'expression'])
    else:
        print(u"全部答对，你真棒！")   
    
    #打印统计结果
    print(u"本次总共用时%d秒, 平均每道题用时%.2f秒，正确率%.2f%%" % (total_time, avg_time, rate*100))     
        
    return t_history, c_history

'''
显示结果
'''
def stat_and_plot(table, t_history, c_history):        
    #统计用时TopN
    n = 3
    t_hist_mean = t_history.mean()
    t_avg_mean = t_hist_mean[-1]
    stat_sn = table.expression.values.tolist()
    stat_time = t_hist_mean.values[:-1]    
    stat_dict = {'sn':stat_sn, 'time':stat_time}    
    stat_df = DataFrame(stat_dict)
    
    t_topn = stat_df.sort_values(by='time', ascending=False)[:n]  
    t_sn = t_topn.sn
    print_lines()
    print(u"耗时Top%d:" % n) 
    for sn in t_sn.index.values.tolist(): 
        print("%-20s: 平均用时:%.2f" % (table.ix[int(sn), 'expression'], t_topn.ix[sn, 'time']))          
    
    #统计正确率TopN
    c_tmp = c_history.copy()
    c_count = c_tmp[c_tmp ==False].count()    
    if c_count.count() > 0:
        c_topn = c_count[1:-1].sort_values(ascending=False)        
        if c_count[c_count > 0].count() < n:
            n = c_count[c_count > 0].count() 
        c_sn = c_topn.index.values.tolist()[:n]
        print_lines()
        print(u"错误Top%d:" % n) 
        for sn in c_sn:        
            print("%-20s: 错误次数:%d" % (table.ix[int(sn), 'expression'], c_topn[sn]))  
     
    #绘图 
    print_lines()
    plt.figure(figsize=(10, 6))
    plt.subplot(211)
    plt.plot(t_history.avg_time)
    plt.title(u"Mean Time")
    plt.ylim(0, t_history.avg_time.max()+2)
    plt.grid()

    plt.subplot(212)
    plt.plot(c_history.avg_corr_rate)
    plt.title(u"Accuracy")
    plt.ylim(0, 1.2)
    plt.grid()
    
    return
    
'''
连加入口
'''
def lianjia10_entry(user,seq):  
    calc_type = "lianjia10"
    table = get_lianjia_table()
    t_hist, c_hist = calc_and_record(user, table, calc_type, seq)
    stat_and_plot(table, t_hist, c_hist)
    return

'''
凑10运算入口
'''
def add10_entry(user,seq):  
    calc_type = "add10"
    table = get_add10_table()
    t_hist, c_hist = calc_and_record(user, table, calc_type, seq)
    stat_and_plot(table, t_hist, c_hist)
    return

def add99_entry(user,seq):  
    calc_type = "add99"
    table = get_add99_table()
    t_hist, c_hist = calc_and_record(user, table, calc_type, seq)
    stat_and_plot(table, t_hist, c_hist)
    return

def mul99_entry(user,seq):  
    calc_type = "mul99"
    table = get_mul99_table()
    t_hist, c_hist = calc_and_record(user, table, calc_type, seq)
    stat_and_plot(table, t_hist, c_hist)
    return

def mul99_entryh(user,seq):  
    calc_type = "mul99h"
    table = get_mul99h_table()
    t_hist, c_hist = calc_and_record(user, table, calc_type, seq)
    stat_and_plot(table, t_hist, c_hist)
    return

'''
20以内平方数入口
'''
def pingfang10_entry(user,seq):  
    calc_type = "pingfang10"
    table = get_pingfang_table(10)
    t_hist, c_hist = calc_and_record(user, table, calc_type, seq)
    stat_and_plot(table, t_hist, c_hist)
    return

def pingfang20_entry(user,seq):  
    calc_type = "pingfang20"
    table = get_pingfang_table(20)
    t_hist, c_hist = calc_and_record(user, table, calc_type, seq)
    stat_and_plot(table, t_hist, c_hist)
    return

def calc_select(user):
    print_lines()
    print(u"1：凑10加法")
    print(u"2：10以内加法")
    print(u"3：九九乘法")
    print(u"4：九九乘法(横)")
    print(u"5：10以内自然数连加")
    print(u"6：10以内平方数")
    print(u"7：20以内平方数")
    print_lines()
    input_str = input(u"请输入题目编号：")
    
    if '1' == input_str:
        add10_entry(user, 'norandom')
    elif '2' == input_str:
        add99_entry(user, 'norandom')
    elif '3' == input_str:
        mul99_entry(user, 'norandom')
    elif '4' == input_str:
        mul99_entryh(user, 'norandom')
    elif '5' == input_str:
        lianjia10_entry(user, 'norandom')
    elif '6' == input_str:
        pingfang10_entry(user, 'norandom')
    elif '7' == input_str:
        pingfang20_entry(user, 'norandom')
    else:
        print( '请选择正确的项目编号')    
    return

def calc_select2(user):
    print_lines()
    print(u"1：凑10加法")
    print(u"2：10以内加法")
    print(u"3：九九乘法")    
    print(u"4：10以内自然数连加")
    print(u"5：20以内平方数")
    print_lines()
    input_str = input(u"请输入题目编号：")
    
    if '1' == input_str:
        add10_entry(user, 'random')
    elif '2' == input_str:
        add99_entry(user, 'random')
    elif '3' == input_str:
        mul99_entry(user, 'random')    
    elif '4' == input_str:
        lianjia10_entry(user, 'random')    
    elif '5' == input_str:
        pingfang20_entry(user, 'random')
    else:
        print( '请选择正确的项目编号')    
    return

def calc_select3(user):
    print_lines()
    print(u"1：凑10加法")
    print(u"2：10以内加法")
    print(u"3：九九乘法")    
    print(u"4：10以内自然数连加")
    print(u"5：20以内平方数")
    print_lines()
    input_str = input(u"请输入题目编号：")
    
    if '1' == input_str:
        add10_entry(user, 'random')
    elif '2' == input_str:
        add99_entry(user, 'random')
    elif '3' == input_str:
        mul99_entry(user, 'random')    
    elif '4' == input_str:
        lianjia10_entry(user, 'random')    
    elif '5' == input_str:
        pingfang20_entry(user, 'random')
    else:
        print( '请选择正确的项目编号')    
    return

def level_select(user):
    print_lines()
    print(u"1：初级")
    print(u"2：二级")
    print(u"3: 三级")
    
    print_lines()
    input_str = input(u"请难度：")
    
    if '1' == input_str:
        calc_select(user)
    elif '2' == input_str:
        calc_select2(user)
    elif '3' == input_str:
        calc_select3(user)
    else:
        print('输入错误，请重新选择')

    return




