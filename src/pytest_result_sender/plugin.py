"""
@Filename:  plugin
@Author:    szkingdom-11
@Time:      2024/12/23  15:02
"""

from datetime import datetime, timedelta

data = {

}


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
    assert timedelta(seconds=3) > data["duration"] >= timedelta(seconds=2.5)
