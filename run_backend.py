"""
Run the FastAPI backend - compatible with Python 3.14+
"""
import sys

# For Python 3.14+, we don't need special event loop policies
# Just run Uvicorn normally
import uvicorn

if __name__ == "__main__":
    try:
        uvicorn.run(
            "backend.main:app",
            host="127.0.0.1",
            port=8000,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
