"""CLI 宠物伙伴 - 终端里陪你编程的小伙伴"""

import random
import time

# ASCII 艺术宠物
ASCII_PETS = {
    "猫": {
        "idle": r"""
  /\_/\
 ( o.o )
  > ^ <
 /|   |\
(_|   |_)
""",
        "happy": r"""
  /\_/\
 ( ^.^ )
  > ~ <
 /|   |\  ♪
(_|   |_)
""",
        "sleep": r"""
  /\_/\
 ( -.- ) z Z
  > ~ <
 /|   |\
(_|   |_)
""",
        "eat": r"""
  /\_/\
 ( o.o )
  > ~ < 🍖
 /|   |\
(_|   |_)
""",
        "sad": r"""
  /\_/\
 ( T.T )
  > ~ <
 /|   |\
(_|   |_)
""",
    },
    "狗": {
        "idle": r"""
  / \__
 (    @\___
 /         O
/   (_____/
/_____/  U
""",
        "happy": r"""
  / \__
 (    @\___  ♪
 /         O
/   (_____/
/_____/  U  ~
""",
        "sleep": r"""
  / \__
 (    -\___  z Z
 /         O
/   (_____/
/_____/  U
""",
        "eat": r"""
  / \__
 (    @\___
 /         O 🍖
/   (_____/
/_____/  U
""",
        "sad": r"""
  / \__
 (    T\___
 /         O
/   (_____/
/_____/  U
""",
    },
    "兔子": {
        "idle": r"""
 (\ /)
 ( . .)
 c(")(")
""",
        "happy": r"""
 (\ /)
 ( ^.^) ♪
 c(")(")
""",
        "sleep": r"""
 (\ /)
 ( -.-) z Z
 c(")(")
""",
        "eat": r"""
 (\ /)
 ( o.o) 🥕
 c(")(")
""",
        "sad": r"""
 (\ /)
 ( T.T)
 c(")(")
""",
    },
    "龙": {
        "idle": r"""
       ____ /\
      { -- }  \
       \  /    >  )
        \/   _/  /
       /  \_/  \/
      / |      |
     /  |      |
    (____|____|)
""",
        "happy": r"""
       ____ /\  🔥
      { ^^ }  \
       \  /    >  )
        \/   _/  /
       /  \_/  \/
      / |      |
     /  |      |  ♪
    (____|____|)
""",
        "sleep": r"""
       ____ /\
      { -- }  \  z Z
       \  /    >  )
        \/   _/  /
       /  \_/  \/
      / |      |
     /  |      |
    (____|____|)
""",
        "eat": r"""
       ____ /\
      { oo }  \
       \  /    >  ) 🍖
        \/   _/  /
       /  \_/  \/
      / |      |
     /  |      |
    (____|____|)
""",
        "sad": r"""
       ____ /\
      { TT }  \
       \  /    >  )
        \/   _/  / 💧
       /  \_/  \/
      / |      |
     /  |      |
    (____|____|)
""",
    },
    "狐狸": {
        "idle": r"""
  /\   /\
 /  \ /  \
(  o   o  )
 \   Y   /
  \  ^  /
   |/ \|
""",
        "happy": r"""
  /\   /\
 /  \ /  \  ♪
(  ^   ^  )
 \   Y   /
  \  ~  /
   |/ \|
""",
        "sleep": r"""
  /\   /\
 /  \ /  \
(  -   -  ) z Z
 \   Y   /
  \  ~  /
   |/ \|
""",
        "eat": r"""
  /\   /\
 /  \ /  \
(  o   o  ) 🍇
 \   Y   /
  \  ~  /
   |/ \|
""",
        "sad": r"""
  /\   /\
 /  \ /  \
(  T   T  )
 \   Y   /
  \  n  /
   |/ \|
""",
    },
    "熊猫": {
        "idle": r"""
  ┌───────┐
  │ ●   ● │
  │  ▼    │
  │  ───  │
  └───────┘
   /|   |\
  (_|   |_)
""",
        "happy": r"""
  ┌───────┐
  │ ◕   ◕ │  ♪
  │  ▼    │
  │  ◡◡◡  │
  └───────┘
   /|   |\
  (_|   |_)
""",
        "sleep": r"""
  ┌───────┐
  │ —   — │  z Z
  │  ▼    │
  │  ───  │
  └───────┘
   /|   |\
  (_|   |_)
""",
        "eat": r"""
  ┌───────┐
  │ ●   ● │
  │  ▼    │  🎋
  │  ◡◡◡  │
  └───────┘
   /|   |\
  (_|   |_)
""",
        "sad": r"""
  ┌───────┐
  │ ●   ● │
  │  ▼    │  💧
  │  ╥╥╥  │
  └───────┘
   /|   |\
  (_|   |_)
""",
    },
}

