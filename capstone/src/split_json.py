#!/usr/bin/env python

import json


def main():
    with open("../data/London_weather.json", "r") as fin:
        data = json.load(fin)

    print(type(data), len(data), data[0])

    step = len(data) // 3

    for i in range(3):
        temp = [str(x).replace("'", '"') for x in data[i * step : (i + 1) * step]]
        print(i * step, (i + 1) * step, len(temp))
        with open(f"../data/London_weather_{i}.json", "w") as fout:
            fout.write("\n".join(temp))


if __name__ == "__main__":
    main()
