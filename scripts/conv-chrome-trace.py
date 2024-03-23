#!/usr/bin/env python3

import json
import argparse
import uuid


def convert_json_to_chrome_trace(
        input_file, output_chrome_trace_file):
    with open(input_file, 'r') as f:
        json_data = json.load(f)

    events = []
    for data in json_data:
        event = {
            "ph": "X",
            "cat": "cat",
            "name": data["name"],
            "pid": "pid",
            "tid": "tag:{}".format(data["tag"]),
            "ts": data["start_time"] * 1000,  # ms to us
            "dur": data["duration"] * 1000,  # ms to us
            "args": {
            }
        }
        events.append(event)
    trace_data = {
        "traceEvents": events,
    }

    with open(output_chrome_trace_file, 'w') as f:
        json.dump(trace_data, f, indent=4)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--output-filepath', default='/dev/stdout')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('input_filepath')
    parser.add_argument('args', nargs='*')

    args, extra_args = parser.parse_known_args()
    convert_json_to_chrome_trace(
        args.input_filepath,
        args.output_filepath)


if __name__ == '__main__':
    main()
