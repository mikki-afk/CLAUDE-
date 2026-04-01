#!/usr/bin/env python3
"""
Buddy - Claude 宠物系统
主入口：整合虚拟宠物、CLI伙伴和宠物管理三大功能
"""

import sys
from buddy.virtual_pet.pet import VirtualPet, PET_TYPES, FOOD_MENU, GAMES
from buddy.cli_companion.companion import CLICompanion
from buddy.pet_manager.manager import PetManager


def print_banner():
    print(r"""
    ╔══════════════════════════════════════╗
    ║     🐾 Buddy - 宠物系统 🐾          ║
    ║                                      ║
    ║  1. 🎮 虚拟宠物 (电子宠物)           ║
    ║  2. 🖥️  CLI 伙伴 (编程陪伴)          ║
    ║  3. 📋 宠物管理 (真实宠物)           ║
    ║  0. 🚪 退出                          ║
    ╚══════════════════════════════════════╝
    """)


# ──────────────── 虚拟宠物 ────────────────

def virtual_pet_menu():
    print("\n🎮 虚拟宠物系统")
    print("─" * 40)
    saved = VirtualPet.list_saved()
    if saved:
        print(f"  已有存档: {', '.join(saved)}")

    choice = input("  [1] 创建新宠物  [2] 加载存档  [0] 返回: ").strip()
    if choice == "1":
        return create_virtual_pet()
    elif choice == "2":
        if not saved:
            print("  没有存档！")
            return None
        name = input(f"  输入宠物名字 ({', '.join(saved)}): ").strip()
        try:
            return VirtualPet.load(name)
        except FileNotFoundError:
            print(f"  找不到 {name} 的存档")
            return None
    return None


def create_virtual_pet() -> VirtualPet | None:
    print("\n  可选宠物类型:")
    for pt, info in PET_TYPES.items():
        print(f"    {info['emoji']} {pt} - 性格: {info['trait']}")
    pet_type = input("  选择类型: ").strip()
    if pet_type not in PET_TYPES:
        print("  无效类型！")
        return None
    name = input("  给宠物起个名字: ").strip()
    if not name:
        print("  名字不能为空！")
        return None
    pet = VirtualPet(name, pet_type)
    print(f"\n  🎉 {PET_TYPES[pet_type]['emoji']} {name} 诞生了！")
    return pet


def virtual_pet_loop(pet: VirtualPet):
    companion = CLICompanion(pet.pet_type, pet.name)

    while True:
        print(pet.status())
        print(companion.show())
        print("  [1] 喂食  [2] 玩耍  [3] 抚摸  [4] 睡觉/叫醒")
        print("  [5] 鼓励  [6] 保存  [0] 返回")
        choice = input("  > ").strip()

        if choice == "0":
            save = input("  保存后退出？(y/n): ").strip().lower()
            if save == "y":
                print(pet.save())
            break
        elif choice == "1":
            print(f"\n  菜单: {', '.join(f'{k}(¥{v["price"]})' for k, v in FOOD_MENU.items())}")
            food = input("  选择食物: ").strip()
            print(pet.feed(food))
        elif choice == "2":
            print(f"\n  游戏: {', '.join(GAMES.keys())}")
            game = input("  选择游戏: ").strip()
            print(pet.play(game))
        elif choice == "3":
            print(pet.pet())
        elif choice == "4":
            if pet.is_sleeping:
                print(pet.wake())
            else:
                print(pet.sleep())
        elif choice == "5":
            print(companion.encourage())
        elif choice == "6":
            print(pet.save())

        event = companion.random_event()
        if event:
            print(event)


# ──────────────── CLI 伙伴 ────────────────

