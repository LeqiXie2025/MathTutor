import os


def create_fixed_files():
    print("🚀 一键创建原始GitHub代码文件")
    print("=" * 50)

    # 创建agents目录
    os.makedirs('agents', exist_ok=True)

    # 根据你的GitHub代码创建文件
    base_agent_content = '''import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaseAgent(ABC):
    """Base class for all agents in the system."""

    def __init__(self, name: str = "BaseAgent"):
        self.name = name
        self.conversation_history: List[Dict[str, str]] = []

    @abstractmethod
    def process_input(self, input_text: str, **kwargs) -> str:
        """Process input and return response. Must be implemented by subclasses."""
        pass

    def add_to_history(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        return self.conversation_history.copy()

    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history.clear()

    def __str__(self) -> str:
        return f"{self.name} (History: {len(self.conversation_history)} messages)"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
'''

    math_tutor_agent_content = '''import os
from typing import Dict, Any
from langchain_deepseek import ChatDeepSeek
from langchain.schema import HumanMessage, SystemMessage
from .base_agent import BaseAgent

class MathTutorAgent(BaseAgent):
    """Math tutoring agent specialized in explaining mathematical concepts."""

    def __init__(self):
        super().__init__("MathTutorAgent")
        self.llm = ChatDeepSeek(
            model="deepseek-chat",
            temperature=0.7,
            max_tokens=2000,
            timeout=30,
            max_retries=2,
            api_key=os.getenv("DEEPSEEK_API_KEY")
        )

        # Define the system prompts for different languages
        self.system_prompts = {
            "en": """You are an expert math tutor. Your role is to:
1. Explain mathematical concepts clearly and step-by-step
2. Provide examples when helpful
3. Break down complex problems into manageable steps
4. Use appropriate mathematical notation
5. Be patient and encouraging

Please provide thorough, educational responses that help students understand the underlying concepts.""",

            "zh": """你是一位专业的数学辅导老师。你的职责是：
1. 清晰且分步骤地解释数学概念
2. 在有帮助时提供示例
3. 将复杂问题分解为可管理的步骤
4. 使用适当的数学符号和表达
5. 保持耐心和鼓励的态度

请提供详细、有教育意义的回答，帮助学生理解基本概念。"""
        }

    def process_input(self, input_text: str, language: str = "en", **kwargs) -> str:
        """Process math questions and provide explanations."""
        system_prompt = self.system_prompts.get(language, self.system_prompts["en"])

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=input_text)
        ]

        try:
            response = self.llm.invoke(messages)
            answer = response.content

            # Add to conversation history
            self.add_to_history("user", input_text)
            self.add_to_history("assistant", answer)

            return answer

        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            if language == "zh":
                error_msg = f"抱歉，我遇到了一个错误：{str(e)}"
            return error_msg

    def answer_question(self, question: str, language: str = "en") -> str:
        """Convenience method for answering math questions."""
        return self.process_input(question, language=language)

# Example usage
if __name__ == "__main__":
    # Test the math tutor agent
    agent = MathTutorAgent()

    # Test in English
    english_question = "Explain the concept of derivatives in calculus."
    english_answer = agent.answer_question(english_question, "en")
    print("English Question:", english_question)
    print("English Answer:", english_answer)
    print()

    # Test in Chinese
    chinese_question = "请解释微积分中导数的概念"
    chinese_answer = agent.answer_question(chinese_question, "zh")
    print("Chinese Question:", chinese_question)
    print("Chinese Answer:", chinese_answer)
'''

    init_content = '''"""
Agents package for the Math Tutor application.
Contains specialized AI agents for mathematical tutoring.
"""

from .base_agent import BaseAgent
from .math_tutor_agent import MathTutorAgent

__all__ = ["BaseAgent", "MathTutorAgent"]
'''

    # 写入agents文件
    agents_files = {
        'base_agent.py': base_agent_content,
        'math_tutor_agent.py': math_tutor_agent_content,
        '__init__.py': init_content
    }

    for filename, content in agents_files.items():
        filepath = os.path.join('agents', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 创建文件: {filepath}")

    # 创建requirements.txt
    requirements_content = '''django==5.2.8
langchain-deepseek
python-dotenv
'''
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    print("✅ 创建文件: requirements.txt")

    # 创建.env文件
    env_content = 'DEEPSEEK_API_KEY=your_deepseek_api_key_here\n'
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("✅ 创建文件: .env")

    print("\n🎯 下一步:")
    print("1. 在.env文件中填入真实的DEEPSEEK_API_KEY")
    print("2. 安装依赖: pip install -r requirements.txt")
    print("3. 运行服务器: python manage.py runserver 8000")
    print("4. 访问: http://127.0.0.1:8000/math/")


if __name__ == "__main__":
    create_fixed_files()