
from typing import Optional
import strawberry
from enum import Enum

@strawberry.type
class Image:
    id: strawberry.ID
    src: str
    width: int
    height: int
@strawberry.input
class ImageInput:
    src: str
    width: int
    height: int

@strawberry.enum
class Size(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    BIG = "big"

@strawberry.type
class Pin:
    id: strawberry.ID
    img: Image
    name: str
    size: Size
    price: int
@strawberry.input
class PinInput:
    img: ImageInput
    name: str
    size: Size

@strawberry.type
class User:
    id: strawberry.ID
    name: str
@strawberry.input
class UserInput:
    name: str

@strawberry.type
class Order:
    id: strawberry.ID
    user: User
    pins: list[Pin]
    totalPrice: int
@strawberry.input
class OrderInput:
    userId: strawberry.ID
    pinsIds: list[strawberry.ID]
    totalPrice: int


images = [
    Image(id=1, src="image1.png", width=50, height=50),
    Image(id=2, src="image2.png", width=50, height=50),
]
pines = [
    Pin(id=1, img=images[0], name="PinDeSpiderman", size=Size.BIG, price=100),
    Pin(id=2, img=images[1], name="PinDeCeti", size=Size.SMALL, price=50),
]
users = [
    User(id=1, name="Manu"),
    User(id = 2, name="Fulana"),
]
orders = [
    Order(id=1, user = users[0], pins = [pines[0], pines[1]], totalPrice=150),
    Order(id=2, user = users[1], pins = [pines[0]], totalPrice=100),
]


#Lectura
@strawberry.type
class Query:
    @strawberry.field
    def pins (self, containsInName: Optional[str] = None, size: Optional[Size] = None) -> list[Pin]:
        result = pines
        if containsInName:
            result = [p for p in result if containsInName.lower() in p.name.lower()]
        if size:
            result = [p for p in result if p.size == size]
            
        return result
    @strawberry.field
    def pin(self, id: int) -> Optional[Pin]:
        return next((p for p in pines if p.id == id), None)

    @strawberry.field
    def users(self) -> list[User]:
        result = users
        return users
    @strawberry.field
    def user(self, id : int) -> Optional[User]:
        return next((u for u in users if u.id == id), None)
    
    @strawberry.field
    def orders (self, userId: Optional[strawberry.ID] = None, pinId: Optional[strawberry.ID] = None) -> list[Order]:
        result = orders
        if userId:
            result = [o for o in result if o.user.id == userId]
        if pinId:
            result = [o for o in result if any(p.id == pinId for p in o.pins)]
        return result
    @strawberry.field
    def order (self, id: int) -> Optional[Order]:
        return next((o for o in orders if o.id == id), None)
    
@strawberry.type
class Mutation:
    @strawberry.mutation
    def createImg(self, data: ImageInput) -> Image:
        new = Image(id=len(images)+1, src=data.src, width=data.width,
                    height = data.height)
        images.append(new)
        return new
    @strawberry.mutation
    def createPin(self, data: PinInput) -> Pin:
        new = Pin(id=len(pines)+1, img = data.img, name=data.name, size=data.size)
        pines.append(new)
        return new
    @strawberry.mutation
    def createUser(self, data: UserInput) -> User:
        new = User(id=len(users)+1, name=data.name)
        users.append(new)
        return new
    @strawberry.mutation
    def createOrder(self, data: OrderInput) -> Order:
        orderUser = next((u for u in users if str(u.id) == str(data.userId)), None)
        orderPins = [p for p in pines if str(p.id) in [str(pid) for pid in data.pinsIds]]
        new = Order(id=len(orders)+1, user=orderUser, pins=orderPins, totalPrice=data.totalPrice)
        orders.append(new)
        return new

schema = strawberry.Schema(query=Query, mutation=Mutation)