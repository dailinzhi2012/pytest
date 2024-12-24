"""
 ---encoding:utf-8---
@Time    : 2024/12/24 12:38
@Author  : szkingdom-11
@File    : pytest_ini
@Project : pytest-result-sender
@Software: PyCharm
"""

from pathlib import Path
from pytest_result_sender import plugin
import pytest

pytest_plugins = "pytester"  # 我是测试开发


@pytest.fixture(autouse=True)
def mock():
    bak_data = plugin.data
    plugin.data = {
        "passed": 0,
        "failed": 0,
    }

    # 创建一个干净的测试环境
    yield

    # 恢复测试环境
    plugin.data = bak_data


@pytest.mark.parametrize(
    'send_when',
    ['every', 'on_fail']
)
def test_send_when(send_when, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(f"""
[pytest]
send_when = {send_when}
send_api = http://baidu.com
    """)
    # 断言：配置加载成功
    config = pytester.parseconfig(str(config_path))
    assert config.getini('send_when') == send_when

    pytester.makepyfile(  # 构造场景，用例全部测试通过
        """  
        def test_pass():
            assert 1 == 1
            """)
    pytester.runpytest("-c", str(config_path))  # 执行测试用例

    # 如何断言，插件到底有没有发送结果？
    print(plugin.data)
    if send_when == 'every':
        assert plugin.data['send_done'] == 1
    else:
        assert plugin.data.get('send_done') is None


@pytest.mark.parametrize(
    'send_api',
    ['http://baidu.com', '']
)
def test_send_api(send_api, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(f"""
[pytest]
send_when = every
send_api = {send_api}
    """)
    # 断言：配置加载成功
    config = pytester.parseconfig(str(config_path))
    assert config.getini('send_api') == send_api

    pytester.makepyfile(  # 构造场景，用例全部测试通过
        """  
        def test_pass():
            assert 1 == 1
            """)

    pytester.runpytest("-c", str(config_path))
# 如何断言，插件到底有没有发送结果？
    if send_api:
        assert plugin.data['send_done'] == 1
    else:
        assert plugin.data.get('send_done') is None