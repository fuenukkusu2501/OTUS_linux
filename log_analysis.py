import os
import re
import json
import argparse
from collections import defaultdict

LOG_PATTERN = r'(?P<ip>\S+) - - \[(?P<date>[^\]]+)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d+) (?P<bytes>\S+) "(?P<referer>[^\"]*)" "(?P<user_agent>[^\"]*)" (?P<duration>\d+)'


def parse_log_line(line):
    match = re.match(LOG_PATTERN, line)
    if match:
        return match.groupdict()
    return None


def process_log_file(log_file):
    methods_count = defaultdict(int)
    total_requests = 0
    ip_count = defaultdict(int)
    longest_requests = []

    with open(log_file, 'r') as file:
        for line in file:
            parsed_data = parse_log_line(line)
            if parsed_data:
                total_requests += 1
                methods_count[parsed_data['method']] += 1
                ip_count[parsed_data['ip']] += 1
                request_info = {
                    "ip": parsed_data['ip'],
                    "date": parsed_data['date'],
                    "method": parsed_data['method'],
                    "url": parsed_data['url'],
                    "duration": int(parsed_data['duration'])
                }
                longest_requests.append(request_info)

    longest_requests = sorted(longest_requests, key=lambda x: x['duration'], reverse=True)[:3]
    top_ips = sorted(ip_count.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        "top_ips": {ip: count for ip, count in top_ips},
        "top_longest": longest_requests,
        "total_stat": methods_count,
        "total_requests": total_requests
    }


def process_logs(path):
    if os.path.isfile(path):
        return [process_log_file(path)]
    elif os.path.isdir(path):
        results = []
        for log_file in os.listdir(path):
            log_file_path = os.path.join(path, log_file)
            if os.path.isfile(log_file_path):
                results.append(process_log_file(log_file_path))
        return results
    else:
        raise ValueError(f"Path {path} is neither a file nor a directory")


def save_to_json(results, output_dir):
    for i, result in enumerate(results):
        output_file = os.path.join(output_dir, f'result_{i + 1}.json')
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=4)


def main():
    parser = argparse.ArgumentParser(description="Parse web server access logs.")
    parser.add_argument('path', help="Path to log file or directory with logs.")
    parser.add_argument('--output', help="Output directory for JSON results.", default='.')
    args = parser.parse_args()

    results = process_logs(args.path)

    for result in results:
        print(json.dumps(result, indent=4))

    save_to_json(results, args.output)


if __name__ == "__main__":
    main()
