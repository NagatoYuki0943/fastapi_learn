# https://fastapi.tiangolo.com/zh/tutorial/body-multiple-params/
import uvicorn
from fastapi import FastAPI, Path, Body
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str


# 混合使用Path,Query和请求体参数
# http://127.0.0.1:8001/docs
@app.post("/items/{item_id}")
async def update_item(
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# 可以声明多个请求体参数
# http://127.0.0.1:8001/docs
@app.post("/items1/{item_id}")
async def update_item1(
    item_id: int,
    item: Item | None = None,
    user: User | None = None
):
    results = {"item_id": item_id}
    if item:
        results.update({"item": item})
    if user:
        results.update({"user": user})
    return results


# 请求体中的单一值
# 与使用 Query 和 Path 为查询参数和路径参数定义额外数据的方式相同，FastAPI 提供了一个同等的 Body
# Body 同样具有与 Query、Path 以及其他后面将看到的类完全相同的额外校验和元数据参数
# 使用 Body 指示 FastAPI 将其作为请求体的另一个键进行处理
# http://127.0.0.1:8001/docs
@app.post("/items2/{item_id}")
async def update_item2(
    item_id: int,
    item: Item | None = None,
    user: User | None = None,
    importance: int = Body(gt=0)
):
    results = {"item_id": item_id, "importance": importance}
    if item:
        results.update({"item": item})
    if user:
        results.update({"user": user})
    return results


# 多个请求体参数和查询参数
# 当然，除了请求体参数外，你还可以在任何需要的时候声明额外的查询参数。
# 由于默认情况下单一值被解释为查询参数，因此你不必显式地添加 Query，你可以仅执行以下操作：
#   q: str = None
# http://127.0.0.1:8001/docs
@app.post("/items3/{item_id}")
async def update_item3(
    item_id: int,
    item: Item | None = None,
    user: User | None = None,
    importance: int = Body(gt=0),
    q: str | None = None
):
    results = {"item_id": item_id, "importance": importance}
    if item:
        results.update({"item": item})
    if user:
        results.update({"user": user})
    if q:
        results.update({"q": q})
    return results


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
