import random

FOOD = {
    "苹果": (10, 2, 5),
    "鱼": (20, 5, 10),
    "蛋糕": (15, 10, 15),
    "牛奶": (8, 3, 3),
    "牛排": (30, 8, 25),
    "沙拉": (12, 4, 8),
}
GAME = {
    "捉迷藏": (15, -10),
    "接球": (10, -8),
    "跑步": (8, -15),
    "拼图": (12, -5),
    "唱歌": (20, -3),
}
PETS = {
    "猫": ("🐱", "独立"),
    "狗": ("🐶", "忠诚"),
    "兔子": ("🐰", "温柔"),
    "龙": ("🐲", "神秘"),
    "狐狸": ("🦊", "聪明"),
    "熊猫": ("🐼", "可爱"),
}
STAGES = [(0, "蛋"), (10, "幼年"), (50, "少年"), (150, "青年"), (300, "成年")]

CAT = {
    "idle": "  /\\_/\\\n ( o.o )\n  > ^ <",
    "happy": "  /\\_/\\\n ( ^.^ ) ♪\n  > ~ <",
    "sleep": "  /\\_/\\\n ( -.- ) z Z\n  > ~ <",
    "sad": "  /\\_/\\\n ( T.T )\n  > ~ <",
}
DOG = {
    "idle": "  / \\__\n (    @\\___\n /         O\n/_____/  U",
    "happy": "  / \\__\n (    @\\___  ♪\n /         O\n/_____/  U ~",
    "sleep": "  / \\__\n (    -\\___  z Z\n /         O\n/_____/  U",
    "sad": "  / \\__\n (    T\\___\n /         O\n/_____/  U",
}
BUN = {
    "idle": " (\\ /)\n ( . .)\n c(\")(\")",
    "happy": " (\\ /)\n ( ^.^) ♪\n c(\")(\")",
    "sleep": " (\\ /)\n ( -.-) z Z\n c(\")(\")",
    "sad": " (\\ /)\n ( T.T)\n c(\")(\")",
}
ARTS = {"猫": CAT, "狗": DOG, "兔子": BUN, "龙": CAT, "狐狸": CAT, "熊猫": CAT}

TIPS = [
    "加油！💪",
    "bug只是还没变成feature~",
    "休息一下吧！👀",
    "记得喝水！🥤",
    "每一行代码都是进步！📈",
    "相信自己！🌟",
    "代码能跑就是胜利！🏆",
    "元气满满！🌈",
    "困了就休息！😴",
    "记得保存！📦",
]


def clamp(v):
    return max(0, min(100, v))


