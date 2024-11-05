import pytest
import time
import signal

from steps.proxy_steps import run_proxy_with_args, start_proxy, send_signal
from steps.logger_steps import wait_for_log_message
from entities.proxy import Proxy

def test_proxy_with_empty_config(project_dir, proxy_bin_name, tmp_path):
    empty_config = tmp_path / "empty.conf"
    proxy = Proxy(config_path=empty_config)
    
    result = run_proxy_with_args(
        project_dir=project_dir,
        proxy_bin_name=proxy_bin_name,
        args=["-c", str(empty_config)]
    )
    
    assert result.returncode == 0, "Proxy failed to start with an empty config"
    assert "Using default configuration" in result.stdout or "Error" in result.stderr, "Unexpected behavior with empty config"
 
def test_proxy_without_config(project_dir, proxy_bin_name):
    result = run_proxy_with_args(
        project_dir=project_dir,
        proxy_bin_name=proxy_bin_name,
        args=[]
    )
    
    assert result.returncode == 0, "Proxy failed to start without config"
    assert "Using default configuration" in result.stdout or "Error" in result.stderr, "Unexpected behavior without config"
 
@pytest.mark.parametrize("config_content", [
    'option_without_equals',           # отсутствует знак "="
    'invalid_option = "value"',        # неверная опция
    'correct_option = "missing_quote', # отсутствует закрывающая кавычка
    'correct_option "no_equals"',      # нет знака "="
])
def test_proxy_with_invalid_config(project_dir, proxy_bin_name, tmp_path, config_content):
    invalid_config = tmp_path / "invalid.conf"
    proxy = Proxy(config_path=invalid_config)
    proxy.update_config(config_content)
    
    result = run_proxy_with_args(
        project_dir=project_dir,
        proxy_bin_name=proxy_bin_name,
        args=["-c", str(invalid_config)]
    )
    
    assert result.returncode != 0, "Proxy should fail with invalid config"
    assert "Error" in result.stderr, "Proxy did not report error for invalid config"
 
def test_proxy_with_large_config(project_dir, proxy_bin_name, tmp_path):
    large_config = tmp_path / "large.conf"
    proxy = Proxy(config_path=large_config)
    
    # Создание конфигурационного файла размером 1ГБ, где значимая часть — в конце
    proxy.update_config("\n" * (1024 * 1024 * 1024 - 100) + 'valid_option="value"')
    
    result = run_proxy_with_args(
        project_dir=project_dir,
        proxy_bin_name=proxy_bin_name,
        args=["-c", str(large_config)]
    )
    
    assert result.returncode == 0, "Proxy failed to start with large config"
    assert "Configuration loaded successfully" in result.stdout, "Proxy did not handle large config correctly"
  
@pytest.mark.xfail(reason="SIGHUP handling not yet implemented")
def test_proxy_reload_config(project_dir, proxy_bin_name, tmp_path, proxy_timeout, log_file_path):
    config = tmp_path / "proxy.conf"
    proxy = Proxy(config_path=config)
    proxy.update_config('option="initial_value"')
    
    # Запускаем прокси
    proc = start_proxy(project_dir, proxy_bin_name, args=["-c", str(config)])
    time.sleep(proxy_timeout)
    
    try:
        # Изменяем конфигурацию
        proxy.update_config('option="new_value"')
        send_signal(proc, signal.SIGHUP)
        
        # Проверяем, что файл конфигурации был изменен
        assert proxy.has_config_changed(), "Config file modification time did not update after SIGHUP"

        # Ожидаем сообщение об обновлении в логе
        line_number, line_content = wait_for_log_message(
            log_file_path=log_file_path,
            start_position=0,
            message="Configuration reloaded",
            timeout=proxy_timeout
        )
        
        assert "Configuration reloaded" in line_content, "Proxy did not reload config correctly after SIGHUP"
    finally:
        send_signal(proc, signal.SIGINT)
        proc.wait(timeout=proxy_timeout)
