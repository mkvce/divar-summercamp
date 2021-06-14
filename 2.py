class NoDeskException(Exception):
    def __init__(self, message=''):
        super().__init__(message)


class Desk:
    def __init__(self, number: int, floor: int):
        self.__id = f"{floor}-{number}"
        self.__withdraw_time = 0
    
    @property
    def id(self):
        return self.__id

    def reserve(self, ts: int, duration: int):
        if ts >= self.__withdraw_time:
            self.__withdraw_time = ts + duration
            return True
        return False



class Floor:
    def __init__(self, number: int, floor_type, price, num_of_desks=0):
        self.__id = number
        self.__desks = [Desk(i, self.__id, price) for i in range(1, num_of_desks + 1)]
        self.__type = floor_type
        self.__price = price
    
    @property
    def type(self):
        return self.__type

    def get_desk(self, ts: int, duration: int):
        for desk in self.__desks:
            if desk.reserve(ts, duration):
                return (desk.id, self.__price)
        raise NoDeskException()

    def add_desk(self):
        self.__desks.append(Desk(len(self.__desks) + 1, self.__id))

    
class WorkSpaceManager:
    def __init__(self, num_of_floors=0):
        self.__floors = [Floor(i) for i in range(1, num_of_floors + 1)]

    def add_desk(self, floor: int, num=1):
        for _ in range(num):
            self.__floors[floor - 1].add_desk()

    def get_desk(self, ts: int, username: str, floor_type: str, duration: int):
        for floor in self.__floors:
            if floor.type == floor_type:
                try:
                    return floor.get_desk(ts, duration)
                except NoDeskException:
                    continue
        raise NoDeskException()

    def add_floor(self, type, price):
        self.__floors.append(Floor(len(self.__floors) + 1, type, price))
    

class UserInterface:
    def __init__(self):
        num_of_floors, special_floor_price = [int(x) for x in input().split()]
        self.__manager = WorkSpaceManager()
        for floor in range(1, num_of_floors + 1):
            num_of_desks, floor_type = input().split()
            num_of_desks = int(num_of_desks)
            if floor_type == 'free':
                price = 0
            elif floor_type == 'special':
                price = special_floor_price
            self.__manager.add_floor(floor_type, price)
            self.__manager.add_desk(floor, num_of_desks)
        self.__run()
        
    def __get_cmd(self):
        return input().split()
    
    def __run(self):
        while True:
            try:
                cmd = self.__get_cmd()
                if cmd[0] == 'end':
                    break
                ts = int(cmd[0])
                if cmd[1] == 'request_desk':
                    username = cmd[2]
                    floor_type = cmd[3]
                    duration = int(cmd[4])
                    desk_id, price = self.__manager.get_desk(ts, username, floor_type, duration)
                    if price:
                        print(f"{username} got desk {desk_id} for {price}")
                    else:
                        print(f"{username} got desk {desk_id}")
            except NoDeskException as err:
                print('no desk available')
    

if __name__ == '__main__':
    UserInterface()
