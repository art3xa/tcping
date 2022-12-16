from typing import List


def print_statistics(ip: str, all_times: List[float | None]):
    """ Print statistics of the ping """
    len_times = len(all_times)
    amount_received = sum([0 if time is None else 1 for time in all_times])
    amount_loss = len_times - amount_received
    received_times = [time for time in all_times if time is not None]
    if len(received_times) == 0:
        print(f'\n--- {ip} ping statistics ---')
        print(f'{len_times} packets transmitted, '
              f'0 received, 100% packet loss')
    else:
        loss_percent = int(amount_loss / len_times * 100)
        total_time = round(sum(received_times), 3)
        min_times = round(min(received_times), 3)
        avg_times = round(sum(received_times) / amount_received, 3)
        max_times = round(max(received_times), 3)
        print(f'\n--- {ip} ping statistics ---')
        print(f'{len_times} packets transmitted, {amount_received} received,'
              f' {loss_percent}% packet loss, time {total_time}ms')
        print(f'rtt min/avg/max = {min_times}/{avg_times}/{max_times} ms')
