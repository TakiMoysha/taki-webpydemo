#!/usr/bin/env python

import argparse

import httpx

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--base_url", type=str, default="http://localhost:8000/")

    args = parser.parse_args()

    r = httpx.get(f"{args.base_url}/api/healthcheck")

    assert r.status_code == 200
