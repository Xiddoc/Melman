"""
An echo command! Echo, echo, echo...
"""

import json
import re
from enum import IntEnum
from typing import List, Dict

from bs4 import BeautifulSoup
from requests import Session, RequestException
from telegram.ext import ContextTypes

from lib import MelmanModule, MelmanUpdate, MelmanMDHelp

hypixel = MelmanModule("hypixel", help_msg=MelmanMDHelp("""
**`hypixel`**
Gets the daily hypixel reward.

**Usage**
```
hypixel <REWARD_LINK>
```
"""))

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'


class DailyReward:
    _session: Session

    csrf_token: str
    daily_reward_id: str
    rewards: List[Dict]

    _SECURITY_TOKEN_REGEX = re.compile(r'securityToken = "([a-zA-Z0-9_-]*)";')
    _APP_DATA_REGEX = re.compile(r"appData = '(.*)';")

    def __init__(self, session: Session, csrf_token: str, app_data: str) -> None:
        self._session = session
        self.csrf_token = csrf_token
        self._set_app_data_from_json(app_data)

    def _set_app_data_from_json(self, app_data: str) -> None:
        parsed_data = json.loads(app_data)

        self.daily_reward_id = parsed_data['id']
        self.rewards = parsed_data['rewards']

        for i, reward in enumerate(self.rewards):
            reward['id'] = i

    @staticmethod
    def _get_daily_reward_html(session: Session, url: str) -> BeautifulSoup:
        form_html = session.get(url).text

        return BeautifulSoup(form_html, 'html.parser')

    @staticmethod
    def _get_app_data_script(html: BeautifulSoup) -> str:
        scripts = html.find_all('script')

        for script in scripts:
            if script.string and 'appData' in script.string:
                return script.string

        raise ValueError(f"Could not parse Daily Reward page. Could not find 'appData' JSON in HTML:\n\n{html}")

    @classmethod
    def _parse_from_html(cls, session: Session, html: BeautifulSoup) -> "DailyReward":
        script = cls._get_app_data_script(html).replace("\\'", "'")

        security_token = cls._SECURITY_TOKEN_REGEX.search(script)
        app_data = cls._APP_DATA_REGEX.search(script)

        if not security_token:
            raise ValueError("Could not find security token in HTML.")

        if not app_data:
            raise ValueError("Could not find app data in HTML.")

        return DailyReward(session, security_token.group(1), app_data.group(1))

    @staticmethod
    def _create_client_session() -> Session:
        client = Session()
        client.headers.update({
            'User-Agent': USER_AGENT
        })
        return client

    @classmethod
    def from_url(cls, url: str) -> "DailyReward":
        client = cls._create_client_session()
        html = cls._get_daily_reward_html(client, url)
        return cls._parse_from_html(client, html)

    def submit(self, selection_id: int) -> None:
        self._session.post(
            url='https://rewards.hypixel.net/claim-reward/claim',
            params={
                'option': selection_id,
                'id': self.daily_reward_id,
                'activeAd': '1',
                '_csrf': self.csrf_token,
                'watchedFallback': 'false',
            }
        )


class DailyRewardPicker:
    # noinspection PyUnusedName
    class Rarity(IntEnum):
        COMMON = 1
        RARE = 2
        EPIC = 3
        LEGENDARY = 4

    @classmethod
    def _get_rarity_from_reward(cls, reward: Dict) -> Rarity:
        rarity: str = reward['rarity']

        return cls.Rarity[rarity]

    @classmethod
    def _get_indicies_for_rarities(cls, rewards: List[Dict]) -> Dict[Rarity, int]:
        index_per_rarity: Dict[cls.Rarity, int] = {}

        for i, reward in enumerate(rewards):
            index_per_rarity[cls._get_rarity_from_reward(reward)] = i

        return index_per_rarity

    @staticmethod
    def _get_best_reward_by_rarity(rarities: Dict[Rarity, int]) -> int:
        max_rarity = max(rarities)

        return rarities[max_rarity]

    @classmethod
    def get_best_reward_index(cls, daily_form: DailyReward) -> int:
        rarity_map = cls._get_indicies_for_rarities(daily_form.rewards)

        return cls._get_best_reward_by_rarity(rarity_map)


# noinspection PyUnusedFunction
@hypixel.route(re.compile(r"https://(rewards\.)?hypixel\.net/claim-reward/.*"))
async def index(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Claiming reward...")

    hypixel_url = update.get_path()
    try:
        reward = DailyReward.from_url(hypixel_url)

        best_index = DailyRewardPicker.get_best_reward_index(reward)
        reward.submit(best_index)

        # print(f"\nYou got '{reward.rewards[best_index]['reward']}' "
        #       f"[{reward.rewards[best_index]['rarity']}] !")
    except RequestException:
        await update.message.reply_text("Invalid reward link.")
    except ValueError:
        await update.message.reply_text("Expired or used reward link.")
