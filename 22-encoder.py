# https://fastapi.tiangolo.com/zh/tutorial/encoder
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime


app = FastAPI()


# 在某些情况下，您可能需要将数据类型（如Pydantic模型）转换为与JSON兼容的数据类型（如dict、list等）
# 可以使用jsonable_encoder
# 让我们假设你有一个数据库名为fake_db，它只能接收与JSON兼容的数据。
# 例如，它不接收datetime这类的对象，因为这些对象与JSON不兼容。
# 因此，datetime对象必须将转换为包含ISO格式化的str类型对象。
# 同样，这个数据库也不会接收Pydantic模型（带有属性的对象），而只接收dict。


fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


# http://127.0.0.1:8001/docs
@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)  # 将Pydantic模型转换为dict，并将datetime转换为str。
    fake_db[id] = json_compatible_item_data
    print(item)
    print(json_compatible_item_data)


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
