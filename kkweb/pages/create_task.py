import os
from dataclasses import asdict

import pandas as pd
import streamlit as st
from task import Task, run_task, task_from_json

import requests

from kkweb.config import DATA_DIR

# from engine.engine import Engine
from datetime import datetime
from . import gui_const

url = 'http://ailabx.com/api/funds'
url = 'http://127.0.0.1:8000/api/funds'


def show_tasks():
    if 'task' not in st.session_state.keys():
        st.session_state.task = Task()

    directory = DATA_DIR.joinpath('tasks')

    # os.listdir() 列出目录下的所有文件和目录名
    tasks = []
    for filename in os.listdir(directory.resolve()):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):  # 判断是否是文件
            # print(f'文件: {file_path}')
            tasks.append(filename)
    tasks.insert(0, '创建新策略')
    task_name = st.selectbox('本地策略列表：', options=tasks, index=0, key='select_task')
    if st.button('切换'):
        print(str(datetime.now()) + '点击切换')

        if task_name and task_name != '创建新策略':
            print('切换任务至{}========================》'.format(task_name))
            st.session_state.task = task_from_json(task_name)
        else:
            st.write(str(datetime.now()) + '初始化')
            print('执行初始化========================》')
            st.session_state.task = Task()


@st.cache_data
def get_funds():
    #
    df = pd.read_csv(DATA_DIR.joinpath('basic').joinpath('etfs.csv').resolve())
    datas = df.to_dict(orient='records')
    #datas = requests.get(url).json()['rows']
    dict_data = {item['symbol']: item['name'] + '({})'.format(item['symbol']) for item in datas}
    return dict_data

def funds_changed():
    st.write(st.session_state.symbols)

def select_funds():
    def _select_funds_format(x):
        return get_funds()[x]

    funds_data = get_funds()
    default = st.session_state.task.symbols.copy()

    if 'symbols' not in st.session_state.keys():
        st.session_state['symbols'] = []
    symbols = st.multiselect(label='请选择基金：', options=list(funds_data.keys()),
                                              format_func=lambda x: _select_funds_format(x),
                                              default=default)
    st.session_state.task.symbols = symbols


def select_period():
    task = st.session_state['task']
    periods = {'RunDaily': '每天运行', 'RunWeekly': '每周运行', 'RunMonthly': '每月运行', 'RunQuarterly': '每季度运行',
               'RunYearly': '每年运行',
               'RunDays': '自定义天数'}

    def _period_format(x):
        return periods[x]

    period = st.selectbox(label='请选择调仓周期', index=list(periods.keys()).index(task.algo_period), options=list(periods.keys()),
                          format_func=lambda x: _period_format(x))
    if period == 'RunDays':
        days = st.number_input(label='请输入天数', min_value=1, max_value=365)
        task.algo_period_days = days
    task.algo_period = period


def select_weights():
    task = st.session_state['task']
    weights = {
        'WeighEqually': '等权分配',
        # 'WeighFix': '固定权重',
        'WeighERC': '风险平价'
    }

    def _weight_format(x):
        return weights[x]

    weight = st.selectbox(label='请选择权重分配',index=list(weights.keys()).index(task.algo_weight), options=list(weights.keys()), format_func=lambda x: _weight_format(x))
    if weight == 'WeightFix':
        fix_weigths = st.text_input(label='请输入权重(逗号分隔)', value='[]')
        task.algo_weight_fix = eval(fix_weigths)
    task.algo_weight = weight


def add_features():
    # st.write("Session State: ", st.session_state)

    factors = list(gui_const.ind_dict.keys())
    # task = st.session_state['task']
    # g_feature_names = st.session_state['feature_names']
    # g_features = st.session_state['features']

    ind_name = st.selectbox('选择因子', options=factors, key='select_features', index=0)
    if st.button('新增'):
        ind = gui_const.ind_dict[ind_name]
        st.session_state.task.feature_names.append(ind.name)
        st.session_state.task.features.append(ind.expr)
        # g_feature_names.append(ind.name)
        # g_features.append(ind.expr)

    # st.write("Session State: ", st.session_state)
    count = 0

    #st.write(st.session_state.task.features)

    for i, (name, feature) in enumerate(zip(st.session_state.task.feature_names, st.session_state.task.features)):
        col1, col2, col3 = st.columns(3)
        with col1:
            f = st.text_input(label='因子名', value=name, key=feature + str(count))
            st.session_state.task.feature_names[i] = f
        with col2:
            n = st.text_input(label='表达式', value=feature, key=name + str(count))
            st.session_state.task.features[i] = n
        with col3:
            if st.button('删除', key='btn' + str(count)):
                st.session_state.task.feature_names.remove(name)
                st.session_state.task.features.remove(feature)
                st.rerun()
        count += 1
    # task.features = g_features
    # task.feature_names = g_feature_names


