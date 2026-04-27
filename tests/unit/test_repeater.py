import pytest
import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock, patch, call
from src.bot.repeater import (
    Repeater,
    RepeaterConfig,
    KeywordMatch,
    MatchType,
    ReplyStrategy,
    get_repeater,
    create_repeater_config
)


class TestKeywordMatching:
    def test_exact_match_found(self):
        config = RepeaterConfig(keywords=["炸群", "举报", "兄弟们"], match_type="exact")
        repeater = Repeater(config=config)
        matches = repeater.match_keyword("大家好啊兄弟们")
        assert len(matches) == 1
        assert matches[0].keyword == "兄弟们"
        assert matches[0].match_type == MatchType.EXACT

    def test_exact_match_multiple(self):
        config = RepeaterConfig(keywords=["炸群", "举报", "兄弟们"], match_type="exact")
        repeater = Repeater(config=config)
        matches = repeater.match_keyword("有人炸群了，举报这个家伙，兄弟们注意")
        assert len(matches) == 3
        assert all(m.match_type == MatchType.EXACT for m in matches)

    def test_exact_match_no_match(self):
        config = RepeaterConfig(keywords=["炸群", "举报", "兄弟们"], match_type="exact")
        repeater = Repeater(config=config)
        matches = repeater.match_keyword("今天天气真好")
        assert len(matches) == 0

    def test_exact_match_empty_text(self):
        config = RepeaterConfig(keywords=["炸群"], match_type="exact")
        repeater = Repeater(config=config)
        matches = repeater.match_keyword("")
        assert len(matches) == 0

    def test_exact_match_none_text(self):
        config = RepeaterConfig(keywords=["炸群"], match_type="exact")
        repeater = Repeater(config=config)
        matches = repeater.match_keyword(None)
        assert len(matches) == 0

    def test_exact_match_non_string_text(self):
        config = RepeaterConfig(keywords=["炸群"], match_type="exact")
        repeater = Repeater(config=config)
        matches = repeater.match_keyword(123)
        assert len(matches) == 0

    def test_regex_match_found(self):
        config = RepeaterConfig(keywords=[r"\d+炸群", r"举[报诉]"], match_type="regex")
        repeater = Repeater(config=config)
        matches = repeater.match_keyword("有人123炸群了")
        assert len(matches) == 1
        assert matches[0].keyword == r"\d+炸群"
        assert matches[0].match_type == MatchType.REGEX

    def test_regex_match_multiple(self):
        config = RepeaterConfig(keywords=[r"炸\w+", r"举\w+"], match_type="regex")
        repeater = Repeater(config=config)
        matches = repeater.match_keyword("有人炸群了，举报这个家伙")
        assert len(matches) == 2

    def test_regex_match_no_match(self):
        config = RepeaterConfig(keywords=[r"\d+炸群"], match_type="regex")
        repeater = Repeater(config=config)
        matches = repeater.match_keyword("有人炸群了")
        assert len(matches) == 0

    def test_regex_match_invalid_pattern(self):
        config = RepeaterConfig(keywords=[r"["], match_type="regex")
        repeater = Repeater(config=config)
        matches = repeater.match_keyword("test")
        assert len(matches) == 0


