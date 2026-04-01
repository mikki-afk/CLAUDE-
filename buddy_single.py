#!/usr/bin/env python3
"""Buddy - 宠物系统 (单文件版)"""
import json, time, random, sys, os

# ═══════════ 虚拟宠物 ═══════════
FOOD = {"苹果":(10,2,5),"鱼":(20,5,10),"蛋糕":(15,10,15),"牛奶":(8,3,3),"牛排":(30,8,25),"沙拉":(12,4,8)}
GAME = {"捉迷藏":(15,-10),"接球":(10,-8),"跑步":(8,-15),"拼图":(12,-5),"唱歌":(20,-3)}
PETS = {"猫":("🐱","独立"),"狗":("🐶","忠诚"),"兔子":("🐰","温柔"),"龙":("🐲","神秘"),"狐狸":("🦊","聪明"),"熊猫":("🐼","可爱")}
STAGES = [(0,"蛋"),(10,"幼年"),(50,"少年"),(150,"青年"),(300,"成年")]

CAT_ART = {"idle":"  /\\_/\\\n ( o.o )\n  > ^ <","happy":"  /\\_/\\\n ( ^.^ ) ♪\n  > ~ <","sleep":"  /\\_/\\\n ( -.- ) z Z\n  > ~ <","sad":"  /\\_/\\\n ( T.T )\n  > ~ <"}
DOG_ART = {"idle":"  / \\__\n (    @\\___\n /         O\n/_____/  U","happy":"  / \\__\n (    @\\___  ♪\n /         O\n/_____/  U ~","sleep":"  / \\__\n (    -\\___  z Z\n /         O\n/_____/  U","sad":"  / \\__\n (    T\\___\n /         O\n/_____/  U"}
BUNNY_ART = {"idle":" (\\ /)\n ( . .)\n c(\")(\")", "happy":" (\\ /)\n ( ^.^) ♪\n c(\")(\")", "sleep":" (\\ /)\n ( -.-) z Z\n c(\")(\")", "sad":" (\\ /)\n ( T.T)\n c(\")(\")"}
ARTS = {"猫":CAT_ART,"狗":DOG_ART,"兔子":BUNNY_ART,"龙":CAT_ART,"狐狸":CAT_ART,"熊猫":CAT_ART}

TIPS = ["加油！你写的代码很棒！💪","bug只是还没变成feature~","休息一下吧！👀","记得喝水哦！🥤","每一行代码都是进步！📈","相信自己！🌟","代码能跑就是胜利！🏆","今天也是元气满满的一天！🌈","困了就休息，效率更重要！😴","不要忘记保存哦！📦"]

clamp = lambda v: max(0, min(100, v))

