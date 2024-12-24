"""
@Filename:  plugin
@Author:    szkingdom-11
@Time:      2024/12/23  15:02
"""

from datetime import datetime, timedelta

import pytest
import requests

data = {
    "failed": 0,
    "passed": 0,
}


def pytest_addoption(parser):
    parser.addini(
        "send_when",
        help="何时发送结果"
    )
    parser.addini(
        "send_api",
        help="结果发往何处"
    )


def pytest_runtest_logreport(report: pytest.TestReport):
    print(report)
    if report.when == "call":
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    # 收集测试用例结束之后执行，所有测试用例收集完毕之后执行
    data["total"] = len(session.items)
    print(f"总共收集到{data['total']}个测试用例")


def pytest_configure(config: pytest.Config):
    # 配置加载完毕之后执行，所有测试用例执行前执行
    data["start_time"] = datetime.now()

    data["send_when"] = config.getini("send_when")
    data["send_api"] = config.getini("send_api")


def pytest_unconfigure():
    # 配置卸载之后执行，所有测试用例执行完毕之后执行
    data["end_time"] = datetime.now()

    data["duration"] = data["end_time"] - data["start_time"]
    data["pass_ratio"] = f"{(data['passed'] / data['total'] * 100):.2f}%"
    # print(f"测试用例执行时间：{data['duration']}")
    # assert timedelta(seconds=3) > data["duration"] >= timedelta(seconds=2.5)
    # assert data["total"] == 3
    # assert data["passed"] == 2
    # assert data["failed"] == 1
    # assert data["pass_ratio"] == "66.67%"
    data["duration"] = remove_leading_zeros_in_time(data["duration"])

    send_result()


def send_result():
    if data["send_when"] == "on_fail" and data["failed"] == 0:
        # 如果配置失败才发送，但实际没有失败，则不发送结果
        return  # 不发送结果
    if not data["send_api"]:
        # 如果没有配置结果发送位置，则不发送结果
        return  # 不发送结果

    url = data["send_api"]  # 动态指定结果发送位置

    content = f"""
    pytest 自动化测试报告
    
    测试时间：{data["end_time"]} 
    用例数量：{data['total']} 
    执行时长：{data['duration']} 
    测试通过：{data['passed']}
    测试失败：{data['failed']}
    通过率：{data['pass_ratio']}
    
    测试报告地址：http://192.168.1.100:8080/report/pytest_result_sender/report.html
    """

    try:
        requests.post(url, json={"msg_type": "text", "content": {"text": content}})
    except Exception:
        pass

    data['send_done'] = 1  # 发送成功


def remove_leading_zeros_in_time(time_str):
    # 分割时间字符串为小时、分钟、秒和毫秒部分
    parts = str(time_str).split(":")
    if len(parts) == 3:  # 确保时间字符串的格式是 hh:mm:ss.xxxxxx
        hours, minutes, rest = parts[0], parts[1], parts[2]

        # 去掉小时和分钟前面的0（如果它们存在的话）
        if hours in ("0", "00"):
            hours = ""
        else:
            hours = hours.lstrip("0")
        minutes = (
            minutes.lstrip("0") if minutes != "0" else "0"
        )  # 处理'00'分钟为'0'的情况

        # 重新组合时间字符串
        if hours == "" and minutes == "":
            # 如果小时和分钟都是0，则直接返回秒和毫秒部分
            return rest
        elif hours == "":
            # 如果小时是0，则只返回分钟、秒和毫秒部分
            return f"{minutes}:{rest}"
        elif minutes == "":
            # 如果分钟是0，但小时不是0（因为已经处理过'00'小时的情况），则返回小时、秒和毫秒部分
            return f"{hours}:{rest}"
        else:
            # 否则，返回完整的时间字符串（但小时和分钟前面的0已被去掉）
            return f"{hours}:{minutes}:{rest}"
    else:
        # 如果时间字符串的格式不正确，则直接返回原始字符串
        return time_str