class TestReplyTemplateRendering:
    def test_render_reply_simple(self):
        config = RepeaterConfig(reply_template="收到关键词【{keyword}】，已记录")
        repeater = Repeater(config=config)
        reply = repeater.render_reply("炸群")
        assert reply == "收到关键词【炸群】，已记录"

    def test_render_reply_custom_template(self):
        config = RepeaterConfig(reply_template="关键词命中: {keyword}")
        repeater = Repeater(config=config)
        reply = repeater.render_reply("举报")
        assert reply == "关键词命中: 举报"

    def test_render_reply_empty_keyword(self):
        config = RepeaterConfig(reply_template="收到关键词【{keyword}】，已记录")
        repeater = Repeater(config=config)
        reply = repeater.render_reply("")
        assert reply == "收到关键词【】，已记录"

    def test_get_replies_separate_strategy(self):
        config = RepeaterConfig(
            keywords=["炸群", "举报"],
            match_type="exact",
            reply_template="收到关键词【{keyword}】，已记录",
            reply_strategy="separate"
        )
        repeater = Repeater(config=config)
        matches = [
            KeywordMatch(keyword="炸群", match_type=MatchType.EXACT, matched_value="炸群"),
            KeywordMatch(keyword="举报", match_type=MatchType.EXACT, matched_value="举报")
        ]
        replies = repeater.get_replies(matches)
        assert len(replies) == 2
        assert "收到关键词【炸群】，已记录" in replies
        assert "收到关键词【举报】，已记录" in replies

    def test_get_replies_merge_strategy(self):
        config = RepeaterConfig(
            keywords=["炸群", "举报"],
            match_type="exact",
            reply_template="收到关键词【{keyword}】，已记录",
            reply_strategy="merge"
        )
        repeater = Repeater(config=config)
        matches = [
            KeywordMatch(keyword="炸群", match_type=MatchType.EXACT, matched_value="炸群"),
            KeywordMatch(keyword="举报", match_type=MatchType.EXACT, matched_value="举报")
        ]
        replies = repeater.get_replies(matches)
        assert len(replies) == 1
        assert replies[0] == "收到关键词【炸群、举报】，已记录"

    def test_get_replies_merge_removes_duplicates(self):
        config = RepeaterConfig(
            keywords=["炸群"],
            match_type="exact",
            reply_template="收到关键词【{keyword}】，已记录",
            reply_strategy="merge"
        )
        repeater = Repeater(config=config)
        matches = [
            KeywordMatch(keyword="炸群", match_type=MatchType.EXACT, matched_value="炸群"),
            KeywordMatch(keyword="炸群", match_type=MatchType.EXACT, matched_value="炸群")
        ]
        replies = repeater.get_replies(matches)
        assert len(replies) == 1
        assert replies[0] == "收到关键词【炸群】，已记录"

    def test_get_replies_empty_matches(self):
        config = RepeaterConfig(reply_template="收到关键词【{keyword}】，已记录")
        repeater = Repeater(config=config)
        replies = repeater.get_replies([])
        assert len(replies) == 0


class TestExceptionRetry:
    @pytest.mark.asyncio
    async def test_send_with_retry_success_first_attempt(self, mocker):
        mock_send_func = AsyncMock(return_value=True)
        config = RepeaterConfig(retry_max_attempts=3, retry_base_delay=0.1)
        repeater = Repeater(config=config, send_func=mock_send_func)

        result = await repeater.send_with_retry(123456, "test message")

        assert result is True
        assert mock_send_func.call_count == 1

    @pytest.mark.asyncio
    async def test_send_with_retry_success_after_retry(self, mocker):
        mock_send_func = AsyncMock(side_effect=[False, False, True])
        config = RepeaterConfig(retry_max_attempts=3, retry_base_delay=0.01)
        repeater = Repeater(config=config, send_func=mock_send_func)

        result = await repeater.send_with_retry(123456, "test message")

        assert result is True
        assert mock_send_func.call_count == 3

    @pytest.mark.asyncio
    async def test_send_with_retry_all_fail(self, mocker):
        mock_send_func = AsyncMock(return_value=False)
        config = RepeaterConfig(retry_max_attempts=3, retry_base_delay=0.01)
        repeater = Repeater(config=config, send_func=mock_send_func)

        result = await repeater.send_with_retry(123456, "test message")

        assert result is False
        assert mock_send_func.call_count == 3

    @pytest.mark.asyncio
    async def test_send_with_retry_timeout(self, mocker):
        mock_send_func = AsyncMock(side_effect=asyncio.TimeoutError("timeout"))
        config = RepeaterConfig(retry_max_attempts=3, retry_base_delay=0.01)
        repeater = Repeater(config=config, send_func=mock_send_func)

        result = await repeater.send_with_retry(123456, "test message")

        assert result is False
        assert mock_send_func.call_count == 3

    @pytest.mark.asyncio
    async def test_send_with_retry_exception(self, mocker):
        mock_send_func = AsyncMock(side_effect=Exception("network error"))
        config = RepeaterConfig(retry_max_attempts=3, retry_base_delay=0.01)
        repeater = Repeater(config=config, send_func=mock_send_func)

        result = await repeater.send_with_retry(123456, "test message")

        assert result is False
        assert mock_send_func.call_count == 3

    @pytest.mark.asyncio
    async def test_send_with_retry_no_send_func(self, mocker):
        config = RepeaterConfig()
        repeater = Repeater(config=config, send_func=None)

        result = await repeater.send_with_retry(123456, "test message")

        assert result is False

    @pytest.mark.asyncio
    async def test_send_with_retry_custom_max_attempts(self, mocker):
        mock_send_func = AsyncMock(side_effect=[False, True])
        config = RepeaterConfig(retry_max_attempts=5, retry_base_delay=0.01)
        repeater = Repeater(config=config, send_func=mock_send_func)

        result = await repeater.send_with_retry(123456, "test message", max_attempts=2)

        assert result is True
        assert mock_send_func.call_count == 2

    @pytest.mark.asyncio
    async def test_send_with_retry_custom_delay(self, mocker):
        mock_send_func = AsyncMock(side_effect=[False, False, True])
        config = RepeaterConfig(retry_max_attempts=3, retry_base_delay=0.1)
        repeater = Repeater(config=config, send_func=mock_send_func)

        result = await repeater.send_with_retry(123456, "test message", base_delay=0.001)

        assert result is True
        assert mock_send_func.call_count == 3