def cli_companion_menu():
    print("\n🖥️  CLI 伙伴系统")
    print("─" * 40)
    companion = CLICompanion()

    print(companion.available_pets())
    pet_type = input("  选择伙伴类型: ").strip()
    name = input("  给伙伴起个名字: ").strip() or "小伙伴"
    companion = CLICompanion(pet_type, name)

    while True:
        print(f"\n  当前伙伴: {name}")
        print("  [1] 查看伙伴  [2] 获得鼓励  [3] 对话")
        print("  [4] 切换状态  [5] 查看全部伙伴  [0] 返回")
        choice = input("  > ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print(companion.show())
        elif choice == "2":
            print(companion.encourage())
        elif choice == "3":
            keyword = input("  说点什么: ").strip()
            print(companion.react(keyword))
        elif choice == "4":
            state = input("  状态 (idle/happy/sleep/eat/sad): ").strip()
            print(companion.show(state))
        elif choice == "5":
            print(companion.available_pets())


# ──────────────── 宠物管理 ────────────────

def pet_manager_menu():
    manager = PetManager()

    while True:
        print("\n📋 宠物管理系统")
        print("─" * 40)
        print("  [1] 查看所有宠物  [2] 添加宠物  [3] 查看宠物详情")
        print("  [4] 添加疫苗记录  [5] 添加医疗记录  [6] 添加喂食计划")
        print("  [7] 添加备注  [8] 疫苗提醒  [9] 删除宠物  [0] 返回")
        choice = input("  > ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print(manager.list_pets())
        elif choice == "2":
            name = input("  宠物名字: ").strip()
            species = input("  种类 (猫/狗/兔子/鸟/鱼/仓鼠/乌龟): ").strip()
            breed = input("  品种 (可选): ").strip()
            try:
                age = float(input("  年龄: ").strip() or "0")
                weight = float(input("  体重(kg): ").strip() or "0")
            except ValueError:
                age, weight = 0, 0
            gender = input("  性别 (公/母/未知): ").strip() or "未知"
            print(manager.add_pet(name, species, breed, age, weight, gender))
        elif choice == "3":
            name = input("  宠物名字: ").strip()
            pet = manager.get_pet(name)
            if pet:
                print(pet.profile())
            else:
                print(f"  找不到 {name}")
        elif choice == "4":
            name = input("  宠物名字: ").strip()
            pet = manager.get_pet(name)
            if pet:
                vax = input("  疫苗名称: ").strip()
                date = input("  接种日期 (YYYY-MM-DD): ").strip()
                next_date = input("  下次接种日期 (可选): ").strip()
                print(pet.add_vaccination(vax, date, next_date))
                manager.save()
            else:
                print(f"  找不到 {name}")
        elif choice == "5":
            name = input("  宠物名字: ").strip()
            pet = manager.get_pet(name)
            if pet:
                desc = input("  描述: ").strip()
                date = input("  日期 (YYYY-MM-DD): ").strip()
                doctor = input("  医生 (可选): ").strip()
                try:
                    cost = float(input("  费用 (可选): ").strip() or "0")
                except ValueError:
                    cost = 0
                print(pet.add_medical_record(desc, date, doctor, cost))
                manager.save()
            else:
                print(f"  找不到 {name}")
        elif choice == "6":
            name = input("  宠物名字: ").strip()
            pet = manager.get_pet(name)
            if pet:
                t = input("  喂食时间 (如 08:00): ").strip()
                food = input("  食物: ").strip()
                amount = input("  量: ").strip()
                print(pet.add_feeding_schedule(t, food, amount))
                manager.save()
            else:
                print(f"  找不到 {name}")
        elif choice == "7":
            name = input("  宠物名字: ").strip()
            pet = manager.get_pet(name)
            if pet:
                note = input("  备注内容: ").strip()
                print(pet.add_note(note))
                manager.save()
            else:
                print(f"  找不到 {name}")
        elif choice == "8":
            print(manager.upcoming_vaccinations())
        elif choice == "9":
            name = input("  宠物名字: ").strip()
            confirm = input(f"  确认删除 {name}? (y/n): ").strip().lower()
            if confirm == "y":
                print(manager.remove_pet(name))


# ──────────────── 主程序 ────────────────

def main():
    print_banner()

    while True:
        choice = input("\n  请选择功能 (1/2/3/0): ").strip()

        if choice == "0":
            print("\n  👋 再见！下次再来陪宠物玩哦！\n")
            sys.exit(0)
        elif choice == "1":
            pet = virtual_pet_menu()
            if pet:
                virtual_pet_loop(pet)
        elif choice == "2":
            cli_companion_menu()
        elif choice == "3":
            pet_manager_menu()
        else:
            print("  无效选择，请输入 1, 2, 3 或 0")
            print_banner()


if __name__ == "__main__":
    main()
