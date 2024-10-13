from typing import List, Optional

from src.message import Message
from src.randomizer import rand_phone_number, rand_text


class Producer:
    def __init__(self, num_msgs: int = 1000):
        self.num_msgs: int = num_msgs
        self.msgs: List[Message] = []
        self.current_msg_index: int = 0
        self._generate()

    def _generate(self):
        for i in range(self.num_msgs):
            self.msgs.append(Message(rand_phone_number(), rand_text()))

    def has_next(self) -> bool:
        return self.current_msg_index < self.num_msgs

    def next(self) -> Optional[Message]:
        if self.current_msg_index < self.num_msgs:
            msg = self.msgs[self.current_msg_index]
            self.current_msg_index += 1
            return msg
        return None