class VPet:
    def __init__(self, name, pt="猫"):
        self.name=name; self.pt=pt; self.emoji=PETS.get(pt,PETS["猫"])[0]
        self.hunger=50; self.happy=50; self.energy=80; self.hp=100
        self.exp=0; self.lv=1; self.coins=50; self.sleeping=False; self.count=0
    def stage(self):
        s="蛋"
        for th,nm in STAGES:
            if self.exp>=th: s=nm
        return s
    def mood(self):
        if self.energy<20: return "困倦😴"
        if self.hunger<20: return "饥饿😫"
        if self.happy>80: return "兴奋🤩"
        if self.happy>50: return "开心😊"
        if self.happy<30: return "难过😢"
        return "普通😐"
    def bar(self, v):
        f=int(v/5); return "█"*f+"░"*(20-f)
    def status(self):
        print(f"\n{'='*40}")
        print(f"  {self.emoji} {self.name} | {self.pt} | 性格: {PETS.get(self.pt,PETS['猫'])[1]}")
        print(f"  阶段: {self.stage()} | 等级: {self.lv} | 经验: {self.exp}")
        print(f"  心情: {self.mood()} | 金币: {self.coins}")
        if self.sleeping: print("  状态: 💤 睡觉中")
        print(f"{'─'*40}")
        for n,v in [("饱腹度",self.hunger),("快乐度",self.happy),("体力值",self.energy),("健康值",self.hp)]:
            print(f"  {n}: [{self.bar(v)}] {v}%")
        print(f"  互动次数: {self.count}\n{'='*40}")
    def feed(self, food):
        if food not in FOOD: print(f"没有这种食物！可选: {', '.join(FOOD.keys())}"); return
        h,hp,p = FOOD[food]
        if self.coins<p: print(f"金币不够！需要{p}，当前{self.coins}"); return
        if self.sleeping: print(f"{self.name}正在睡觉！"); return
        self.coins-=p; self.hunger=clamp(self.hunger+h); self.happy=clamp(self.happy+hp)
        self.exp+=5; self.lv=1+self.exp//30; self.count+=1
        print(f"{self.emoji} {self.name} 吃了 {food}！饱腹+{h} 快乐+{hp} 花费{p}金币")
        if self.exp in [t for t,_ in STAGES]: print(f"  ✨ 进化了！当前: {self.stage()}")
    def play(self, game):
        if game not in GAME: print(f"没有这个游戏！可选: {', '.join(GAME.keys())}"); return
        if self.sleeping: print(f"{self.name}正在睡觉！"); return
        if self.energy<10: print(f"{self.name}太累了！"); return
        hp,en = GAME[game]; r=random.randint(3,12)
        self.happy=clamp(self.happy+hp); self.energy=clamp(self.energy+en); self.coins+=r
        self.exp+=8; self.lv=1+self.exp//30; self.count+=1
        print(f"{self.emoji} {self.name} 玩了 {game}！快乐+{hp} 体力{en} 获得{r}金币")
    def pet_it(self):
        self.happy=clamp(self.happy+8); self.exp+=3; self.lv=1+self.exp//30; self.count+=1
        r=random.choice(["蹭了蹭你的手","发出满足的声音","开心地转圈圈","对你眨眨眼","跳到你怀里"])
        print(f"{self.emoji} {self.name}{r}！快乐+8")
    def toggle_sleep(self):
        if self.sleeping:
            self.sleeping=False; print(f"{self.emoji} {self.name} 醒了！精神满满！")
        else:
            self.sleeping=True; self.energy=clamp(self.energy+30); self.hp=clamp(self.hp+10)
            print(f"{self.emoji} {self.name} 睡着了...💤 体力+30 健康+10")
    def show_art(self, state="idle"):
        art = ARTS.get(self.pt, CAT_ART).get(state, CAT_ART["idle"])
        print(f"\n--- {self.name} ---\n{art}\n")

def virtual_pet():
    print("\n🎮 虚拟宠物系统")
    print("可选宠物:")
    for k,(e,t) in PETS.items(): print(f"  {e} {k} - {t}")
    pt = input("选择类型: ").strip()
    if pt not in PETS: pt="猫"
    name = input("起个名字: ").strip() or "小宝"
    p = VPet(name, pt)
    print(f"\n🎉 {p.emoji} {name} 诞生了！")
    while True:
        p.status(); p.show_art()
        print("  [1]喂食 [2]玩耍 [3]抚摸 [4]睡觉/醒来 [5]鼓励 [0]返回")
        c = input("  > ").strip()
        if c=="0": break
        elif c=="1":
            print(f"  食物: {', '.join(f'{k}(¥{v[2]})' for k,v in FOOD.items())}")
            p.feed(input("  选择: ").strip())
        elif c=="2":
            print(f"  游戏: {', '.join(GAME.keys())}")
            p.play(input("  选择: ").strip())
        elif c=="3": p.pet_it()
        elif c=="4": p.toggle_sleep()
        elif c=="5": p.show_art("happy"); print(f"💬 {name}: {random.choice(TIPS)}")

# ═══════════ CLI 伙伴 ═══════════
def cli_companion():
    print("\n🖥️ CLI 伙伴系统")
    for k in ARTS: print(f"\n  [{k}]"); print(ARTS[k]["idle"])
    pt = input("选择伙伴: ").strip()
    if pt not in ARTS: pt="猫"
    name = input("起个名字: ").strip() or "小伙伴"
    art = ARTS.get(pt, CAT_ART)
    while True:
        print(f"\n  当前伙伴: {name}")
        print("  [1]查看 [2]鼓励 [3]聊天 [4]表情 [0]返回")
        c = input("  > ").strip()
        if c=="0": break
        elif c=="1": print(f"\n--- {name} ---\n{art['idle']}")
        elif c=="2": print(f"\n--- {name} ---\n{art['happy']}\n💬 {name}: {random.choice(TIPS)}")
        elif c=="3":
            w=input("  说点什么: ").strip().lower()
            if any(x in w for x in ["error","bug","错","fail"]): print(f"\n{art['sad']}\n💬 {name}: 别灰心，我们一起解决！")
            elif any(x in w for x in ["success","done","完成","棒","好"]): print(f"\n{art['happy']}\n💬 {name}: 太棒了！🎉")
            elif any(x in w for x in ["累","困","tired"]): print(f"\n{art['sleep']}\n💬 {name}: 休息一下吧💤")
            else: print(f"\n{art['idle']}\n💬 {name}: 我在这里陪着你！")
        elif c=="4":
            s=input("  表情(idle/happy/sleep/sad): ").strip()
            print(f"\n--- {name} ---\n{art.get(s,art['idle'])}")

