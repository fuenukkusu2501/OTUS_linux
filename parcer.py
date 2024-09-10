import subprocess
import datetime
import psutil

def parse_ps_aux():
    result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, text=True)

    processes = result.stdout.splitlines()[1:]

    users = {}
    total_memory = 0.0
    total_cpu = 0.0
    max_mem_process = ("", 0.0)
    max_cpu_process = ("", 0.0)

    for process in processes:
        columns = process.split(None, 10)
        user = columns[0]
        cpu = float(columns[2])
        mem = float(columns[3])
        process_name = columns[10][:20]

        if 'ps aux' in process_name or 'python' in process_name:
            continue

        if user in users:
            users[user] += 1
        else:
            users[user] = 1

        total_memory += mem
        total_cpu += cpu

        if mem > max_mem_process[1]:
            max_mem_process = (process_name, mem)
        if cpu > max_cpu_process[1]:
            max_cpu_process = (process_name, cpu)

    num_cores = psutil.cpu_count()

    print("Отчёт о состоянии системы:")
    print(f"Пользователи системы: {', '.join(users.keys())}")
    print(f"Процессов запущено: {len(processes)}")

    print("\nПользовательских процессов:")
    for user, count in users.items():
        print(f"{user}: {count}")

    print(f"\nВсего памяти используется: {total_memory:.1f}%")
    print(f"Всего CPU используется: {total_cpu / num_cores:.1f}% от общего количества ядер")
    print(f"Больше всего памяти использует: {max_mem_process[1]}% {max_mem_process[0]}")
    print(f"Больше всего CPU использует: {max_cpu_process[1] / num_cores:.1f}% {max_cpu_process[0]} от общего количества ядер")

    filename = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M-scan.txt")
    with open(filename, "w") as file:
        file.write(f"Отчёт о состоянии системы:\n")
        file.write(f"Пользователи системы: {', '.join(users.keys())}\n")
        file.write(f"Процессов запущено: {len(processes)}\n\n")
        file.write(f"Пользовательских процессов:\n")
        for user, count in users.items():
            file.write(f"{user}: {count}\n")
        file.write(f"\nВсего памяти используется: {total_memory:.1f}%\n")
        file.write(f"Всего CPU используется: {total_cpu / num_cores:.1f}% от общего количества ядер\n")
        file.write(f"Больше всего памяти использует: {max_mem_process[1]}% {max_mem_process[0]}\n")
        file.write(f"Больше всего CPU использует: {max_cpu_process[1] / num_cores:.1f}% {max_cpu_process[0]} от общего количества ядер\n")

if __name__ == "__main__":
    parse_ps_aux()