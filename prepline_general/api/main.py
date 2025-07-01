import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(project_root)

if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(
            "prepline_general.api.app:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="debug",
            workers=1
        )
    except Exception as e:
        print(f"[ERROR] 启动服务失败: {str(e)}")
        sys.exit(1)