# ═══════════ 宠物管理 ═══════════
pets_db = {}

def pet_manager():
    global pets_db
    while True:
        print("\n📋 宠物管理系统")
        print("─"*40)
        print("  [1]所有宠物 [2]添加 [3]详情 [4]疫苗 [5]备注 [0]返回")
        c = input("  > ").strip()
        if c=="0": break
        elif c=="1":
            if not pets_db: print("  还没有宠物，先添加一只吧！"); continue
            emoji={"猫":"🐱","狗":"🐶","兔子":"🐰","鸟":"🐦","鱼":"🐟","仓鼠":"🐹","乌龟":"🐢"}
            print("\n🐾 我的宠物:")
            for n,p in pets_db.items():
                e=emoji.get(p["species"],"🐾")
                print(f"  {e} {n} | {p['species']} | {p.get('age',0)}岁 {p.get('weight',0)}kg")
            print(f"  共 {len(pets_db)} 只")
        elif c=="2":
            n=input("  名字: ").strip()
            s=input("  种类(猫/狗/兔子/鸟/鱼/仓鼠/乌龟): ").strip()
            b=input("  品种(可选): ").strip()
            try: a=float(input("  年龄: ").strip() or "0")
            except: a=0
            try: w=float(input("  体重kg: ").strip() or "0")
            except: w=0
            g=input("  性别(公/母): ").strip() or "未知"
            pets_db[n]={"species":s,"breed":b,"age":a,"weight":w,"gender":g,"vaccines":[],"notes":[]}
            print(f"  🐾 已添加: {n}")
        elif c=="3":
            n=input("  宠物名字: ").strip()
            if n not in pets_db: print(f"  找不到{n}"); continue
            p=pets_db[n]
            emoji={"猫":"🐱","狗":"🐶","兔子":"🐰","鸟":"🐦","鱼":"🐟","仓鼠":"🐹","乌龟":"🐢"}
            print(f"\n{'='*40}")
            print(f"  {emoji.get(p['species'],'🐾')} {n}")
            print(f"  种类: {p['species']}  品种: {p.get('breed','')}")
            print(f"  年龄: {p['age']}岁  体重: {p['weight']}kg  性别: {p['gender']}")
            if p.get("vaccines"):
                print(f"  💉 疫苗:")
                for v in p["vaccines"]: print(f"    - {v}")
            if p.get("notes"):
                print(f"  📝 备注:")
                for note in p["notes"][-5:]: print(f"    - {note}")
            print(f"{'='*40}")
        elif c=="4":
            n=input("  宠物名字: ").strip()
            if n not in pets_db: print(f"  找不到{n}"); continue
            v=input("  疫苗名称: ").strip()
            d=input("  日期: ").strip()
            pets_db[n].setdefault("vaccines",[]).append(f"{v} ({d})")
            print(f"  💉 已记录: {v}")
        elif c=="5":
            n=input("  宠物名字: ").strip()
            if n not in pets_db: print(f"  找不到{n}"); continue
            note=input("  备注: ").strip()
            pets_db[n].setdefault("notes",[]).append(note)
            print(f"  📝 已添加备注")

# ═══════════ 主菜单 ═══════════
def main():
    while True:
        print("""
    ╔══════════════════════════════════╗
    ║     🐾 Buddy - 宠物系统 🐾      ║
    ║                                  ║
    ║  1. 🎮 虚拟宠物 (电子宠物)       ║
    ║  2. 🖥️  CLI 伙伴 (编程陪伴)      ║
    ║  3. 📋 宠物管理 (真实宠物)       ║
    ║  0. 🚪 退出                      ║
    ╚══════════════════════════════════╝""")
        c = input("\n  选择 (1/2/3/0): ").strip()
        if c=="0": print("\n  👋 再见！下次再来玩哦！\n"); break
        elif c=="1": virtual_pet()
        elif c=="2": cli_companion()
        elif c=="3": pet_manager()

if __name__=="__main__": main()