class TestLogOutput:
    def test_handle_message_logs_received(self, mocker, caplog):
        caplog.set_level(logging.INFO)
        mock_send_func = AsyncMock(return_value=True)
        config = RepeaterConfig(keywords=["炸群"], match_type="exact")
        repeater = Repeater(config=config, send_func=mock_send_func)

        data = {
            "post_type": "message",
            "message_type": "group",
            "group_id": 123456,
            "user_id": 7890,
            "raw_message": "有人炸群了"
        }

        async def run_test():
            await repeater.handle_message(data)

        asyncio.run(run_test())

        assert any("Received group message" in record.message for record in caplog.records)
        assert any("Keyword matched" in record.message for record in caplog.records)

    def test_handle_message_logs_no_match(self, mocker, caplog):
        caplog.set_level(logging.INFO)
        mock_send_func = AsyncMock(return_value=True)
        config = RepeaterConfig(keywords=["炸群"], match_type="exact")
        repeater = Repeater(config=config, send_func=mock_send_func)

        data = {
            "post_type": "message",
            "message_type": "group",
            "group_id": 123456,
            "user_id": 7890,
            "raw_message": "今天天气真好"
        }

        async def run_test():
            await repeater.handle_message(data)

        asyncio.run(run_test())

        mock_send_func.assert_not_called()

    def test_handle_message_non_group_ignored(self, mocker, caplog):
        caplog.set_level(logging.INFO)
        mock_send_func = AsyncMock(return_value=True)
        config = RepeaterConfig(keywords=["炸群"], match_type="exact")
        repeater = Repeater(config=config, send_func=mock_send_func)

        data = {
            "post_type": "message",
            "message_type": "private",
            "user_id": 7890,
            "raw_message": "有人炸群了"
        }

        async def run_test():
            await repeater.handle_message(data)

        asyncio.run(run_test())

        mock_send_func.assert_not_called()

    def test_handle_message_non_message_ignored(self, mocker, caplog):
        caplog.set_level(logging.INFO)
        mock_send_func = AsyncMock(return_value=True)
        config = RepeaterConfig(keywords=["炸群"], match_type="exact")
        repeater = Repeater(config=config, send_func=mock_send_func)

        data = {
            "post_type": "event",
            "message_type": "group",
            "raw_message": "有人炸群了"
        }

        async def run_test():
            await repeater.handle_message(data)

        asyncio.run(run_test())

        mock_send_func.assert_not_called()