class VPet:
    def __init__(self, name, pt="猫"):
        self.name = name
        self.pt = pt
        self.emoji = PETS.get(pt, PETS["猫"])[0]
        self.hunger = 50
        self.happy = 50
        self.energy = 80
        self.hp = 100
        self.exp = 0
        self.lv = 1
        self.coins = 50
        self.sleeping = False
        self.count = 0

    def stage(self):
        r = "蛋"
        for t, n in STAGES:
            if self.exp >= t:
                r = n
        return r

    def mood(self):
        if self.energy < 20:
            return "困倦😴"
        if self.hunger < 20:
            return "饥饿😫"
        if self.happy > 80:
            return "兴奋🤩"
        if self.happy > 50:
            return "开心😊"
        if self.happy < 30:
            return "难过😢"
        return "普通😐"

    def bar(self, v):
        f = int(v / 5)
        return "█" * f + "░" * (20 - f)

    def status(self):
        print("")
        print("=" * 40)
        print("  " + self.emoji + " " + self.name + " | " + self.pt)
        print("  阶段:" + self.stage() + " 等级:" + str(self.lv) + " 经验:" + str(self.exp))
        print("  心情:" + self.mood() + " 金币:" + str(self.coins))
        print("─" * 40)
        for n, v in [("饱腹", self.hunger), ("快乐", self.happy), ("体力", self.energy), ("健康", self.hp)]:
            print("  " + n + ":[" + self.bar(v) + "]" + str(v) + "%")
        print("  互动:" + str(self.count))
        print("=" * 40)

    def feed(self, food):
        if food not in FOOD:
            print("没有！可选:" + ",".join(FOOD.keys()))
            return
        h, hp, p = FOOD[food]
        if self.coins < p:
            print("金币不够！要" + str(p) + "有" + str(self.coins))
            return
        if self.sleeping:
            print("在睡觉！")
            return
        self.coins -= p
        self.hunger = clamp(self.hunger + h)
        self.happy = clamp(self.happy + hp)
        self.exp += 5
        self.lv = 1 + self.exp // 30
        self.count += 1
        print(self.emoji + self.name + "吃了" + food + "！饱腹+" + str(h) + " 快乐+" + str(hp) + " -" + str(p) + "币")

    def play(self, g):
        if g not in GAME:
            print("没有！可选:" + ",".join(GAME.keys()))
            return
        if self.sleeping:
            print("在睡觉！")
            return
        if self.energy < 10:
            print("太累了！")
            return
        hp, en = GAME[g]
        r = random.randint(3, 12)
        self.happy = clamp(self.happy + hp)
        self.energy = clamp(self.energy + en)
        self.coins += r
        self.exp += 8
        self.lv = 1 + self.exp // 30
        self.count += 1
        print(self.emoji + self.name + "玩了" + g + "！快乐+" + str(hp) + " 体力" + str(en) + " +" + str(r) + "币")

    def pet_it(self):
        self.happy = clamp(self.happy + 8)
        self.exp += 3
        self.lv = 1 + self.exp // 30
        self.count += 1
        r = random.choice(["蹭了蹭你", "转圈圈", "眨眨眼", "跳到怀里"])
        print(self.emoji + self.name + r + "！快乐+8")

    def toggle_sleep(self):
        if self.sleeping:
            self.sleeping = False
            print(self.emoji + self.name + "醒了！")
        else:
            self.sleeping = True
            self.energy = clamp(self.energy + 30)
            self.hp = clamp(self.hp + 10)
            print(self.emoji + self.name + "睡着了💤 体力+30")

    def art(self, st="idle"):
        a = ARTS.get(self.pt, CAT)
        print("\n" + a.get(st, CAT["idle"]) + "\n")


def virtual_pet():
    print("\n🎮 虚拟宠物")
    for k in PETS:
        e, t = PETS[k]
        print("  " + e + k + "-" + t)
    pt = input("选类型:").strip()
    if pt not in PETS:
        pt = "猫"
    name = input("起名字:").strip()
    if not name:
        name = "小宝"
    p = VPet(name, pt)
    print("\n🎉" + p.emoji + name + "诞生了！")
    while True:
        p.status()
        p.art()
        print("[1]喂食[2]玩[3]摸[4]睡[5]鼓励[0]返回")
        c = input("> ").strip()
        if c == "0":
            break
        elif c == "1":
            items = []
            for k in FOOD:
                items.append(k + "¥" + str(FOOD[k][2]))
            print("食物:" + ",".join(items))
            p.feed(input("选:").strip())
        elif c == "2":
            print("游戏:" + ",".join(GAME.keys()))
            p.play(input("选:").strip())
        elif c == "3":
            p.pet_it()
        elif c == "4":
            p.toggle_sleep()
        elif c == "5":
            p.art("happy")
            print("💬" + name + ":" + random.choice(TIPS))


