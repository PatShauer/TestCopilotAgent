# TestCopilotAgent

一个用于调用OpenAI兼容LLM API的Python实现。本项目提供了一个简单、灵活的函数，可以与各种LLM提供商一起使用，包括OpenAI、Azure OpenAI、LocalAI、Ollama和其他OpenAI兼容的API。

## 功能特性

- **通用兼容性**：适用于任何OpenAI兼容的API
- **全面的错误处理**：对网络问题、API错误和无效参数进行强大的错误处理
- **灵活配置**：支持各种模型、参数和自定义设置
- **简单接口**：易于使用的函数，具有合理的默认值
- **完整文档**：完整的文档和示例
- **类型提示**：完整的类型注释，提供更好的开发体验
- **测试**：包含全面的单元测试

## 安装

1. 克隆此仓库：
```bash
git clone https://github.com/PatShauer/TestCopilotAgent.git
cd TestCopilotAgent
```

2. 安装依赖项：
```bash
pip install -r requirements.txt
```

## 快速开始

```python
from llm_api import call_llm_api, extract_response_text

# 使用OpenAI的基本用法
response = call_llm_api(
    prompt="法国的首都是什么？",
    api_url="https://api.openai.com/v1",
    api_key="your-openai-api-key",
    model="gpt-3.5-turbo"
)

text = extract_response_text(response)
print(text)  # "法国的首都是巴黎。"
```

## API参考

### `call_llm_api()`

调用OpenAI兼容LLM API的主要函数。

**参数：**
- `prompt` (str)：要发送给LLM的用户提示/消息
- `api_url` (str)：API端点的基础URL
- `api_key` (str, 可选)：用于身份验证的API密钥（本地API为None）
- `model` (str)：要使用的模型名称（默认："gpt-3.5-turbo"）
- `temperature` (float)：采样温度0-2（默认：0.7）
- `max_tokens` (int, 可选)：要生成的最大令牌数
- `system_message` (str, 可选)：用于上下文的系统消息
- `timeout` (int)：请求超时秒数（默认：30）
- `**kwargs`：API的其他参数

**返回值：**
- `Dict`：包含生成文本和元数据的完整API响应

### `extract_response_text()`

从API响应中提取生成的文本。

**参数：**
- `api_response` (Dict)：来自`call_llm_api()`的响应

**返回值：**
- `str`：生成的文本内容

### `get_usage_info()`

从API响应中提取令牌使用信息。

**参数：**
- `api_response` (Dict)：来自`call_llm_api()`的响应

**返回值：**
- `Dict` 或 `None`：包括令牌计数的使用信息

## 使用示例

### OpenAI API
```python
response = call_llm_api(
    prompt="解释量子计算",
    api_url="https://api.openai.com/v1",
    api_key="sk-...",
    model="gpt-4",
    temperature=0.7,
    system_message="你是一名物理学教授。"
)
```

### Azure OpenAI
```python
response = call_llm_api(
    prompt="写一个摘要",
    api_url="https://your-resource.openai.azure.com/openai/deployments/your-deployment",
    api_key="your-azure-key",
    model="gpt-35-turbo"
)
```

### 本地API（LocalAI、Ollama等）
```python
response = call_llm_api(
    prompt="你好，你怎么样？",
    api_url="http://localhost:8080/v1",
    model="local-model"
    # 本地API不需要API密钥
)
```

### 使用自定义参数
```python
response = call_llm_api(
    prompt="从1数到10",
    api_url="https://api.openai.com/v1",
    api_key="sk-...",
    model="gpt-3.5-turbo",
    temperature=0.1,
    max_tokens=100,
    top_p=0.9,
    frequency_penalty=0.0,
    stop=["\n"]
)
```

## 错误处理

该函数提供全面的错误处理：

```python
try:
    response = call_llm_api(
        prompt="测试提示",
        api_url="https://api.example.com/v1",
        api_key="invalid-key"
    )
    text = extract_response_text(response)
    print(text)
    
except ValueError as e:
    print(f"无效参数：{e}")
except RuntimeError as e:
    print(f"API错误：{e}")
except Exception as e:
    print(f"意外错误：{e}")
```

## 测试

运行测试套件：

```bash
python -m unittest test_llm_api.py -v
```

## 文件结构

- `llm_api.py` - 包含LLM API函数的主要模块
- `test_llm_api.py` - 全面的单元测试
- `examples.py` - 使用示例和演示
- `requirements.txt` - Python依赖项

## 支持的提供商

此实现适用于任何OpenAI兼容的API，包括：

- **OpenAI**（GPT-3.5、GPT-4等）
- **Azure OpenAI服务**
- **LocalAI**（自托管）
- **Ollama**（本地模型）
- **Together AI**
- **Anyscale Endpoints**
- **OpenRouter**
- **Perplexity AI**
- **以及更多...**

## 环境变量

为了方便起见，您可以设置环境变量：

```bash
export OPENAI_API_KEY="your-openai-key"
export AZURE_OPENAI_API_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
```

## 贡献

1. Fork这个仓库
2. 创建一个功能分支
3. 进行更改
4. 运行测试以确保一切正常
5. 提交拉取请求

## 许可证

本项目是开源项目，根据MIT许可证提供。