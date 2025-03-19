from flask import Flask, render_template, request, jsonify
from flask import request, abort
import logging
import sys
import heapq



app = Flask(__name__)

@app.route('/')
def home():
    visitor_ip = request.remote_addr
    app.logger.info(f"Visited by IP: {visitor_ip}")
    return render_template('start.html', ip=visitor_ip)


@app.before_request
def restrict_ips():
    banned_ips = ['172.22.82.6']  # 这里添加你想要禁止的 IP 地址
    if request.remote_addr in banned_ips:
        abort(403)  # 可以返回403错误页面或者其他适当的响应

@app.route('/tu_01')
def tu_01():
    return render_template('tu_01.html')

@app.route('/tu_erfen')
def tu_erfen():
    return render_template('tu_erfen.html')

@app.route('/digui_erfen')
def digui_erfen():
    return render_template('digui_erfen.html')

@app.route('/tu_01_fenzhi')
def tu_01_fenzhi():
    return render_template('tu_01_fenzhi.html')

@app.route('/digui_01_bei')
def digui_01_bei():
    return render_template('digui_01_bei.html')


def bound(weight, profit, items, level, capacity):
    """
    计算当前节点的上界（bound）
    """
    j = level
    totWeight = weight
    profitBound = profit
    while j < len(items) and totWeight + items[j]['weight'] <= capacity:
        totWeight += items[j]['weight']
        profitBound += items[j]['value']
        j += 1
    if j < len(items):
        profitBound += (capacity - totWeight) * (items[j]['value'] / items[j]['weight'])
    return profitBound


@app.route('/solve_knapsack', methods=['POST'])
def solve_knapsack():
    data = request.get_json()
    items = data['items']
    capacity = data['capacity']

    # 初始化步骤列表
    steps = []

    # 初始状态 q0
    state = 'q0'
    steps.append({
        'state': state,
        'action': '开始状态',
        'level': '',
        'next_state': 'q1',
        'contains': [],
        'profit': '0',
    })

    # q1: 读取物品个数
    steps.append({
        'state': 'q1',
        'action': '读取物品个数',
        'level': '',
        'next_state': 'q2',
        'contains': [],
        'profit': '0',
    })

    # q2: 读取背包容量
    steps.append({
        'state': 'q2',
        'action': '读取背包容量',
        'level': '',
        'next_state': 'q3',
        'contains': [],
        'profit': '0',
    })

    # q3: 开始求解物品
    steps.append({
        'state': 'q3',
        'action': '开始求解物品',
        'level': '',
        'next_state': 'q4',
        'contains': [],
        'profit': '0',
    })

    # 分支限界法求解背包问题
    pq = []
    maxProfit = 0
    bestItems = []

    pq.append({
        'level': -1,
        'weight': 0,
        'profit': 0,
        'itemsTaken': [],
        'bound': bound(0, 0, items, 0, capacity),
        'parent': 'root',
        'id': 'node0',
        'nodeOrder': 0,
        'pruned': False,
    })

    nodeId = 0
    nodeCount = 0

    while pq:
        pq.sort(key=lambda x: x['bound'], reverse=True)
        node = pq.pop(0)

        steps.append({
            'state': 'q5',
            'action': '选择bound最大的活结点',
            'level': '',
            'next_state': 'q6',
            'contains': [],
            'profit': node['profit'],
        })

        level = node['level'] + 1
        if level < len(items):
            includeWeight = node['weight'] + items[level]['weight']
            includeProfit = node['profit'] + items[level]['value']

            if includeWeight <= capacity:
                includeBound = bound(includeWeight, includeProfit, items, level + 1, capacity)
                if includeBound > maxProfit:
                    includeNode = {
                        'level': level,
                        'weight': includeWeight,
                        'profit': includeProfit,
                        'itemsTaken': node['itemsTaken'] + [level],
                        'bound': includeBound,
                        'parent': node['id'],
                        'id': f'node{nodeId}',
                        'nodeOrder': nodeCount,
                        'pruned': False,
                    }
                    pq.append(includeNode)
                    steps.append({
                        'state': 'q6',
                        'action': f'扩展活结点',
                        'level': level,
                        'next_state': 'q4',
                        'contains': includeNode['itemsTaken'],
                        'profit': includeProfit,
                    })
                    nodeCount += 1
                    if includeProfit > maxProfit:
                        maxProfit = includeProfit
                        bestItems = includeNode['itemsTaken']

            excludeBound = bound(node['weight'], node['profit'], items, level + 1, capacity)
            if excludeBound > maxProfit:
                excludeNode = {
                    'level': level,
                    'weight': node['weight'],
                    'profit': node['profit'],
                    'itemsTaken': node['itemsTaken'],
                    'bound': excludeBound,
                    'parent': node['id'],
                    'id': f'node{nodeId + 1}',
                    'nodeOrder': nodeCount,
                    'pruned': False,
                }
                pq.append(excludeNode)
                steps.append({
                    'state': 'q6',
                    'action': f'扩展活结点',
                    'level': level,
                    'next_state': 'q4',
                    'contains': node['itemsTaken'],
                    'profit': node['profit'],
                })
                nodeCount += 1

    steps.append({
        'state': 'q7',
        'action': '回溯得到最优解',
        'level': '',
        'next_state': 'q8',
        'contains': bestItems,
        'profit': maxProfit,
    })

    steps.append({
        'state': 'q8',
        'action': '将解写入纸带，结束',
        'level': '',
        'next_state': '',
        'contains': bestItems,
        'profit': maxProfit,
    })

    print(maxProfit)
    print(bestItems)

    return jsonify({
        'steps': steps,
        'maxProfit': maxProfit,
        'optimalSolution': bestItems,
    })




