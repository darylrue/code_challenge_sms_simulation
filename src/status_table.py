import time
from queue import Queue
from typing import Optional

from rich.live import Live
from rich.table import Table

from src.message import Message
from src.monitor import Monitor, MonitorStatus


def display(
        input_q: Queue[Message],
        monitor: Monitor,
        total_num_msgs: int,
        display_update_secs: Optional[float] = None) -> None:
    """
    Display the status of the message processing in a table format.

    :param input_q: the queue from which messages are being processed
    :param monitor: the Monitor object that is tracking the status of the message processing
    :param total_num_msgs: the total number of messages to be processed
    :param display_update_secs: the number of seconds to wait between updates to the display (Default: 0.75)
    :return: None
    """
    if display_update_secs is None:
        display_update_secs = 0.75

    print()
    with Live(_generate_table(monitor.status(), total_num_msgs), refresh_per_second=4) as live:
        while not input_q.empty():
            live.update(_generate_table(monitor.status(), total_num_msgs))
            time.sleep(display_update_secs)
        live.update(_generate_table(monitor.status(), total_num_msgs))
    print()


def _generate_table(status: MonitorStatus, total_num_msgs: int) -> Table:
    table = Table(title='Message Processing Status')
    table.add_column('Messages Sent', style='cyan', justify='center')
    table.add_column('Messages Failed', style='red', justify='center')
    table.add_column('Avg. Time per Message', style='blue', justify='center')
    table.add_column('Total Messages Processed', style='green', justify='center')
    table.add_column('Percentage of Messages Processed', style='magenta', justify='center')

    num_msgs_processed = status.num_msgs_sent + status.num_msgs_failed
    percentage_processed = (num_msgs_processed / total_num_msgs) * 100

    table.add_row(
        str(status.num_msgs_sent),
        str(status.num_msgs_failed),
        str(status.avg_time_per_msg),
        str(num_msgs_processed),
        f'{round(percentage_processed)}%'
    )
    return table
