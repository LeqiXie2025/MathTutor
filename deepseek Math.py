import re
import sympy as sp
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, SystemMessage

# 加载环境变量
load_dotenv()

def initialize_deepseek_llm():
    """初始化 DeepSeek 语言模型"""
    api_key = input("请输入你的DeepSeek API密钥: ")

    if not api_key:
        raise ValueError("请输入有效的DeepSeek API密钥")

    try:
        # 初始化模型
        llm = ChatDeepSeek(
            model="deepseek-chat",
            base_url="https://api.deepseek.com/v1",
            temperature=0.2,
            max_tokens=1500,
            timeout=60,
            max_retries=2
        )
        return llm
    except Exception as e:
        print(f"模型初始化失败: {e}")
        raise

# 调用函数
llm = initialize_deepseek_llm()
print("模型初始化成功！")

# 3. 定义系统提示词
system_prompt = """
你是一个专门帮助大学生学习高等数学的双语助手，需满足以下要求：
1. 分析能力：遇到高数题（微积分、线性代数、概率论等），先拆解考点，再分步推导，最后总结思路；
2. 准确率：公式推导、计算过程必须严谨，可用sympy工具验证关键步骤；
3. 双语支持：用户用中文提问则优先中文回答（可附英文关键词），用英文提问则全英文回答，支持切换语言；
4. 语气：亲切热心，像学长/学姐一样，避免生硬，结尾可加鼓励的话；
5. 格式：步骤用数字编号，公式用$包裹（如$∫x²dx$），方便阅读。
"""


def generate_practice_problems(user_input, lang):
    """根据用户问题生成巩固练习题"""
    practice_prompt = """
    请根据用户的问题，生成3-5道相关的巩固练习题。
    要求：
    1. 题目难度循序渐进
    2. 覆盖用户问题的核心知识点
    3. 如果是中文问题，用中文出题；英文问题用英文出题
    4. 每道题都要有明确的题目要求
    5. 在最后提供参考答案

    格式：
    📚 巩固练习题：
    1. [题目1]
    2. [题目2]
    3. [题目3]

    💡 参考答案：
    1. [答案1]
    2. [答案2]
    3. [答案3]
    """

    try:
        # 组装练习题生成消息
        practice_messages = [
            SystemMessage(content=practice_prompt),
            HumanMessage(content=f"用户原问题：{user_input}\n生成语言：{lang}\n请生成相关的巩固练习题：")
        ]

        # 调用模型生成练习题
        practice_response = llm.invoke(practice_messages)
        practice_content = practice_response.content

        return f"\n\n🎯 巩固练习\n{practice_content}"

    except Exception as e:
        print(f"生成练习题失败: {e}")
        return ""

def math_assistant(user_input, lang="auto"):
    """数学助手主函数"""
    # 自动识别语言
    if lang == "auto":
        lang = "zh" if any('\u4e00' <= char <= '\u9fff' for char in user_input) else "en"

    # 组装消息
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"用户问题：{user_input}\n指定语言：{lang}")
    ]

    try:
        # 调用DeepSeek模型
        response = llm.invoke(messages)
        answer = response.content

        # 补充sympy计算验证
        answer = add_sympy_verification(user_input, answer)

        # === 在这里添加巩固练习题 ===
        answer += generate_practice_problems(user_input, lang)
        return answer

    except Exception as e:
        return f"抱歉，处理问题时出现错误：{str(e)}\n请检查网络连接或稍后重试。"



def add_sympy_verification(user_input, original_answer):
    """使用sympy进行数学验证"""
    try:
        # 导数验证
        if "求导" in user_input or "导数" in user_input or "differentiate" in user_input.lower():
            if "x" in user_input:
                x = sp.Symbol('x')
                # 尝试提取表达式
                if "y=" in user_input:
                    expr_str = user_input.split("y=")[1].split(" ")[0]
                else:
                    # 寻找包含x的数学表达式
                    matches = re.findall(r'[x\d+\-*/^()]+', user_input)
                    if matches:
                        expr_str = matches[0]
                    else:
                        return original_answer

                expr = sp.sympify(expr_str)
                derivative = sp.diff(expr, x)
                original_answer += f"\n\n📌 Sympy验证（导数）：$\\frac{{d}}{{dx}}({expr}) = {derivative}$"

        # 积分验证
        elif "积分" in user_input or "integral" in user_input.lower():
            if "x" in user_input:
                x = sp.Symbol('x')
                matches = re.findall(r'[x\d+\-*/^()]+', user_input)
                if matches:
                    expr_str = matches[0]
                    expr = sp.sympify(expr_str)
                    integral = sp.integrate(expr, x)
                    original_answer += f"\n\n📌 Sympy验证（不定积分）：$∫{expr}dx = {integral} + C$"

        # 方程求解验证
        elif "方程" in user_input or "equation" in user_input.lower():
            if "x" in user_input:
                x = sp.Symbol('x')
                # 尝试提取方程
                eq_matches = re.findall(r'([^=]+)=([^=]+)', user_input)
                for left, right in eq_matches:
                    try:
                        left_expr = sp.sympify(left.strip())
                        right_expr = sp.sympify(right.strip())
                        equation = sp.Eq(left_expr, right_expr)
                        solutions = sp.solve(equation, x)
                        original_answer += f"\n\n📌 Sympy验证（方程解）：${sp.latex(equation)}$ 的解为 $x = {solutions}$"
                    except:
                        pass

    except Exception as e:
        # 如果sympy处理失败，不影响主要回答
        print(f"Sympy验证失败: {e}")

    return original_answer





# 4. 交互入口
if __name__ == "__main__":
    print("🎉 DeepSeek高数双语学习助手已启动！"
          "🎉 DeepSeek Advanced Mathematics Bilingual Learning Assistant has started!")
    print("💡 示例问题：'求函数 y=x^2+3x 的导数' 或 '计算 ∫(2x+1)dx'"
          "💡Example questions: 'Find the derivative of the function y=x^2+3x' or 'Calculate ∫(2x+1)dx'")
    print("💡 输入'退出'结束对话"
          "💡Enter 'exit' to end the conversation")
    print("-" * 50)

    while True:
        try:
            user_question = input("\n🧠 你的问题\Your question：").strip()
            if user_question.lower() in ['退出', 'exit', 'quit']:
                print("👋 加油学习，下次见！Good luck for your study，C U next time！")
                break
            elif not user_question:
                continue

            # 调用助手并输出答案
            answer = math_assistant(user_question)
            print(f"\n🤖 助手回答：\n{answer}")
            print("-" * 50)

        except KeyboardInterrupt:
            print("\n👋 程序已退出，再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误：{e}")