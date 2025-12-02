import os


def create_template_files():
    print("🚀 一键创建模板文件")
    print("=" * 50)

    # 创建templates/math_app目录
    templates_dir = os.path.join('templates', 'math_app')
    os.makedirs(templates_dir, exist_ok=True)

    # 创建home.html文件
    home_html = """<!DOCTYPE html>
<html>
<head>
    <title>数学辅导助手 - Math Tutor</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        textarea, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        textarea {
            min-height: 100px;
            resize: vertical;
        }
        button {
            background-color: #3498db;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #2980b9;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>数学辅导助手 / Math Tutor Assistant</h1>

        <div class="form-group">
            <label for="question">输入你的数学问题 / Enter your math question:</label>
            <textarea id="question" name="question" placeholder="例如：什么是二次方程的求根公式？ / e.g., What is the quadratic formula?"></textarea>
        </div>

        <div class="form-group">
            <label for="language">回答语言 / Answer in:</label>
            <select id="language" name="language">
                <option value="en">English</option>
                <option value="zh">中文</option>
            </select>
        </div>

        <button onclick="submitQuestion()">获取答案 / Get Answer</button>

        <div id="result" class="result" style="display: none;">
            <h3>答案 / Answer:</h3>
            <div id="answer"></div>
        </div>
    </div>

    <script>
        function submitQuestion() {
            const question = document.getElementById('question').value;
            const language = document.getElementById('language').value;
            const resultDiv = document.getElementById('result');
            const answerDiv = document.getElementById('answer');

            if (!question) {
                alert('请输入问题 / Please enter a question');
                return;
            }

            // 显示加载中
            answerDiv.innerHTML = '处理中... / Processing...';
            resultDiv.style.display = 'block';

            // 发送请求
            fetch('/math/query/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: new URLSearchParams({
                    'question': question,
                    'language': language
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    answerDiv.innerHTML = data.answer;
                } else {
                    answerDiv.innerHTML = '错误: ' + data.error;
                }
            })
            .catch(error => {
                answerDiv.innerHTML = '请求失败: ' + error;
            });
        }

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    </script>
</body>
</html>"""

    home_path = os.path.join(templates_dir, 'home.html')
    with open(home_path, 'w', encoding='utf-8') as f:
        f.write(home_html)

    print(f"✅ 创建文件: {home_path}")

    # 验证创建结果
    print("\\n📁 创建后templates文件夹内容:")
    for root, dirs, files in os.walk('templates'):
        for file in files:
            print(f"   📄 {os.path.join(root, file)}")

    print("\\n🎯 下一步: 运行服务器测试")
    print("命令: python manage.py runserver 8000")
    print("访问: http://127.0.0.1:8000/math/")


if __name__ == "__main__":
    create_template_files()