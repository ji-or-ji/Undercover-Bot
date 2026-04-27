import re
import asyncio
import logging
from typing import List, Dict, Optional, Callable, Awaitable, Pattern, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger("NapCatLoginManager")


class MatchType(Enum):
    EXACT = "exact"
    REGEX = "regex"


class ReplyStrategy(Enum):
    SEPARATE = "separate"
    MERGE = "merge"


@dataclass
class RepeaterConfig:
    keywords: List[str] = field(default_factory=lambda: ["炸群", "举报", "兄弟们"])
    match_type: str = "exact"
    reply_template: str = "收到关键词【{keyword}】，已记录"
    reply_strategy: str = "separate"
    retry_max_attempts: int = 3
    retry_base_delay: float = 1.0


@dataclass
class KeywordMatch:
    keyword: str
    match_type: MatchType
    matched_value: str


class Repeater:
    def __init__(
        self,
        config: Optional[RepeaterConfig] = None,
        send_func: Optional[Callable[[int, str], Awaitable[bool]]] = None
    ):
        self.config = config or RepeaterConfig()
        self._send_func = send_func
        self._compiled_patterns: Dict[str, Optional[Pattern]] = {}
        self._init_patterns()

    def _init_patterns(self):
        for kw in self.config.keywords:
            if self.config.match_type == MatchType.REGEX.value:
                try:
                    self._compiled_patterns[kw] = re.compile(kw)
                except re.error as e:
                    logging.getLogger("NapCatLoginManager").error(f"Invalid regex pattern '{kw}': {e}")
                    self._compiled_patterns[kw] = None
            else:
                self._compiled_patterns[kw] = None

    def set_send_func(self, send_func: Callable[[int, str], Awaitable[bool]]):
        self._send_func = send_func

    def match_keyword(self, text: Any) -> List[KeywordMatch]:
        matches = []
        if not text:
            return matches

        if not isinstance(text, str):
            try:
                text = str(text)
            except Exception:
                return matches

        for kw in self.config.keywords:
            pattern = self._compiled_patterns.get(kw)
            if pattern is None:
                if self.config.match_type == MatchType.REGEX.value:
                    try:
                        pattern = re.compile(kw)
                        self._compiled_patterns[kw] = pattern
                    except re.error:
                        continue

            if pattern is not None:
                try:
                    if pattern.search(text):
                        matches.append(KeywordMatch(
                            keyword=kw,
                            match_type=MatchType.REGEX,
                            matched_value=kw
                        ))
                except Exception as e:
                    logging.getLogger("NapCatLoginManager").error(f"Regex match error for '{kw}': {e}")
            else:
                if kw in text:
                    matches.append(KeywordMatch(
                        keyword=kw,
                        match_type=MatchType.EXACT,
                        matched_value=kw
                    ))

        return matches

    def render_reply(self, keyword: str) -> str:
        return self.config.reply_template.format(keyword=keyword)

    def get_replies(self, matches: List[KeywordMatch]) -> List[str]:
        if self.config.reply_strategy == ReplyStrategy.MERGE.value and matches:
            unique_keywords = list(dict.fromkeys(m.keyword for m in matches))
            merged_keyword = "、".join(unique_keywords)
            return [self.render_reply(merged_keyword)]
        return [self.render_reply(m.keyword) for m in matches]

    async def send_with_retry(
        self,
        group_id: int,
        message: str,
        max_attempts: Optional[int] = None,
        base_delay: Optional[float] = None
    ) -> bool:
        if self._send_func is None:
            logging.getLogger("NapCatLoginManager").error("send_func not configured")
            return False

        max_attempts = max_attempts or self.config.retry_max_attempts
        base_delay = base_delay or self.config.retry_base_delay
        last_error = None

        for attempt in range(max_attempts):
            try:
                success = await self._send_func(group_id, message)
                if success:
                    if attempt > 0:
                        logging.getLogger("NapCatLoginManager").info(f"Retry succeeded: group_id={group_id}, attempt={attempt + 1}")
                    return True
                logging.getLogger("NapCatLoginManager").warning(f"Send failed (attempt {attempt + 1}/{max_attempts}): group_id={group_id}")
            except asyncio.TimeoutError as e:
                last_error = e
                logging.getLogger("NapCatLoginManager").warning(f"Timeout (attempt {attempt + 1}/{max_attempts}): group_id={group_id}, error={e}")
            except Exception as e:
                last_error = e
                logging.getLogger("NapCatLoginManager").error(f"Send exception (attempt {attempt + 1}/{max_attempts}): group_id={group_id}, error={e}")

            if attempt < max_attempts - 1:
                delay = base_delay * (2 ** attempt)
                logging.getLogger("NapCatLoginManager").info(f"Retrying in {delay}s: group_id={group_id}")
                await asyncio.sleep(delay)

                logging.getLogger("NapCatLoginManager").error(f"All {max_attempts} attempts failed: group_id={group_id}, last_error={last_error}")
        return False

    async def handle_message(self, data: Dict) -> Optional[bool]:
        if data.get("post_type") != "message":
            return None
        if data.get("message_type") != "group":
            return None

        group_id = data.get("group_id")
        if not isinstance(group_id, int):
            return None
            
        user_id = data.get("user_id")
        raw_message = data.get("raw_message", "")

        if not isinstance(raw_message, str):
            raw_message = str(raw_message)

        logging.getLogger("NapCatLoginManager").info(f"Received group message: group_id={group_id}, user_id={user_id}, message={raw_message}")

        matches = self.match_keyword(raw_message)

        if not matches:
            return None

        logging.getLogger("NapCatLoginManager").info(f"Keyword matched: group_id={group_id}, user_id={user_id}, matches={[m.keyword for m in matches]}")

        replies = self.get_replies(matches)

        if self.config.reply_strategy == ReplyStrategy.SEPARATE.value:
            for reply in replies:
                await self.send_with_retry(group_id, reply)
        else:
            for reply in replies:
                await self.send_with_retry(group_id, reply)

        return True


_repeater_instance: Optional[Repeater] = None


def get_repeater(
    config: Optional[RepeaterConfig] = None,
    send_func: Optional[Callable[[int, str], Awaitable[bool]]] = None
) -> Repeater:
    global _repeater_instance
    if _repeater_instance is None or config is not None or send_func is not None:
        _repeater_instance = Repeater(config=config, send_func=send_func)
    return _repeater_instance


def create_repeater_config(config_dict: Dict) -> RepeaterConfig:
    return RepeaterConfig(
        keywords=config_dict.get("repeater", {}).get("keywords", ["炸群", "举报", "兄弟们"]),
        match_type=config_dict.get("repeater", {}).get("match_type", "exact"),
        reply_template=config_dict.get("repeater", {}).get("reply_template", "收到关键词【{keyword}】，已记录"),
        reply_strategy=config_dict.get("repeater", {}).get("reply_strategy", "separate"),
        retry_max_attempts=config_dict.get("repeater", {}).get("retry_max_attempts", 3),
        retry_base_delay=config_dict.get("repeater", {}).get("retry_base_delay", 1.0)
    )
