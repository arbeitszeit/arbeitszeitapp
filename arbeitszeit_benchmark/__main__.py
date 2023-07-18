from __future__ import annotations

import argparse
import timeit
from dataclasses import dataclass
from typing import Dict, Optional

from typing_extensions import Self

from .get_company_transactions import GetCompanyTransactionsBenchmark
from .get_statistics import GetStatisticsBenchmark
from .runner import BenchmarkCatalog, BenchmarkResult, render_results_as_json
from .show_prd_account_details_benchmark import ShowPrdAccountDetailsBenchmark


def main() -> None:
    arguments = parse_arguments()
    configuration = Configuration.from_arguments(arguments)
    results: Dict[str, BenchmarkResult] = dict()
    catalog = BenchmarkCatalog()
    catalog.register_benchmark(
        name="get_company_transactions", benchmark_class=GetCompanyTransactionsBenchmark
    )
    catalog.register_benchmark(
        name="show_prd_account_details", benchmark_class=ShowPrdAccountDetailsBenchmark
    )
    catalog.register_benchmark(
        name="get_statistics", benchmark_class=GetStatisticsBenchmark
    )
    for name, benchmark_class in catalog.get_all_benchmarks():
        if (configuration.include_filter or "") not in name:
            continue
        benchmark = benchmark_class()
        try:
            average_benchmark_time = (
                timeit.timeit(benchmark.run, number=configuration.repeats)
                / configuration.repeats
            )
        finally:
            benchmark.tear_down()
        results[name] = BenchmarkResult(
            name=name, average_execution_time_in_secs=average_benchmark_time
        )
    print(render_results_as_json(results))


@dataclass
class Configuration:
    repeats: int
    include_filter: Optional[str]

    @classmethod
    def from_arguments(cls, arguments: argparse.Namespace) -> Self:
        return cls(
            repeats=arguments.repeats,
            include_filter=arguments.include,
        )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include", "-i", default=None)
    parser.add_argument("--repeats", "-n", type=int, default=5)
    return parser.parse_args()


main()
