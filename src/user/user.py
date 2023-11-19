# унести в елку
from src.type.type import User


USER_DB: list[User] = [{
        "name": "Владимир",
        "bank": "Яндекс",
        "chat_id": "3365571"
      },{
        "name": "Вероника",
        "bank": "Альфа",
        "chat_id": "3333333333"
     },{
         "name": "вова2",
        "bank": "Сбер",
        "chat_id": "5975810763"
     }
     ]


def get_user_by_id(id: int) -> User | None:
    for i, user in enumerate(USER_DB):
        if user['chat_id'] == str(id):
            return USER_DB[i]
    return None
