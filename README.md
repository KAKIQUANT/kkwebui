
# 项目简介

KakiQuant 是一个创新的量化金融和区块链项目，我们旨在通过先进的分析工具和区块链技术，打造普惠金融体系，使普通投资者也能享有专业量化机构的工具，提高投资决策质量。

## 推荐环境

- Python 3.9


## 使用 `pip` 安装项目所需的依赖项：

```bash
pip install -r requirements.txt
```

## 安装 TA-Lib

windows用户

由于 TA-Lib 在某些平台上的安装可能会有问题，我们建议通过预编译的轮子文件进行安装。您可以在以下网址找到适合您平台的轮子文件：[https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)

下载相应的 `.whl` 文件后，使用 `pip` 安装（文件中已经提供相应轮子）：

```bash
pip install path/to/your/TA_Lib‑0.4.0‑cp39‑cp39‑win_amd64.whl
```

将 `path/to/your/` 替换为您下载的 `.whl` 文件的实际路径。

对于 macOS/Linux 用户

```bash
brew install ta-lib
pip install ta-lib
```

## 配置 OpenAI API Key

为了使用 OpenAI 的 API，您需要设置 `OPENAI_API_KEY` 环境变量。以下是设置环境变量的方法：

### 对于 macOS/Linux 用户

在终端中，运行以下命令：

```bash
export OPENAI_API_KEY='your_openai_api_key'
```

### 对于 Windows 用户

在命令提示符中，运行以下命令：

```bash
setx OPENAI_API_KEY=your_openai_api_key
```

将 `your_openai_api_key` 替换为您的实际 API 密钥。

请确保在运行项目之前，所有依赖项均已正确安装，并且已配置 `OPENAI_API_KEY` 环境变量。



