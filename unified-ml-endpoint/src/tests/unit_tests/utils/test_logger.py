import logging
import os
import re
import time
from unittest.mock import MagicMock, patch

from ada.utils.logs.time_logger import log_time


def test_log_time():
    # Mocking the logger to capture log messages
    with patch(
        "ada.utils.logs.time_logger.time_logger", new=MagicMock(spec=logging.Logger)
    ) as mock_logger:

        @log_time
        def test_func():
            time.sleep(0.1)
            return "Test function executed"

        result = test_func()

        # Asserting that the function returned the correct result
        assert result == "Test function executed"

        # Asserting that the logger was called with the correct arguments
        file_name = os.path.basename(__name__)
        mock_logger.info.assert_called_once()
        log_message = mock_logger.info.call_args[0][0] % mock_logger.info.call_args[0][1:]
        assert "test_func" in log_message
        assert file_name in log_message
        assert (
            0.09 <= float(re.findall(r"took (\d+\.\d+) s", log_message)[0]) <= 0.11
        ), "Time not within range"