def add_rule(rules, rule_type='buy'):
    task = st.session_state['task']
    f = st.selectbox(label='因子', options=task.feature_names, key=rule_type)
    if st.button('添加', key='rule_add' + rule_type):
        print('f name>>', f)
        r = gui_const.Rule(f)
        rules.append(r.get_expr())

    # st.write(rules)
    for i, rule_str in enumerate(rules):

        rule = gui_const.Rule().parse_from(rule_str)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            # st.writee(task.feature_names)
            rule.feature_name = st.selectbox(label='因子', options=task.feature_names, key='factor' + rule_type + str(i))
        with col2:
            op_index = 0
            if rule.ops == '=':
                op_index = 1
            elif rule.ops == "<":
                op_index = 2
            rule.ops = st.selectbox(label='比较', options=['>', '=', '<'], key='ops' + rule_type + str(i), index=op_index)
        with col3:
            rule.value = st.number_input(label='值', value=float(rule.value), min_value=-100.0, step=0.01,
                                         max_value=100.0, key='value' + rule_type + str(i))

        with col4:
            if st.button('删除', key='rule_delete' + rule_type + str(i)):
                rules.remove(rule_str)
                st.rerun()
        rules[i] = rule.get_expr()


def buy_and_sell_rules():
    task = st.session_state['task']

    col1, col2 = st.columns(2)
    with col1:
        add_rule(task.rules_buy)

    with col2:
        add_rule(task.rules_sell, rule_type='sell')


def order_by():
    task = st.session_state['task']
    index = 0
    if task.order_by and task.order_by in task.feature_names:
        index = task.feature_names.index(task.order_by)
    order_by = st.selectbox(label='排序因子', options=task.feature_names, index=index)
    top_K = st.number_input(label='top K = ', value=task.topK)
    # drop_N = st.number_input(label='排除前N个 = ', value=task.dropN)
    task.order_by = order_by
    task.topK = top_K
    # task.dropN = drop_N


def backtest(task: Task):
    if st.button(label='开始回测'):
        with st.spinner('回测进行中，请稍后...'):
            res = run_task(task)

            df = res.prices
            ratio = res.stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('年化收益', value=str(round(float(ratio.loc['cagr'][task.name]) * 100, 2)) + '%')
            with col2:
                st.metric('最大回撤', value=str(round(float(ratio.loc['max_drawdown'][task.name]) * 100, 2)) + '%')
            with col3:
                st.metric('calmar比率', value=str(round(float(ratio.loc['calmar'][task.name]), 2)))

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('基准', value=str(round(float(ratio.loc['cagr']['基准']) * 100, 2)) + '%')
            with col2:
                st.metric('基准', value=str(round(float(ratio.loc['max_drawdown']['基准']) * 100, 2)) + '%')
            with col3:
                st.metric('基准', value=str(round(float(ratio.loc['calmar']['基准']), 2)))

            orders_df = res.get_transactions()

            col1, col2 = st.columns(2)
            with col1:
                st.write(ratio)
                print(ratio)
            with col2:
                st.line_chart(df)

            st.write(orders_df)


def build():
    if 'task' not in st.session_state.keys():
        st.session_state['task'] = Task()

    for key in ['rules_buy', 'rules_sell', 'features', 'feature_names']:
        if key not in st.session_state.keys():
            st.session_state[key] = []

    # with col2:
    task = st.session_state['task']
    tab1, tab2, tab3, tab4 = st.tabs(["选择ETF", "因子配置", "交易规则", "回测设置"])
    with tab1:
        select_funds()
    with tab2:
        add_features()
    with tab3:
        # add_features(task)
        buy_and_sell_rules()

    with tab4:
        col1, col2, col3 = st.columns(3)
        with col1:
            order_by()

        with col2:
            select_period()
            select_weights()

        name = st.text_input(label='策略名称', value=task.name)
        task.name = name

        col1, col2 = st.columns(2)
        with col1:
            date_start = st.date_input(label='起始日期', value=datetime(2010, 1, 1))
            task.start_date = date_start.strftime("%Y%m%d")
        with col2:
            task = st.session_state['task']
            date_end = st.date_input(label='结束日期')
            task.end_date = date_end.strftime("%Y%m%d")
            if st.button(label='保存策略'):
                import uuid
                if task._id is None:
                    task._id = str(uuid.uuid4())
                import json
                from kkwebui.config import DATA_DIR
                st.write(task)
                with open(DATA_DIR.joinpath('tasks').joinpath(name + '.json'), "w", encoding='UTF-8') as f:
                    json.dump(asdict(task), f, ensure_ascii=False)

            if st.button(label='发布策略'):
                import requests, json, uuid
                task_data = asdict(task)
                from utils import mongo_utils
                if task._id is None:
                    task._id = str(uuid.uuid4())
                del task_data['_id']
                mongo_utils.get_db()['tasks'].update_one({'_id': task._id}, {'$set': task_data}, upsert=True)

        backtest(task)
    # st.write(task)
