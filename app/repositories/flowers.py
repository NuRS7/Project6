

class FlowersRepository:
    flowers_db = []
    flower_id = 1

    @classmethod
    def add_flower(cls, name: str, quantity: int, price: float, photo: str = None):
        flower = {
            "id": cls.flower_id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "photo": photo
        }
        cls.flowers_db.append(flower)
        cls.flower_id += 1

    @classmethod
    def get_flowers(cls):
        return cls.flowers_db
