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
    def __init__(self, number: int, num_of_desks=0):
        self.__id = number
        self.__desks = [Desk(i, self.__id) for i in range(1, num_of_desks + 1)]


    def get_desk(self, ts: int, duration: int):
        for desk in self.__desks:
            if desk.reserve(ts, duration):
                return desk.id
        raise NoDeskException()

    def add_desk(self):
        self.__desks.append(Desk(len(self.__desks) + 1, self.__id))

    
class WorkSpaceManager:
    def __init__(self, num_of_floors: int):
        self.__floors = [Floor(i) for i in range(1, num_of_floors + 1)]

    def add_desk(self, floor: int, num=1):
        for _ in range(num):
            self.__floors[floor - 1].add_desk()

    def get_desk(self, ts: int, username: str, duration: int):
        for floor in self.__floors:
            try:
                return floor.get_desk(ts, duration)
            except NoDeskException:
                continue
        raise NoDeskException()
    

class UserInterface:
    def __init__(self):
        num_of_floors = int(input())
        self.__manager = WorkSpaceManager(num_of_floors)
        for floor in range(1, num_of_floors + 1):
            num_of_desks = int(input())
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
                    duration = int(cmd[3])
                    desk_id = self.__manager.get_desk(ts, username, duration)
                    print(f"{username} got desk {desk_id}")
            except NoDeskException as err:
                print('no desk available')
    

if __name__ == '__main__':
    UserInterface()
