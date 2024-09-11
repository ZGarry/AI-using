import os
from openai import OpenAI
import concurrent.futures

# 请先安装 OpenAI SDK: `pip3 install openai`
key = ''
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")


def query(info):
    # 不适用流式的方式
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": info},
        ],
        stream=False
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content


def write_to_file(filename, content):
    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建文件的完整路径
    file_path = os.path.join(script_dir, filename)
    # 查询并写入文件
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content + '\n')


def concurrent_query(items):
    # 并发执行查询
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(items)) as executor:
        futures = {executor.submit(query, item): idx for idx, item in enumerate(items)}
        results = {}
        for future in concurrent.futures.as_completed(futures):
            try:
                idx = futures[future]
                result = future.result()
                results[idx] = result
            except Exception as e:
                print(f"An error occurred: {e}")
        return [results[idx] for idx in sorted(results)]


# 获取知识点列表
# Java后端
lev = "轮胎生产"
tens = query(f"帮我介绍十个{lev}知识点, 彼此之间用,隔开，告诉知识点的名称即可")
items = tens.split(",")

# 并发查询并写入文件
results = concurrent_query(items)
for item, result in zip(items, results):
    write_to_file(item.strip() + ".md", result)
