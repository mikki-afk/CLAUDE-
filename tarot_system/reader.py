"""
塔罗占卜引擎 - Tarot Reader
洗牌、抽牌、正逆位判定、解读输出
"""

import random
from datetime import datetime


class TarotReader:
    """塔罗占卜师"""

    def __init__(self, cards):
        """
        Args:
            cards: 牌库列表，每张牌是 dict，至少包含:
                   name, number, suit, element, upright, reversed,
                   upright_love, reversed_love, upright_work, reversed_work
        """
        self.deck = list(cards)
        self.history = []

    def shuffle(self):
        """洗牌"""
        random.shuffle(self.deck)

    def draw(self, count):
        """
        抽牌并决定正逆位
        Returns: list of (card, is_reversed)
        """
        self.shuffle()
        drawn = random.sample(self.deck, min(count, len(self.deck)))
        result = []
        for card in drawn:
            is_reversed = random.random() < 0.5
            result.append((card, is_reversed))
        return result

    def read(self, spread, question=""):
        """
        执行一次完整占卜
        Args:
            spread: 牌阵定义 dict (from spreads.py)
            question: 用户的问题
        Returns:
            reading dict
        """
        drawn = self.draw(spread["count"])
        positions = spread["positions"]

        reading = {
            "spread_name": spread["name"],
            "question": question,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "cards": [],
        }

        for i, (card, is_reversed) in enumerate(drawn):
            position = positions[i] if i < len(positions) else f"位置{i+1}"
            reading["cards"].append({
                "position": position,
                "card": card,
                "is_reversed": is_reversed,
            })

        self.history.append(reading)
        return reading

    def format_reading(self, reading, topic="general"):
        """
        格式化占卜结果为可显示的字符串
        Args:
            reading: read() 返回的 dict
            topic: 'general' | 'love' | 'work'
        """
        lines = []
        lines.append("")
        lines.append("=" * 50)
        lines.append(f"  {reading['spread_name']}")
        lines.append(f"  时间: {reading['timestamp']}")
        if reading["question"]:
            lines.append(f"  问题: {reading['question']}")
        lines.append("=" * 50)

        for item in reading["cards"]:
            card = item["card"]
            is_reversed = item["is_reversed"]
            orientation = "逆位" if is_reversed else "正位"
            emoji = card.get("emoji", "")

            lines.append("")
            lines.append(f"  [{item['position']}]")
            lines.append(f"  {emoji} {card['name']} ({orientation})")
            lines.append(f"  编号: {card['number']}  元素: {card['element']}")
            lines.append("")

            # 根据主题选择解读
            if is_reversed:
                keywords = card.get("reversed", "")
                if topic == "love":
                    detail = card.get("reversed_love", card.get("reversed", ""))
                elif topic == "work":
                    detail = card.get("reversed_work", card.get("reversed", ""))
                else:
                    detail = card.get("reversed", "")
            else:
                keywords = card.get("upright", "")
                if topic == "love":
                    detail = card.get("upright_love", card.get("upright", ""))
                elif topic == "work":
                    detail = card.get("upright_work", card.get("upright", ""))
                else:
                    detail = card.get("upright", "")

            lines.append(f"  关键词: {keywords}")
            lines.append(f"  解读: {detail}")
            lines.append("  " + "-" * 46)

        # 综合建议
        lines.append("")
        lines.append("  [综合建议]")
        lines.append(f"  {self._generate_advice(reading, topic)}")
        lines.append("")
        lines.append("=" * 50)
        lines.append("  塔罗从不给标准答案，而是帮你理清思绪，")
        lines.append("  让你在迷茫中找到属于自己的方向。")
        lines.append("=" * 50)
        lines.append("")

        return "\n".join(lines)

    def _generate_advice(self, reading, topic):
        """根据牌面生成简要综合建议"""
        cards_info = reading["cards"]
        reversed_count = sum(1 for c in cards_info if c["is_reversed"])
        total = len(cards_info)

        if total == 0:
            return "请先抽牌。"

        # 分析正逆位比例
        if reversed_count == 0:
            energy = "整体能量积极正向"
        elif reversed_count == total:
            energy = "整体能量提示需要反思和调整"
        elif reversed_count > total / 2:
            energy = "逆位牌偏多，提示有些方面需要关注和调整"
        else:
            energy = "正逆位平衡，事情在发展中"

        # 分析元素分布
        elements = {}
        for item in cards_info:
            elem = item["card"].get("element", "")
            if elem:
                elements[elem] = elements.get(elem, 0) + 1

        element_hint = ""
        if elements:
            dominant = max(elements, key=elements.get)
            element_map = {
                "火": "行动力和热情是关键",
                "水": "情感和直觉很重要",
                "风": "沟通和思考是重点",
                "土": "务实和稳定是基础",
                "大阿卡纳": "这个问题涉及重要的人生课题",
            }
            element_hint = element_map.get(dominant, "")

        parts = [energy]
        if element_hint:
            parts.append(element_hint)

        if topic == "love":
            parts.append("感情中记得倾听内心真实的声音")
        elif topic == "work":
            parts.append("事业上保持清醒的判断和持续的努力")
        else:
            parts.append("相信自己的直觉，同时保持理性思考")

        return "。".join(parts) + "。"

    def get_history(self):
        """获取占卜历史"""
        if not self.history:
            return "  暂无占卜记录。"
        lines = ["\n  占卜历史:"]
        for i, r in enumerate(self.history, 1):
            cards_str = ", ".join(
                f"{c['card']['name']}({'逆' if c['is_reversed'] else '正'})"
                for c in r["cards"]
            )
            lines.append(f"  {i}. [{r['timestamp']}] {r['spread_name']}")
            if r["question"]:
                lines.append(f"     问题: {r['question']}")
            lines.append(f"     牌面: {cards_str}")
        return "\n".join(lines)
