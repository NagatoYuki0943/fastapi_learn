# https://fastapi.tiangolo.com/zh/tutorial/body-updates/
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from enum import Enum


app = FastAPI()


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


class ItemID(str, Enum):
    foo = "foo"
    bar = "bar"
    baz = "baz"


items = {
    ItemID.foo: {"name": "Foo", "price": 50.2},
    ItemID.bar: {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    ItemID.baz: {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


# http://127.0.0.1:8001/docs
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: ItemID):
    return items[item_id]


# PUT 用于接收替换现有数据的数据
# http://127.0.0.1:8001/docs
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: ItemID, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded


# 用 PATCH 进行部分更新
# PATCH操作用于更新 部分 数据。
# 即，只发送要更新的数据，其余数据保持不变。
# PATCH 没有 PUT 知名，也怎么不常用。
# 很多人甚至只用 PUT 实现部分更新。
# FastAPI 对此没有任何限制，可以随意互换使用这两种操作。


# 使用 Pydantic 的 exclude_unset 参数
# 更新部分数据时，可以在 Pydantic 模型的 .dict() 中使用 exclude_unset 参数。
# 比如，item.dict(exclude_unset=True)。
# 这段代码生成的 dict 只包含创建 item 模型时显式设置的数据，而不包括默认值。
# 然后再用它生成一个只含已设置（在请求中所发送）数据，且省略了默认值的 dict。
# 接下来，用 .copy() 为已有模型创建调用 update 参数的副本，该参数为包含更新数据的 dict。
@app.patch("/items1/{item_id}", response_model=Item)
async def update_item1(item_id: ItemID, item: Item):
    # 源数据
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    # 新数据排除默认值
    update_data = item.dict(exclude_unset=True) # 不包括默认值
    # 源数据复制一份更新为新数据
    updated_item = stored_item_model.copy(update=update_data)
    # 更新到源数据
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
