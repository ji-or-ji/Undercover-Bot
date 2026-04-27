import pytest
import os
import time
import asyncio
from fastapi.testclient import TestClient
from src.bot.main import app, process_message, is_at_bot, send_group_msg, BOT_QQ, AT_REPLY_TEXT, MAX_RETRIES

client = TestClient(app)

class TestIsAtBot:
    def test_at_bot_with_matching_qq(self, mocker):
        mocker.patch("src.bot.main.BOT_QQ", 123456)
        data = {
            "message": [
                {"type": "at", "data": {"qq": "123456"}}
            ]
        }
        assert is_at_bot(data) is True

    def test_at_bot_with_non_matching_qq(self, mocker):
        mocker.patch("src.bot.main.BOT_QQ", 123456)
        data = {
            "message": [
                {"type": "at", "data": {"qq": "999999"}}
            ]
        }
        assert is_at_bot(data) is False

    def test_at_bot_with_no_at_segment(self, mocker):
        mocker.patch("src.bot.main.BOT_QQ", 123456)
        data = {
            "message": [
                {"type": "text", "data": {"text": "hello"}}
            ]
        }
        assert is_at_bot(data) is False

    def test_at_bot_with_empty_message(self, mocker):
        mocker.patch("src.bot.main.BOT_QQ", 123456)
        data = {"message": []}
        assert is_at_bot(data) is False

    def test_at_bot_with_string_message(self, mocker):
        mocker.patch("src.bot.main.BOT_QQ", 123456)
        data = {"message": "hello world"}
        assert is_at_bot(data) is False

    def test_at_bot_with_all_zero_qq(self, mocker):
        mocker.patch("src.bot.main.BOT_QQ", 0)
        data = {
            "message": [
                {"type": "at", "data": {"qq": "0"}}
            ]
        }
        assert is_at_bot(data) is True


class TestProcessMessageAt:
    def test_process_message_at_bot(self, mocker):
        mocker.patch("src.bot.main.BOT_QQ", 123456)
        mocker.patch("src.bot.main.AT_REPLY_TEXT", "awa")
        data = {
            "post_type": "message",
            "message_type": "group",
            "group_id": 111111,
            "user_id": 7890,
            "message": [
                {"type": "at", "data": {"qq": "123456"}}
            ]
        }
        reply = process_message(data)
        assert reply == "awa"

    def test_process_message_at_bot_with_text(self, mocker):
        mocker.patch("src.bot.main.BOT_QQ", 123456)
        mocker.patch("src.bot.main.AT_REPLY_TEXT", "awa")
        data = {
            "post_type": "message",
            "message_type": "group",
            "group_id": 111111,
            "user_id": 7890,
            "message": [
                {"type": "at", "data": {"qq": "123456"}},
                {"type": "text", "data": {"text": "你好"}}
            ]
        }
        reply = process_message(data)
        assert reply == "awa"

    def test_process_message_private_not_reply(self, mocker):
        mocker.patch("src.bot.main.BOT_QQ", 123456)
        data = {
            "post_type": "message",
            "message_type": "private",
            "user_id": 7890,
            "message": [
                {"type": "at", "data": {"qq": "123456"}}
            ]
        }
        reply = process_message(data)
        assert reply is None

    def test_process_message_at_different_bot(self, mocker):
        mocker.patch("src.bot.main.BOT_QQ", 123456)
        data = {
            "post_type": "message",
            "message_type": "group",
            "group_id": 111111,
            "user_id": 7890,
            "message": [
                {"type": "at", "data": {"qq": "999999"}}
            ]
        }
        reply = process_message(data)
        assert reply is None


class TestSendGroupMsgRetry:
    def test_send_group_msg_success(self, mocker):
        mock_post = mocker.patch("httpx.AsyncClient.post")
        mock_post.return_value.status_code = 200

        import asyncio
        result = asyncio.run(send_group_msg(123456, "test"))
        assert result is True
        assert mock_post.call_count == 1

    def test_send_group_msg_network_error_with_retry(self, mocker):
        mock_post = mocker.patch("httpx.AsyncClient.post", side_effect=Exception("Network error"))

        import asyncio
        result = asyncio.run(send_group_msg(123456, "test"))
        assert result is False
        assert mock_post.call_count == MAX_RETRIES

    def test_send_group_msg_timeout_with_retry(self, mocker):
        mock_post = mocker.patch("httpx.AsyncClient.post", side_effect=Exception("timeout"))

        import asyncio
        result = asyncio.run(send_group_msg(123456, "test"))
        assert result is False
        assert mock_post.call_count == MAX_RETRIES

    def test_send_group_msg_http_error_with_retry(self, mocker):
        mock_response = mocker.MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_post = mocker.patch("httpx.AsyncClient.post", return_value=mock_response)

        import asyncio
        result = asyncio.run(send_group_msg(123456, "test"))
        assert result is False
        assert mock_post.call_count == MAX_RETRIES

    def test_send_group_msg_eventual_success(self, mocker):
        mock_post = mocker.patch("httpx.AsyncClient.post")
        mock_post.side_effect = [Exception("error"), Exception("error"), type("obj", (object,), {"status_code": 200})()]

        import asyncio
        result = asyncio.run(send_group_msg(123456, "test"))
        assert result is True
        assert mock_post.call_count == 3