# 使用备忘录法解决01背包问题
def knapsack_with_memoization(items, capacity):
    memo = {}  
    steps = []  
    stack_operations = []  
    max_depth = 0  
    optimalSelection = [0] * len(items)  
    path = {} 
    all_optimal_solutions = []  


    def dp(n, cap, depth):
        nonlocal max_depth
        max_depth = max(max_depth, depth)  

        call_desc = f"处理物品 {n} (剩余容量 {cap}, 递归深度 {depth})"
        stack_operations.append(f"入栈: {call_desc}") 


        if (n, cap) in memo:
            result_desc = f"使用备忘录已有结果 memo[{n}][{cap}] = {memo[(n, cap)]}"
            steps.append(f"memo[{n}][{cap}] = {memo[(n, cap)]} ({result_desc})")
            stack_operations.append(f"出栈: {call_desc} - {result_desc}")
            return memo[(n, cap)]

        
        if n == 0 or cap == 0:
            result = 0
            steps.append(f"memo[{n}][{cap}] = {result} (基本情况处理)")
        else:
            if items[n - 1]['weight'] <= cap:
                include_value = items[n - 1]['value']
                include_weight = items[n - 1]['weight']
                include_result = dp(n - 1, cap - include_weight, depth + 1) + include_value

                
                exclude_result = dp(n - 1, cap, depth + 1)

                if include_result > exclude_result:
                    result = include_result
                    chosen_items = [items[n - 1]]  
                    path[(n, cap)] = 1  
                    steps.append(f"memo[{n}][{cap}] = {result} (包括 物品 {n} - 重量={include_weight}, 价值={include_value}, 剩余容量 {cap})")
                    steps.append(f"memo[{n - 1}][{cap - include_weight}] + {include_value} = {include_result} (使用备忘录已有结果 memo[{n - 1}][{cap - include_weight}])")
                else:
                    result = exclude_result
                    chosen_items = []  
                    steps.append(f"memo[{n}][{cap}] = {result} (不包括 物品 {n} - 剩余容量 {cap})")
                    steps.append(f"memo[{n - 1}][{cap}] = {exclude_result} (使用备忘录已有结果 memo[{n - 1}][{cap}])")
            else:
                
                result = dp(n - 1, cap, depth + 1)
                steps.append(f"memo[{n}][{cap}] = {result} (物品 {n} 太重无法包括 - 重量={items[n - 1]['weight']}, 剩余容量 {cap})")

        memo[(n, cap)] = result  
        stack_operations.append(f"出栈: {call_desc} - memo[{n}][{cap}] = {result}")  
        return result

    
    best_value = dp(len(items), capacity, 1)
    best_items = []

    
    n, cap = len(items), capacity
    while n > 0 and cap > 0:
        if memo.get((n - 1, cap - items[n - 1]['weight']), 0) + items[n - 1]['value'] == memo.get((n, cap), 0):
            best_items.append(items[n - 1])
            cap -= items[n - 1]['weight']
        n -= 1

    
    n, cap = len(items), capacity
    while n > 0:
        if path.get((n, cap), 0) == 1:
            optimalSelection[n - 1] = 1
            cap -= items[n - 1]['weight']
        n -= 1

    
    steps.append(f"最终结果: 最大价值 = {best_value}, 选取的物品 = {best_items}, 最优解 = {optimalSelection}")
    print(optimalSelection)

    
    return best_value, best_items, steps, stack_operations, max_depth, optimalSelection


@app.route('/solve_knapsack_bei', methods=['POST'])
def solve_knapsack_bei():
    data = request.get_json()
    items = data['items']
    capacity = data['capacity']

    max_profit, best_items, steps, stack_operations, max_depth, optimalSelection = knapsack_with_memoization(items, capacity)

    return jsonify({
        "maxProfit": max_profit,
        "bestItems": best_items,
        "steps": steps,
        "stackOperations": stack_operations,
        "maxDepth": max_depth,
        "optimalSelection":optimalSelection
    })




@app.route('/digui_01_huisu')
def digui_01_huisu():
    return render_template('digui_01_huisu.html')


if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)  
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')) 
    handler.setLevel(logging.INFO)  
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=5000, debug=True)

