"""虚拟宠物模块 - 电子宠物风格的虚拟宠物"""

import json
import time
import random
from pathlib import Path
from enum import Enum

DATA_DIR = Path(__file__).parent.parent / "data"


class Mood(Enum):
    HAPPY = "开心 😊"
    NORMAL = "普通 😐"
    SAD = "难过 😢"
    HUNGRY = "饥饿 😫"
    SLEEPY = "困倦 😴"
    EXCITED = "兴奋 🤩"


class Stage(Enum):
    EGG = "蛋"
    BABY = "幼年"
    CHILD = "少年"
    TEEN = "青年"
    ADULT = "成年"


STAGE_THRESHOLDS = {
    Stage.EGG: 0,
    Stage.BABY: 10,
    Stage.CHILD: 50,
    Stage.TEEN: 150,
    Stage.ADULT: 300,
}

FOOD_MENU = {
    "苹果": {"hunger": 10, "happiness": 2, "price": 5},
    "鱼": {"hunger": 20, "happiness": 5, "price": 10},
    "蛋糕": {"hunger": 15, "happiness": 10, "price": 15},
    "牛奶": {"hunger": 8, "happiness": 3, "price": 3},
    "牛排": {"hunger": 30, "happiness": 8, "price": 25},
    "沙拉": {"hunger": 12, "happiness": 4, "price": 8},
}

GAMES = {
    "捉迷藏": {"happiness": 15, "energy": -10},
    "接球": {"happiness": 10, "energy": -8},
    "跑步": {"happiness": 8, "energy": -15},
    "拼图": {"happiness": 12, "energy": -5},
    "唱歌": {"happiness": 20, "energy": -3},
}

PET_TYPES = {
    "猫": {"emoji": "🐱", "trait": "独立"},
    "狗": {"emoji": "🐶", "trait": "忠诚"},
    "兔子": {"emoji": "🐰", "trait": "温柔"},
    "龙": {"emoji": "🐲", "trait": "神秘"},
    "狐狸": {"emoji": "🦊", "trait": "聪明"},
    "熊猫": {"emoji": "🐼", "trait": "可爱"},
}


