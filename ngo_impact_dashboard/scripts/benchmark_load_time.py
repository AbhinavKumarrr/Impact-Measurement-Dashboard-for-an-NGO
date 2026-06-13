"""Benchmark API and dashboard load times. Target: < 3 seconds."""
import os
import statistics
import sys
import time
from urllib.request import urlopen
from urllib.error import URLError

API_URL = os.getenv("BENCHMARK_API_URL", "http://127.0.0.1:8000/api/dashboard")
HEALTH_URL = os.getenv("BENCHMARK_HEALTH_URL", "http://127.0.0.1:8000/api/health")
TARGET_SECONDS = 3.0
RUNS = 10
WARMUP = 2


def timed_get(url: str) -> tuple[float, int]:
    start = time.perf_counter()
    with urlopen(url, timeout=30) as resp:
        data = resp.read()
        elapsed = time.perf_counter() - start
        return elapsed, len(data)


def main():
    print("NGO Impact Dashboard — Performance Benchmark")
    print(f"Target: page load < {TARGET_SECONDS}s")
    print("-" * 50)

    try:
        health_elapsed, _ = timed_get(HEALTH_URL)
        print(f"Health check:     {health_elapsed*1000:.0f} ms")
    except URLError:
        print("ERROR: API not running. Start with:")
        print("  cd api && uvicorn main:app --port 8000")
        sys.exit(1)

    print(f"Warming cache ({WARMUP} requests)...")
    for _ in range(WARMUP):
        timed_get(API_URL)

    times = []
    sizes = []
    for i in range(RUNS):
        elapsed, size = timed_get(API_URL)
        times.append(elapsed)
        sizes.append(size)
        print(f"  Run {i+1:2d}: {elapsed*1000:6.0f} ms  ({size:,} bytes)")

    avg = statistics.mean(times)
    p95 = sorted(times)[int(len(times) * 0.95)]
    max_t = max(times)

    # Estimate full page load: API + JS parse/render (~0.3s cached assets, ~1.2s first visit)
    render_overhead = 0.3 if avg < 0.1 else 1.2
    estimated_page_load = avg + render_overhead

    print("-" * 50)
    print(f"API avg:          {avg*1000:.0f} ms")
    print(f"API p95:          {p95*1000:.0f} ms")
    print(f"API max:          {max_t*1000:.0f} ms")
    print(f"Avg payload:      {statistics.mean(sizes):,.0f} bytes")
    print(f"Est. page load:   {estimated_page_load:.2f} s (API + render)")
    print("-" * 50)

    api_pass = p95 < 1.0  # API alone should be well under 1s cached
    page_pass = estimated_page_load < TARGET_SECONDS

    if api_pass and page_pass:
        print(f"RESULT: PASS — under {TARGET_SECONDS}s target")
        sys.exit(0)
    else:
        print(f"RESULT: FAIL — exceeds {TARGET_SECONDS}s target")
        if not api_pass:
            print(f"  API p95 ({p95:.2f}s) exceeds 1s cached threshold")
        if not page_pass:
            print(f"  Est. page load ({estimated_page_load:.2f}s) exceeds target")
        sys.exit(1)


if __name__ == "__main__":
    main()
