#!/usr/bin/env python3

import json
import argparse
import uuid


def normalize_chrome_trace(input_chrome_trace):
    output_normalized_chrome_trace = input_chrome_trace.copy()
    normalized_trace_events = []
    for i, event in enumerate(input_chrome_trace['traceEvents']):
        if 'ph' not in event:
            print(
                '[warning] There is no "ph" field at ".traceEvents[{}]"'.format(i))
            continue
        if event['ph'] == 'X':
            trace_event_b = event.copy()
            trace_event_b['ph'] = 'B'
            del trace_event_b['dur']
            trace_event_e = event.copy()
            trace_event_e['ph'] = 'E'
            trace_event_e['ts'] = event['ts'] + event['dur']
            del trace_event_e['dur']
            normalized_trace_events.append(trace_event_b)
            normalized_trace_events.append(trace_event_e)
        elif event['ph'] in ['B', 'E']:
            normalized_trace_events.append(event.copy())
        else:
            print(
                '[warning] There is no implementation of ".traceEvents[{}].ph": "{}"'.format(
                    i, event['ph']))
            continue
    normalized_trace_events = sorted(
        normalized_trace_events,
        key=lambda x: x['ts'])
    output_normalized_chrome_trace['traceEvents'] = normalized_trace_events
    return output_normalized_chrome_trace


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