# 编程鼓励语
ENCOURAGEMENTS = [
    "加油！你写的代码很棒！💪",
    "bug 只是还没变成 feature 而已~",
    "休息一下吧，眼睛很重要！👀",
    "你今天的代码比昨天更优雅了！✨",
    "记得喝水哦！🥤",
    "每一行代码都是进步！📈",
    "相信自己，你能解决这个问题的！🌟",
    "好的代码就像好的笑话，不需要解释 😄",
    "Stack Overflow 是每个程序员的好朋友~",
    "代码能跑就是胜利！🏆",
    "不要忘记 git commit 哦！📦",
    "你的键盘声真好听！⌨️",
    "困了就休息，效率更重要！😴",
    "写注释是对未来的自己负责！📝",
    "今天也是元气满满的一天！🌈",
]

# 随机事件
RANDOM_EVENTS = [
    "你的宠物发现了一颗闪亮的星星 ⭐",
    "你的宠物在键盘上打了一段神秘代码",
    "你的宠物抓到了一只 bug 🐛",
    "你的宠物帮你整理了桌面",
    "你的宠物学会了一个新表情",
    "你的宠物在屏幕角落发现了一块饼干 🍪",
    "你的宠物和屏幕上的光标玩了起来",
    "你的宠物偷偷看了你的代码，表示赞赏",
]


class CLICompanion:
    """CLI 宠物伙伴"""

    def __init__(self, pet_type: str = "猫", name: str = "小伙伴"):
        self.pet_type = pet_type if pet_type in ASCII_PETS else "猫"
        self.name = name
        self.state = "idle"
        self.last_event_time = time.time()
        self.event_interval = 300  # 5 minutes between random events

    def show(self, state: str = None) -> str:
        if state:
            self.state = state
        art = ASCII_PETS[self.pet_type].get(self.state, ASCII_PETS[self.pet_type]["idle"])
        return f"--- {self.name} ---{art}"

    def encourage(self) -> str:
        msg = random.choice(ENCOURAGEMENTS)
        return f"{self.show('happy')}\n💬 {self.name}: {msg}"

    def random_event(self) -> str | None:
        now = time.time()
        if now - self.last_event_time >= self.event_interval:
            self.last_event_time = now
            event = random.choice(RANDOM_EVENTS)
            return f"\n🎲 [随机事件] {event}\n"
        return None

    def react(self, keyword: str) -> str:
        keyword = keyword.lower()
        if any(w in keyword for w in ["error", "bug", "fail", "错误"]):
            return f"{self.show('sad')}\n💬 {self.name}: 别灰心，我们一起找到问题！"
        elif any(w in keyword for w in ["success", "pass", "done", "完成", "成功"]):
            return f"{self.show('happy')}\n💬 {self.name}: 太棒了！我就知道你可以的！🎉"
        elif any(w in keyword for w in ["tired", "累", "困"]):
            return f"{self.show('sleep')}\n💬 {self.name}: 休息一下吧，我在这里等你 💤"
        elif any(w in keyword for w in ["hungry", "饿", "吃"]):
            return f"{self.show('eat')}\n💬 {self.name}: 我也饿了，一起去吃东西吧！"
        else:
            return f"{self.show('idle')}\n💬 {self.name}: 我在这里陪着你！"

    def available_pets(self) -> str:
        result = "🐾 可选的伙伴类型:\n"
        for pet_type in ASCII_PETS:
            result += f"\n  [{pet_type}]"
            result += ASCII_PETS[pet_type]["idle"]
        return result
