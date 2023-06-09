# https://fastapi.tiangolo.com/zh/tutorial/cookie-params/
import uvicorn
from fastapi import FastAPI, Cookie


app = FastAPI()


# 声明 Cookie 参数的结构与声明 Query 参数和 Path 参数时相同
# http://127.0.0.1:8001/items
# http://127.0.0.1:8001/items?id=10
@app.get("/items")
async def read_items(id: str | None = Cookie(default=None)):
    return {"id": id}


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