class TestConfigCreation:
    def test_create_repeater_config_default(self):
        config_dict = {}
        config = create_repeater_config(config_dict)

        assert config.keywords == ["炸群", "举报", "兄弟们"]
        assert config.match_type == "exact"
        assert config.reply_template == "收到关键词【{keyword}】，已记录"
        assert config.reply_strategy == "separate"
        assert config.retry_max_attempts == 3
        assert config.retry_base_delay == 1.0

    def test_create_repeater_config_custom(self):
        config_dict = {
            "repeater": {
                "keywords": ["测试"],
                "match_type": "regex",
                "reply_template": "测试模板: {keyword}",
                "reply_strategy": "merge",
                "retry_max_attempts": 5,
                "retry_base_delay": 2.0
            }
        }
        config = create_repeater_config(config_dict)

        assert config.keywords == ["测试"]
        assert config.match_type == "regex"
        assert config.reply_template == "测试模板: {keyword}"
        assert config.reply_strategy == "merge"
        assert config.retry_max_attempts == 5
        assert config.retry_base_delay == 2.0

    def test_create_repeater_config_partial(self):
        config_dict = {
            "repeater": {
                "keywords": ["自定义"]
            }
        }
        config = create_repeater_config(config_dict)

        assert config.keywords == ["自定义"]
        assert config.match_type == "exact"
        assert config.reply_template == "收到关键词【{keyword}】，已记录"


class TestGetRepeater:
    def test_get_repeater_singleton(self):
        repeater1 = get_repeater()
        repeater2 = get_repeater()
        assert repeater1 is repeater2

    def test_get_repeater_with_config(self):
        config = RepeaterConfig(keywords=["test"])
        repeater = get_repeater(config=config)
        assert repeater.config.keywords == ["test"]

    def test_get_repeater_with_send_func(self):
        mock_func = AsyncMock()
        repeater = get_repeater(send_func=mock_func)
        assert repeater._send_func is mock_func


class TestRepeaterIntegration:
    @pytest.mark.asyncio
    async def test_handle_message_full_flow_separate(self, mocker):
        caplog_handler = MagicMock()
        handler = logging.Handler()
        handler.emit = caplog_handler

        mock_send_func = AsyncMock(return_value=True)
        config = RepeaterConfig(
            keywords=["炸群", "举报"],
            match_type="exact",
            reply_template="收到关键词【{keyword}】，已记录",
            reply_strategy="separate",
            retry_max_attempts=1,
            retry_base_delay=0.01
        )
        repeater = Repeater(config=config, send_func=mock_send_func)

        data = {
            "post_type": "message",
            "message_type": "group",
            "group_id": 123456,
            "user_id": 7890,
            "raw_message": "有人炸群了，举报一下"
        }

        await repeater.handle_message(data)

        assert mock_send_func.call_count == 2
        mock_send_func.assert_any_call(123456, "收到关键词【炸群】，已记录")
        mock_send_func.assert_any_call(123456, "收到关键词【举报】，已记录")

    @pytest.mark.asyncio
    async def test_handle_message_full_flow_merge(self, mocker):
        mock_send_func = AsyncMock(return_value=True)
        config = RepeaterConfig(
            keywords=["炸群", "举报"],
            match_type="exact",
            reply_template="收到关键词【{keyword}】，已记录",
            reply_strategy="merge",
            retry_max_attempts=1,
            retry_base_delay=0.01
        )
        repeater = Repeater(config=config, send_func=mock_send_func)

        data = {
            "post_type": "message",
            "message_type": "group",
            "group_id": 123456,
            "user_id": 7890,
            "raw_message": "有人炸群了，举报一下"
        }

        await repeater.handle_message(data)

        assert mock_send_func.call_count == 1
        mock_send_func.assert_called_once_with(123456, "收到关键词【炸群、举报】，已记录")
