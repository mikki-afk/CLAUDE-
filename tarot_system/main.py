#!/usr/bin/env python3
"""
Tarot System - 塔罗牌占卜系统
交互式 CLI 入口
"""

import sys
import time
import random

from tarot_system.cards import TAROT_DECK
from tarot_system.spreads import SPREADS, list_spreads, get_spread
from tarot_system.reader import TarotReader


def print_banner():
    print(r"""
    ╔══════════════════════════════════════════╗
    ║                                          ║
    ║        塔罗牌占卜系统                     ║
    ║        Tarot Reading System               ║
    ║                                          ║
    ║   基于韦特塔罗体系 · 78张完整牌组          ║
    ║                                          ║
    ╚══════════════════════════════════════════╝
    """)


def print_menu():
    print("\n  [1] 开始占卜")
    print("  [2] 查看所有牌阵")
    print("  [3] 浏览塔罗牌")
    print("  [4] 占卜历史")
    print("  [5] 塔罗小知识")
    print("  [0] 退出")


def meditation_prompt():
    """冥想引导"""
    prompts = [
        "请闭上眼睛，深呼吸三次...",
        "让心静下来，专注于你的问题...",
        "放下杂念，感受内心的声音...",
        "当你准备好了，按回车键抽牌。",
    ]
    print()
    for p in prompts:
        print(f"  {p}")
        time.sleep(1)


def shuffle_animation():
    """洗牌动画"""
    frames = ["  洗牌中 |", "  洗牌中 /", "  洗牌中 -", "  洗牌中 \\"]
    for _ in range(3):
        for frame in frames:
            print(f"\r{frame}", end="", flush=True)
            time.sleep(0.15)
    print("\r  洗牌完成！        ")


def choose_spread():
    """选择牌阵"""
    print("\n  请选择牌阵:")
    print(list_spreads())
    print()
    choice = input("  输入牌阵名称 (single/three/cross/relationship): ").strip().lower()
    spread = get_spread(choice)
    if not spread:
        print("  无效选择，使用默认三牌时间流。")
        spread = get_spread("three")
    return spread


def choose_topic():
    """选择解读主题"""
    print("\n  请选择解读方向:")
    print("  [1] 综合解读")
    print("  [2] 感情方向")
    print("  [3] 事业方向")
    choice = input("  > ").strip()
    if choice == "2":
        return "love"
    elif choice == "3":
        return "work"
    return "general"


def do_reading(reader):
    """执行一次完整占卜流程"""
    # 1. 选牌阵
    spread = choose_spread()
    print(f"\n  已选择: {spread['name']} ({spread['count']}张牌)")

    # 2. 输入问题
    print("\n  占卜注意事项:")
    print("  - 问题要单一、具体、短期（3-6个月）")
    print("  - 避免问生老病死、具体时间/数字")
    print("  - 同一问题短期内不要重复占卜")
    print()
    question = input("  请输入你的问题（可留空）: ").strip()

    # 3. 选主题
    topic = choose_topic()

    # 4. 冥想引导
    meditation_prompt()
    input()

    # 5. 洗牌抽牌
    shuffle_animation()

    # 6. 占卜
    reading = reader.read(spread, question)

    # 7. 显示结果
    print(reader.format_reading(reading, topic))

    # 8. 问是否再来
    again = input("  是否再占一次？(y/n): ").strip().lower()
    if again == "y":
        do_reading(reader)


def browse_cards():
    """浏览塔罗牌"""
    print("\n  浏览塔罗牌:")
    print("  [1] 大阿卡纳 (22张)")
    print("  [2] 权杖 (14张)")
    print("  [3] 圣杯 (14张)")
    print("  [4] 宝剑 (14张)")
    print("  [5] 星币 (14张)")
    print("  [0] 返回")

    choice = input("  > ").strip()
    filters = {
        "1": "大阿卡纳",
        "2": "权杖",
        "3": "圣杯",
        "4": "宝剑",
        "5": "星币",
    }

    suit = filters.get(choice)
    if not suit:
        return

    print(f"\n  === {suit} ===\n")
    for card in TAROT_DECK:
        if card["suit"] == suit:
            emoji = card.get("emoji", "")
            print(f"  {emoji} {card['name']} (#{card['number']})")
            print(f"     元素: {card['element']}")
            print(f"     正位: {card['upright']}")
            print(f"     逆位: {card['reversed']}")
            print()

    input("  按回车返回...")


def show_tips():
    """塔罗小知识"""
    tips = [
        "塔罗牌共78张：22张大阿卡纳代表人生重大课题，56张小阿卡纳反映日常事件。",
        "四元素对应：火(权杖)-行动热情、水(圣杯)-情感直觉、风(宝剑)-思维沟通、土(星币)-物质稳定。",
        "逆位不代表「坏」，而是能量受阻、需要反思或换个角度看待问题。",
        "韦特塔罗由爱德华·韦特和画家潘密拉·史密斯共同创作，是最流行的塔罗体系。",
        "塔罗与心理学家荣格的「集体潜意识」理论密切相关，是连接内心的工具。",
        "灵数1-10对应事件发展阶段：1开始→5动荡→10完成新生。",
        "占卜时心无杂念，专注一个问题，不要同时想多个事情。",
        "塔罗不是算命工具，而是帮助你理清思绪、照见内心的一面镜子。",
        "同一问题建议2周到1个月后再复占，以第一次专注状态下的结果为准。",
        "宫廷牌（国王、皇后、骑士、侍从）通常代表人物性格或角色互动。",
    ]
    print("\n  === 塔罗小知识 ===\n")
    selected = random.sample(tips, min(3, len(tips)))
    for i, tip in enumerate(selected, 1):
        print(f"  {i}. {tip}")
        print()
    input("  按回车返回...")


def main():
    print_banner()

    reader = TarotReader(TAROT_DECK)

    while True:
        print_menu()
        choice = input("\n  请选择 > ").strip()

        if choice == "0":
            print("\n  愿塔罗的智慧指引你前行。再见！\n")
            sys.exit(0)
        elif choice == "1":
            do_reading(reader)
        elif choice == "2":
            print(f"\n{list_spreads()}")
            input("\n  按回车返回...")
        elif choice == "3":
            browse_cards()
        elif choice == "4":
            print(reader.get_history())
            input("\n  按回车返回...")
        elif choice == "5":
            show_tips()
        else:
            print("  无效选择，请输入 0-5")


if __name__ == "__main__":
    main()