class VirtualPet:
    """虚拟宠物类"""

    def __init__(self, name: str, pet_type: str = "猫"):
        self.name = name
        self.pet_type = pet_type
        self.emoji = PET_TYPES.get(pet_type, PET_TYPES["猫"])["emoji"]
        self.trait = PET_TYPES.get(pet_type, PET_TYPES["猫"])["trait"]

        self.hunger = 50  # 0-100, 0=饿死
        self.happiness = 50  # 0-100
        self.energy = 80  # 0-100
        self.health = 100  # 0-100
        self.exp = 0
        self.level = 1
        self.coins = 50
        self.stage = Stage.EGG

        self.created_at = time.time()
        self.last_interact = time.time()
        self.interaction_count = 0
        self.is_sleeping = False

    def get_mood(self) -> Mood:
        if self.energy < 20:
            return Mood.SLEEPY
        if self.hunger < 20:
            return Mood.HUNGRY
        if self.happiness > 80:
            return Mood.EXCITED
        if self.happiness > 50:
            return Mood.HAPPY
        if self.happiness < 30:
            return Mood.SAD
        return Mood.NORMAL

    def _update_stage(self):
        for stage in reversed(list(Stage)):
            if self.exp >= STAGE_THRESHOLDS[stage]:
                if self.stage != stage:
                    self.stage = stage
                    return True
                return False
        return False

    def _clamp(self, value: int, low: int = 0, high: int = 100) -> int:
        return max(low, min(high, value))

    def _gain_exp(self, amount: int):
        self.exp += amount
        old_level = self.level
        self.level = 1 + self.exp // 30
        evolved = self._update_stage()
        return old_level != self.level, evolved

    def _time_decay(self):
        elapsed = time.time() - self.last_interact
        hours = elapsed / 3600
        if hours > 0.5:
            decay = int(hours * 5)
            self.hunger = self._clamp(self.hunger - decay)
            self.happiness = self._clamp(self.happiness - decay // 2)
            self.energy = self._clamp(self.energy + decay)  # rest recovers energy

    def feed(self, food_name: str) -> str:
        if food_name not in FOOD_MENU:
            return f"没有 {food_name} 这种食物！可选: {', '.join(FOOD_MENU.keys())}"

        food = FOOD_MENU[food_name]
        if self.coins < food["price"]:
            return f"金币不够！需要 {food['price']}，当前 {self.coins} 金币"

        if self.is_sleeping:
            return f"{self.name} 正在睡觉，不要打扰它！"

        self._time_decay()
        self.coins -= food["price"]
        self.hunger = self._clamp(self.hunger + food["hunger"])
        self.happiness = self._clamp(self.happiness + food["happiness"])
        leveled, evolved = self._gain_exp(5)
        self.interaction_count += 1
        self.last_interact = time.time()

        msg = f"{self.emoji} {self.name} 吃了 {food_name}！\n"
        msg += f"  饱腹度 +{food['hunger']} | 快乐度 +{food['happiness']} | 花费 {food['price']} 金币\n"
        if leveled:
            msg += f"  🎉 升级了！当前等级: {self.level}\n"
        if evolved:
            msg += f"  ✨ 进化了！当前阶段: {self.stage.value}\n"
        return msg

    def play(self, game_name: str) -> str:
        if game_name not in GAMES:
            return f"没有 {game_name} 这个游戏！可选: {', '.join(GAMES.keys())}"

        if self.is_sleeping:
            return f"{self.name} 正在睡觉，不要打扰它！"

        if self.energy < 10:
            return f"{self.name} 太累了，需要休息！"

        self._time_decay()
        game = GAMES[game_name]
        self.happiness = self._clamp(self.happiness + game["happiness"])
        self.energy = self._clamp(self.energy + game["energy"])
        reward = random.randint(3, 12)
        self.coins += reward
        leveled, evolved = self._gain_exp(8)
        self.interaction_count += 1
        self.last_interact = time.time()

        msg = f"{self.emoji} {self.name} 玩了 {game_name}！\n"
        msg += f"  快乐度 +{game['happiness']} | 体力 {game['energy']} | 获得 {reward} 金币\n"
        if leveled:
            msg += f"  🎉 升级了！当前等级: {self.level}\n"
        if evolved:
            msg += f"  ✨ 进化了！当前阶段: {self.stage.value}\n"
        return msg

    def sleep(self) -> str:
        if self.is_sleeping:
            return f"{self.name} 已经在睡觉了"
        self.is_sleeping = True
        self.energy = self._clamp(self.energy + 30)
        self.health = self._clamp(self.health + 10)
        return f"{self.emoji} {self.name} 睡着了... 💤\n  体力 +30 | 健康 +10"

    def wake(self) -> str:
        if not self.is_sleeping:
            return f"{self.name} 没有在睡觉"
        self.is_sleeping = False
        return f"{self.emoji} {self.name} 醒了！精神满满！"

    def pet(self) -> str:
        if self.is_sleeping:
            self.happiness = self._clamp(self.happiness + 3)
            return f"{self.emoji} 你轻轻摸了摸 {self.name}，它在睡梦中微笑了"

        self._time_decay()
        self.happiness = self._clamp(self.happiness + 8)
        self.last_interact = time.time()
        self.interaction_count += 1
        self._gain_exp(3)

        responses = [
            f"{self.name} 蹭了蹭你的手",
            f"{self.name} 发出了满足的声音",
            f"{self.name} 开心地转圈圈",
            f"{self.name} 对你眨眨眼睛",
            f"{self.name} 跳到你怀里",
        ]
        return f"{self.emoji} {random.choice(responses)}！快乐度 +8"

    def status(self) -> str:
        self._time_decay()
        mood = self.get_mood()
        bars = {
            "饱腹度": self.hunger,
            "快乐度": self.happiness,
            "体力值": self.energy,
            "健康值": self.health,
        }
        status = f"\n{'='*40}\n"
        status += f"  {self.emoji} {self.name} | {self.pet_type} | 性格: {self.trait}\n"
        status += f"  阶段: {self.stage.value} | 等级: {self.level} | 经验: {self.exp}\n"
        status += f"  心情: {mood.value} | 金币: {self.coins}\n"
        if self.is_sleeping:
            status += f"  状态: 💤 睡觉中\n"
        status += f"{'─'*40}\n"
        for name, val in bars.items():
            filled = int(val / 5)
            bar = "█" * filled + "░" * (20 - filled)
            status += f"  {name}: [{bar}] {val}%\n"
        status += f"  互动次数: {self.interaction_count}\n"
        status += f"{'='*40}\n"
        return status

    def save(self) -> str:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "name": self.name,
            "pet_type": self.pet_type,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "health": self.health,
            "exp": self.exp,
            "level": self.level,
            "coins": self.coins,
            "stage": self.stage.name,
            "created_at": self.created_at,
            "last_interact": self.last_interact,
            "interaction_count": self.interaction_count,
            "is_sleeping": self.is_sleeping,
        }
        filepath = DATA_DIR / f"vpet_{self.name}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return f"已保存 {self.name} 的数据到 {filepath}"

    @classmethod
    def load(cls, name: str) -> "VirtualPet":
        filepath = DATA_DIR / f"vpet_{name}.json"
        if not filepath.exists():
            raise FileNotFoundError(f"找不到宠物 {name} 的存档")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        pet = cls(data["name"], data["pet_type"])
        pet.hunger = data["hunger"]
        pet.happiness = data["happiness"]
        pet.energy = data["energy"]
        pet.health = data["health"]
        pet.exp = data["exp"]
        pet.level = data["level"]
        pet.coins = data["coins"]
        pet.stage = Stage[data["stage"]]
        pet.created_at = data["created_at"]
        pet.last_interact = data["last_interact"]
        pet.interaction_count = data["interaction_count"]
        pet.is_sleeping = data["is_sleeping"]
        return pet

    @classmethod
    def list_saved(cls) -> list[str]:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        return [f.stem.replace("vpet_", "") for f in DATA_DIR.glob("vpet_*.json")]
