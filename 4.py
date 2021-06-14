class NoDeskException(Exception):
    def __init__(self, message=''):
        super().__init__(message)


class Desk:
    def __init__(self, number: int, floor: int, feature_code: str):
        self.__id = f"{floor}-{number}"
        self.__reserves = []
        self.__feature = feature_code

    @property
    def feature(self):
        return self.__feature

    class Reservation:
        def __init__(self, start: int, end: int):
            self.__start = start
            self.__end = end
        
        def contains(self, t: int) -> bool:
            return self.__start <= t < self.__end

    
    @property
    def id(self):
        return self.__id

    def reserve(self, ts: int, duration: int, feature_code: str) -> bool:
        if self.__feature != feature_code:
            return False
        return self.request(ts, duration)

    def request(self, ts: int, duration: int):
        for t in range(ts, ts + duration):
            for reserve in self.__reserves:
                if reserve.contains(t):
                    return False
        self.__reserves.append(Desk.Reservation(ts, ts + duration))
        return True


class Floor:
    def __init__(self, number: int, floor_type: str, price: list, num_of_desks=0):
        self.__id = number
        self.__desks = [Desk(i, self.__id, price) for i in range(1, num_of_desks + 1)]
        self.__type = floor_type
        self.__price = price
    
    @property
    def type(self):
        return self.__type

    def add_desk(self, feature_code: str):
        self.__desks.append(Desk(len(self.__desks) + 1, self.__id, feature_code))

    def get_desk(self, ts: int, duration: int):
        for desk in self.__desks:
            if desk.request(ts, duration):
                feature_code = desk.feature
                price = self.__price[0] + sum([self.__price[i] * duration for i in range(1, len(self.__price)) if feature_code[i - 1] == '1'])
                return (desk.id, price)
        raise NoDeskException()

    def reserve_desk(self, start_time: int, duration: int, feature_code: str):
        if self.__type != 'special':
            raise NoDeskException()
        for desk in self.__desks:
            if desk.reserve(start_time, duration, feature_code):
                price = self.__price[0] + sum([self.__price[i] * duration for i in range(1, len(self.__price)) if feature_code[i - 1] == '1'])
                return (desk.id, price)
        raise NoDeskException()

    
class WorkSpaceManager:
    def __init__(self, num_of_floors=0):
        self.__floors = [Floor(i) for i in range(1, num_of_floors + 1)]

    def add_desk(self, floor: int, feature_code: str):
        self.__floors[floor - 1].add_desk(feature_code)

    def get_desk(self, ts: int, username: str, floor_type: str, duration: int):
        for floor in self.__floors:
            if floor.type == floor_type:
                try:
                    return floor.get_desk(ts, duration)
                except NoDeskException:
                    continue
        raise NoDeskException()

    def reserve_desk(self, start_time, username: str, duration: int, feature_code: str):
        for floor in self.__floors:
            try:
                return floor.reserve_desk(start_time, duration, feature_code)
            except NoDeskException:
                continue
        raise NoDeskException()

    def add_floor(self, type: str, price: list):
        self.__floors.append(Floor(len(self.__floors) + 1, type, price))
    

class UserInterface:
    def __init__(self):
        num_of_features = int(input())
        features_price = [int(x) for x in input().split()]
        num_of_floors, special_floor_price = [int(x) for x in input().split()]
        self.__manager = WorkSpaceManager()
        for floor in range(1, num_of_floors + 1):
            num_of_desks, floor_type = input().split()
            num_of_desks = int(num_of_desks)
            features_code = input().split()
            price = []
            if floor_type == 'free':
                price.append(0)
            elif floor_type == 'special':
                price.append(special_floor_price)
            price.extend(features_price)
            self.__manager.add_floor(floor_type, price)
            for i in range(num_of_desks):
                self.__manager.add_desk(floor, features_code[i])
        self.__run()
        
    def __get_cmd(self):
        return input().split()
    
    def __run(self):
        while True:
            try:
                cmd = self.__get_cmd()
                if cmd[0] == 'end':
                    break
                if cmd[1] == 'request_desk':
                    self.__handle_request_desk_cmd(cmd)
                elif cmd[1] == 'reserve_desk':
                    self.__handle_reserve_desk_cmd(cmd)
            except NoDeskException as err:
                print('no desk available')

    def __handle_request_desk_cmd(self, cmd: list):
        ts = int(cmd[0])
        username = cmd[2]
        floor_type = cmd[3]
        duration = int(cmd[4])
        desk_id, price = self.__manager.get_desk(ts, username, floor_type, duration)
        print(f"{username} got desk {desk_id} for {price}")
    
    def __handle_reserve_desk_cmd(self, cmd: list):
        username = cmd[2]
        start_time = int(cmd[3])
        duration = int(cmd[4])
        feature_code = cmd[5]
        desk_id, price = self.__manager.reserve_desk(start_time, username, duration, feature_code)
        print(f"{username} reserved desk {desk_id} for {price}")

    
if __name__ == '__main__':
    UserInterface()
