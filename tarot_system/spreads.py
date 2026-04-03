"""
牌阵定义 - Tarot Spreads
支持：单牌、三牌时间流、凯尔特十字牌阵
"""


SPREADS = {
    "single": {
        "name": "单牌占卜",
        "description": "抽取一张牌，直接反映当前核心问题",
        "count": 1,
        "positions": ["核心提示"],
    },
    "three": {
        "name": "三牌时间流",
        "description": "过去 - 现在 - 未来，展示事件发展脉络",
        "count": 3,
        "positions": ["过去（事件起因/背景）", "现在（当前状态/核心）", "未来（发展趋势/建议）"],
    },
    "cross": {
        "name": "凯尔特十字",
        "description": "经典大牌阵，适合深入分析复杂问题",
        "count": 10,
        "positions": [
            "现状（当前核心问题）",
            "挑战（主要障碍/阻力）",
            "潜意识（内心深层想法）",
            "过去（近期影响事件）",
            "上方（最佳可能结果）",
            "未来（即将发生的事）",
            "自我（你对问题的态度）",
            "环境（外界/他人影响）",
            "希望与恐惧（内心期待或担忧）",
            "最终结果（事件走向）",
        ],
    },
    "relationship": {
        "name": "感情关系牌阵",
        "description": "分析双方关系状态与发展方向",
        "count": 5,
        "positions": [
            "你的状态（你在关系中的位置）",
            "对方状态（对方的想法/态度）",
            "关系现状（两人之间的连接）",
            "挑战（需要面对的问题）",
            "建议（改善方向）",
        ],
    },
}


def get_spread(name):
    """获取牌阵定义"""
    return SPREADS.get(name)


def list_spreads():
    """列出所有可用牌阵"""
    result = []
    for key, spread in SPREADS.items():
        result.append(f"  [{key}] {spread['name']} ({spread['count']}张) - {spread['description']}")
    return "\n".join(result)
