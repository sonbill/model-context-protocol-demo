# Model Context Protocol (MCP) Demo

Repository này chứa mã nguồn demo cho việc triển khai Model Context Protocol (MCP), một giao thức giúp kết nối các ứng dụng với các mô hình ngôn ngữ lớn.

## Giới thiệu

Model Context Protocol (MCP) là một tiêu chuẩn mới để kết nối các ứng dụng với các mô hình AI. MCP định nghĩa một giao thức chuẩn để gửi yêu cầu và nhận phản hồi từ các mô hình AI, giúp cho việc tích hợp trở nên dễ dàng và thống nhất.

## Cài đặt

### Yêu cầu
- Docker
- Docker Compose (tùy chọn)
- Python 3.9+

### Bước 1: Clone repository

```bash
git clone https://github.com/sonbill/model-context-protocol-demo.git
cd model-context-protocol-demo
```

### Bước 2: Xây dựng và chạy container Docker

```bash
docker build -t mcp/time .
```

### Bước 3: Chạy MCP server

```bash
docker run -i --rm mcp/time
```

## Cấu hình VS Code

Để sử dụng MCP server trong VS Code, thêm cấu hình sau vào file `settings.json`:

```json
{
    "mcp": {
        "inputs": [],
        "servers": {
            "mcp-server-time": {
                "command": "docker",
                "args": ["run", "-i", "--rm", "mcp/time"],
                "env": {}
            }
        }
    }
}
```

## Cách sử dụng

Sau khi cài đặt MCP server, bạn có thể sử dụng nó để lấy thời gian hiện tại tại các múi giờ khác nhau:

1. Mở VS Code
2. Mở Command Palette (Ctrl+Shift+P hoặc Cmd+Shift+P)
3. Chọn "MCP: Execute Server Command"
4. Chọn "mcp-server-time" từ danh sách server
5. Nhập tên múi giờ (ví dụ: "Asia/Ho_Chi_Minh")

## Cấu trúc dự án

- `main.py`: File chính của MCP server
- `Dockerfile`: Cấu hình để build Docker image
- `requirements.txt`: Danh sách các thư viện Python cần thiết
- `docker-compose.yml`: Cấu hình Docker Compose để dễ dàng chạy

## Tài liệu tham khảo

- [Model Context Protocol Documentation](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
- [Python pytz Documentation](https://pypi.org/project/pytz/)