class TestReceiveMessageEndpoint:
    def test_receive_at_message_reply_awa(self, mocker):
        mock_send = mocker.patch("src.bot.main.send_group_msg", return_value=True)

        response = client.post("/onebot", json={
            "post_type": "message",
            "message_type": "group",
            "group_id": 123456,
            "user_id": 7890,
            "message": [
                {"type": "at", "data": {"qq": str(BOT_QQ)}}
            ]
        })
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        mock_send.assert_called_once_with(123456, "awa")

    def test_receive_non_at_message_no_reply(self, mocker):
        mock_send = mocker.patch("src.bot.main.send_group_msg")

        response = client.post("/onebot", json={
            "post_type": "message",
            "message_type": "group",
            "group_id": 123456,
            "user_id": 7890,
            "raw_message": "hello world"
        })
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        mock_send.assert_not_called()

    def test_receive_at_message_send_failure(self, mocker):
        mock_send = mocker.patch("src.bot.main.send_group_msg", return_value=False)

        response = client.post("/onebot", json={
            "post_type": "message",
            "message_type": "group",
            "group_id": 123456,
            "user_id": 7890,
            "message": [
                {"type": "at", "data": {"qq": str(BOT_QQ)}}
            ]
        })
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        mock_send.assert_called_once()

    def test_receive_message_no_group_id(self, mocker):
        mock_send = mocker.patch("src.bot.main.send_group_msg")

        response = client.post("/onebot", json={
            "post_type": "message",
            "message_type": "group",
            "user_id": 7890,
            "message": [
                {"type": "at", "data": {"qq": str(BOT_QQ)}}
            ]
        })
        assert response.status_code == 200
        mock_send.assert_not_called()


class TestTiming:
    def test_at_reply_response_time(self, mocker):
        mock_send = mocker.patch("src.bot.main.send_group_msg", return_value=True)

        start = time.time()
        response = client.post("/onebot", json={
            "post_type": "message",
            "message_type": "group",
            "group_id": 123456,
            "user_id": 7890,
            "message": [
                {"type": "at", "data": {"qq": str(BOT_QQ)}}
            ]
        })
        elapsed = (time.time() - start) * 1000
        assert response.status_code == 200
        assert elapsed < 500, f"Response time {elapsed:.2f}ms exceeds 500ms"


class TestProcessMessageKeyword:
    def test_process_message_with_keyword_returns_none(self):
        data = {
            "post_type": "message",
            "message_type": "group",
            "group_id": 123456,
            "user_id": 7890,
            "raw_message": "大家好，兄弟们好！"
        }
        reply = process_message(data)
        assert reply is None

    def test_process_message_without_keyword(self):
        data = {
            "post_type": "message",
            "message_type": "group",
            "group_id": 123456,
            "user_id": 7890,
            "raw_message": "Hello world!"
        }
        reply = process_message(data)
        assert reply is None

    def test_process_message_not_group(self):
        data = {
            "post_type": "message",
            "message_type": "private",
            "user_id": 7890,
            "raw_message": "兄弟们好！"
        }
        reply = process_message(data)
        assert reply is None

    def test_process_message_not_message_post_type(self):
        data = {
            "post_type": "notice",
            "message_type": "group",
            "raw_message": "兄弟们好！"
        }
        reply = process_message(data)
        assert reply is None


class TestConfig:
    def test_bot_qq_loaded(self):
        assert "BOT_QQ" in dir(__import__("src.bot.main", fromlist=["BOT_QQ"]))

    def test_at_reply_text_loaded(self):
        assert AT_REPLY_TEXT == "awa"

    def test_max_retries_loaded(self):
        assert MAX_RETRIES == 3
