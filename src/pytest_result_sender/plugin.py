"""
@Filename:  plugin
@Author:    szkingdom-11
@Time:      2024/12/23  15:02
"""
import pytest
from datetime import datetime, timedelta

data = {}

def pytest_runtest_logreport(report):
    # 每个测试用例执行完毕之后执行，可以获取到测试用例的执行结果
    if report.when == "call":    # 只处理call阶段的测试用例
        if report.outcome == "passed":
            data["passed"] = data.get("passed", 0) + 1
        elif report.outcome == "failed":
            data["failed"] = data.get("failed", 0) + 1
        elif report.outcome == "skipped":
            data["skipped"] = data.get("skipped", 0) + 1
        print(f"测试用例{report.nodeid}执行完毕，结果：{report.outcome}")

def pytest_collection_finish(session: pytest.Session):
    # 收集测试用例结束之后执行，所有测试用例收集完毕之后执行
    data["total"] = len(session.items)
    print(f"总共收集到{data['total']}个测试用例")

def pytest_configure():
    # 配置加载完毕之后执行，所有测试用例执行前执行
    data["start_time"] = datetime.now()
    print(f"{datetime.now()}  pytest开始执行")


def pytest_unconfigure():
    # 配置卸载之后执行，所有测试用例执行完毕之后执行
    data["end_time"] = datetime.now()
    print(f"{datetime.now()}  pytest结束执行")

    data["duration"] = data["end_time"] - data["start_time"]
    print(f"测试用例执行时间：{data['duration']}")
    # assert timedelta(seconds=3) > data["duration"] >= timedelta(seconds=2.5)
    assert data['total'] == 3

