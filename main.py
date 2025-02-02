import random
import re
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register

@register("dnd_Dice", "scwunai", "一个 DnD 骰子插件，支持格式 xdY 和检定功能", "1.0.0")
class DnDDicePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("roll")
    async def roll_dice(self, event: AstrMessageEvent, dice: str, threshold: int = 10):
        # 正则表达式匹配 xdy 格式
        match = re.match(r'(\d*)d(\d+)', dice)

        if not match:
            yield event.plain_result("请输入有效的格式，例如 `1d6` 或 `2d20`。")
            return
        
        # 提取投掷次数和面数
        num_rolls = int(match.group(1)) if match.group(1) else 1  # 默认为 1
        sides = int(match.group(2))

        results = [random.randint(1, sides) for _ in range(num_rolls)]
        total = sum(results)
        
        # 输出每次投掷的结果
        results_str = ', '.join(map(str, results))
        yield event.plain_result(f"你投掷的结果是: {results_str} (总和: {total})")
        
        # 检定成功失败的逻辑
        if total >= threshold:  # 使用用户传入的成功阈值
            yield event.plain_result(f"检定成功！ (成功阈值: {threshold})")
        else:
            yield event.plain_result(f"检定失败！ (成功阈值: {threshold})")