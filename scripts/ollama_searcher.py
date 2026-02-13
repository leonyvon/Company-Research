"""
Ollama智能搜索工具
通过命令行调用进行智能搜索和摘要生成
"""

import sys
import io
import json
from typing import Optional

# 设置UTF-8输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from ollama import chat, web_fetch, web_search
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


def ollama_searcher(keyword: str) -> str:
    """
    调用Ollama进行智能搜索和摘要生成

    Args:
        keyword (str): 搜索关键词

    Returns:
        str: 搜索结果的摘要内容（JSON格式）
    """
    if not OLLAMA_AVAILABLE:
        return json.dumps({
            "keyword": keyword,
            "error": "Ollama库未安装，请运行: pip install ollama"
        }, ensure_ascii=False)

    try:
        available_tools = {'web_search': web_search, 'web_fetch': web_fetch}
        messages = [
            {'role': 'system', 'content': "**调用工具搜索关键词**"},
            {'role': 'user', 'content': f"keyword:{keyword}"}
        ]

        # 第一次调用：模型决定搜索策略
        response = chat(
            model='gemini-3-flash-preview:cloud',
            messages=messages,
            tools=[web_search, web_fetch]
        )

        messages.append(response.message)

        # 如果模型决定调用工具，执行工具调用
        if response.message.tool_calls:
            for tool_call in response.message.tool_calls:
                function_to_call = available_tools.get(tool_call.function.name)
                if function_to_call:
                    args = tool_call.function.arguments
                    result = function_to_call(**args)
                    messages.append({
                        'role': 'tool',
                        'content': str(result)[:2000 * 4],
                        'tool_name': tool_call.function.name
                    })
                else:
                    messages.append({
                        'role': 'tool',
                        'content': f'未找到工具 {tool_call.function.name}',
                        'tool_name': tool_call.function.name
                    })
        else:
            return json.dumps({
                "keyword": keyword,
                "error": "模型未调用任何工具"
            }, ensure_ascii=False)

        # 第二次调用：基于工具结果生成最终摘要
        system_prompt = """
        指令：请你根据我提供的搜索结果，生成简短、客观的摘要。
        条件判断：如果搜寻的关键词属于事件，还需按时间顺序考察事件的起因、经过和后续发展.
        限制：仅总结内容，自身不需要对搜索结果进行分析或评价
        """
        final_response = chat(
            model='gemini-3-flash-preview:cloud',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f'关键词:{keyword} 搜索结果：\n'+messages[-1]['content']}
            ]
        )

        return json.dumps({
            "keyword": keyword,
            "summary": final_response.message.content,
            "status": "success"
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "keyword": keyword,
            "error": str(e)
        }, ensure_ascii=False)


if __name__ == "__main__":
    # 命令行调用格式: python ollama_searcher.py "搜索关键词"
    if len(sys.argv) > 1:
        keyword = " ".join(sys.argv[1:])
    else:
        keyword = input("请输入搜索关键词: ")

    result = ollama_searcher(keyword)
    print(result)