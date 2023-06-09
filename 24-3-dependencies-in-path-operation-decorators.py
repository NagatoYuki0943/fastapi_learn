# https://fastapi.tiangolo.com/zh/tutorial/dependencies/dependencies-in-path-operation-decorators/
import uvicorn
from fastapi import FastAPI, Depends, Depends, Header, HTTPException


app = FastAPI()


# 路径操作装饰器依赖项
# 有时，我们并不需要在路径操作函数中使用依赖项的返回值。
# 或者说，有些依赖项不返回值。
# 但仍要执行或解析该依赖项。
# 对于这种情况，不必在声明路径操作函数的参数时使用 Depends，而是可以在路径操作装饰器中添加一个由 dependencies 组成的 list。


# 路径装饰器依赖项可以声明请求的需求项（比如响应头）或其他子依赖项
async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        # 路径装饰器依赖项与正常的依赖项一样，可以 raise 异常
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key    # 无论路径装饰器依赖项是否返回值，路径操作都不会使用这些值。


# 路径操作装饰器支持可选参数 ~ dependencies。
# 该参数的值是由 Depends() 组成的 list
@app.get("/items", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
