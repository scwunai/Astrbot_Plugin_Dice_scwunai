import random
import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

@register("dnd_dice", "Your Name", "一个 DnD 骰子插件，支持格式 xdY 和检定功能", "1.0.0")
class DicePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    # 注册指令 /roll  <次数>d<面数> <检定阈值>
    @filter.command("roll")
    async def roll_dice(self, event: AstrMessageEvent, dice: str, threshold: int):
        """
        掷骰子的逻辑，支持格式 xdy (默认 1d6) 和阈值。
        """
        try:
            # 解析 xdy 格式的骰子
            roll_count, die_faces = map(int, dice.lower().split('d'))
        except ValueError:
            roll_count, die_faces = 1, 6  # 默认值为 1d6

        # 投掷骰子
        rolls = [random.randint(1, die_faces) for _ in range(roll_count)]
        success_count = sum(1 for roll in rolls if roll >= threshold)
        
        # 输出投掷结果
        result_message = f"你投掷了 {roll_count} 次 {die_faces} 面骰子，结果: {', '.join(map(str, rolls))}。\n"
        result_message += f"检定成功的次数: {success_count}/{roll_count} 次\n"
        
        # 判断是否有成功的检定
        if success_count > 0:
            result_message += f"你有 {success_count} 次成功检定！"
        else:
            result_message += "很遗憾，你没有成功的检定。"
        
        # 发送结果
        yield event.plain_result(result_message)
