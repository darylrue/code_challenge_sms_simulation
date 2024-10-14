from queue import Queue

from src.message import Message
from src.randomizer import rand_phone_number, rand_text


def gen_msg_queue(num_msgs: int = 1000) -> Queue[Message]:
    q: Queue[Message] = Queue(maxsize=num_msgs)
    for _ in range(num_msgs):
        q.put(Message(rand_phone_number(), rand_text()))
    return q