def cli_companion():
    print("\n🖥️ CLI伙伴")
    pt = input("选(猫/狗/兔子):").strip()
    if pt not in ARTS:
        pt = "猫"
    name = input("起名字:").strip()
    if not name:
        name = "伙伴"
    art = ARTS.get(pt, CAT)
    while True:
        print("\n伙伴:" + name)
        print("[1]看[2]鼓励[3]聊[0]返回")
        c = input("> ").strip()
        if c == "0":
            break
        elif c == "1":
            print("\n" + art["idle"])
        elif c == "2":
            print("\n" + art["happy"])
            print("💬" + name + ":" + random.choice(TIPS))
        elif c == "3":
            w = input("说:").strip()
            if any(x in w for x in ["error", "bug", "错", "难"]):
                print("\n" + art["sad"])
                print("💬" + name + ":别灰心！")
            elif any(x in w for x in ["done", "完成", "棒", "好"]):
                print("\n" + art["happy"])
                print("💬" + name + ":太棒了！🎉")
            elif any(x in w for x in ["累", "困"]):
                print("\n" + art["sleep"])
                print("💬" + name + ":休息吧💤")
            else:
                print("\n" + art["idle"])
                print("💬" + name + ":我陪着你！")


pets_db = {}


def pet_manager():
    emo = {"猫": "🐱", "狗": "🐶", "兔子": "🐰", "鸟": "🐦", "鱼": "🐟", "仓鼠": "🐹", "乌龟": "🐢"}
    while True:
        print("\n📋宠物管理")
        print("[1]列表[2]添加[3]详情[4]疫苗[5]备注[0]返回")
        c = input("> ").strip()
        if c == "0":
            break
        elif c == "1":
            if not pets_db:
                print("还没有宠物！")
                continue
            for n in pets_db:
                p = pets_db[n]
                e = emo.get(p["s"], "🐾")
                print("  " + e + n + "|" + p["s"] + "|" + str(p["a"]) + "岁" + str(p["w"]) + "kg")
        elif c == "2":
            n = input("名字:").strip()
            s = input("种类:").strip()
            b = input("品种:").strip()
            try:
                a = float(input("年龄:").strip() or "0")
            except Exception:
                a = 0
            try:
                w = float(input("体重kg:").strip() or "0")
            except Exception:
                w = 0
            pets_db[n] = {"s": s, "b": b, "a": a, "w": w, "v": [], "n": []}
            print("🐾已添加" + n + "!")
        elif c == "3":
            n = input("名字:").strip()
            if n not in pets_db:
                print("找不到")
                continue
            p = pets_db[n]
            e = emo.get(p["s"], "🐾")
            print("\n" + e + n)
            print("种类:" + p["s"] + " 品种:" + p["b"])
            print("年龄:" + str(p["a"]) + "岁 体重:" + str(p["w"]) + "kg")
            if p["v"]:
                print("💉疫苗:")
                for v in p["v"]:
                    print("  -" + v)
            if p["n"]:
                print("📝备注:")
                for x in p["n"][-5:]:
                    print("  -" + x)
        elif c == "4":
            n = input("名字:").strip()
            if n not in pets_db:
                print("找不到")
                continue
            v = input("疫苗:").strip()
            d = input("日期:").strip()
            pets_db[n]["v"].append(v + "(" + d + ")")
            print("💉已记录" + v)
        elif c == "5":
            n = input("名字:").strip()
            if n not in pets_db:
                print("找不到")
                continue
            x = input("备注:").strip()
            pets_db[n]["n"].append(x)
            print("📝已添加")


def main():
    while True:
        print("")
        print("╔════════════════════════╗")
        print("║  🐾 Buddy 宠物系统 🐾 ║")
        print("║ 1.🎮虚拟宠物          ║")
        print("║ 2.🖥️ CLI伙伴           ║")
        print("║ 3.📋宠物管理          ║")
        print("║ 0.🚪退出              ║")
        print("╚════════════════════════╝")
        c = input("选(1/2/3/0):").strip()
        if c == "0":
            print("👋再见！")
            break
        elif c == "1":
            virtual_pet()
        elif c == "2":
            cli_companion()
        elif c == "3":
            pet_manager()


if __name__ == "__main__":
    main()
