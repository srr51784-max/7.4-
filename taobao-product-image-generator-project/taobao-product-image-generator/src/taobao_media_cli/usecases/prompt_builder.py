from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

STYLE_PRESETS: Dict[str, str] = {
    "blue-business": "蓝色简约商务风，白色和浅蓝渐变背景，干净专业，有品牌授权感，适合淘宝汽车配件类目",
    "deep-blue-business": "深蓝色高级商务风，科技感线条，稳重专业，突出品牌和品质",
    "red-promo": "红色喜庆促销风，三周年庆或活动促销氛围，视觉冲击强但不杂乱",
    "apple-minimal": "苹果官网式极简风，大量留白，高级灰白背景，精致光影，现代高级感",
    "white-clean": "白底精修风，纯白背景，产品单独展示，不添加文字和装饰",
    "black-premium": "黑色高级质感风，暗色背景，金属高光，适合高端产品展示",
}

IMAGE_TYPE_RULES: Dict[str, str] = {
    "main": "淘宝1:1主图，产品居中放大，占画面65%-75%，短卖点标签，首图要有点击欲望",
    "detail": "电商详情页竖图，默认1440x1920px，分区清晰，一张图只讲一个重点",
    "white": "白底精修图，只展示产品本体，不要文字、图标、包装盒、背景装饰或额外元素",
    "poster": "商业海报风，突出活动主题和核心卖点，产品仍然是画面主体",
    "comparison": "对比展示图，用简洁左右对比结构突出卖点，不夸大不虚假",
    "edit": "基于参考图编辑，严格保持产品形状、角度、比例、结构和材质，不改变产品本体",
}

SELLING_POINTS = [
    "品牌正版授权",
    "高清实拍质感",
    "精准适配车型",
    "稳定耐用结构",
    "安装适配清晰",
    "商务视觉升级",
    "白底精修展示",
    "细节清晰可见",
    "质感光影强化",
    "平台主图规范",
]


@dataclass
class PromptRequest:
    product: str
    image_type: str = "main"
    style: str = "blue-business"
    ratio: str = "1:1"
    count: int = 1
    platform: str = "淘宝"
    store_name: Optional[str] = None
    watermark: Optional[str] = None
    keep_shape: bool = True
    remove_packaging: bool = False
    language: str = "zh"
    extra: Optional[str] = None


def _copy_for_index(index: int, image_type: str) -> str:
    if image_type == "white":
        return "不添加任何文字，只做白底产品精修"
    point_a = SELLING_POINTS[index % len(SELLING_POINTS)]
    point_b = SELLING_POINTS[(index + 3) % len(SELLING_POINTS)]
    return f"短文案只突出：{point_a}、{point_b}；文字简短，不要密集排版"


def build_prompt(req: PromptRequest, index: int = 0) -> str:
    style_text = STYLE_PRESETS.get(req.style, req.style)
    type_rule = IMAGE_TYPE_RULES.get(req.image_type, IMAGE_TYPE_RULES["main"])
    parts: List[str] = [
        f"为{req.platform}生成一张电商产品图。",
        f"产品：{req.product}。",
        f"图片类型：{type_rule}。",
        f"视觉风格：{style_text}。",
        f"画面比例/尺寸：{req.ratio}。",
        "产品要清晰、放大、主体突出，光影真实，商业摄影质感。",
    ]

    if req.keep_shape:
        parts.append("严格保持参考产品的原始形状、角度、结构、材质和关键细节，不要改造产品本体。")
    if req.remove_packaging:
        parts.append("去掉包装盒和无关背景，只保留产品本体和必要设计元素。")
    if req.store_name and req.image_type != "white":
        parts.append(f"将店铺名“{req.store_name}”自然设计到画面中，字号小，不抢产品主体。")
    if req.watermark and req.image_type != "white":
        parts.append(f"在画面中部添加半透明水印“{req.watermark}”，使用微软雅黑风格，透明度低，不遮挡产品识别。")

    parts.append(_copy_for_index(index, req.image_type))
    parts.append("避免虚假夸张承诺；不要添加未提供的官方logo；不要让文字遮挡产品。")

    if req.extra:
        parts.append(f"额外要求：{req.extra}")

    return "\n".join(parts)


def build_prompts(req: PromptRequest) -> List[Dict[str, str]]:
    return [
        {
            "index": str(i + 1),
            "image_type": req.image_type,
            "ratio": req.ratio,
            "prompt": build_prompt(req, i),
        }
        for i in range(req.count)
    ]


def request_from_dict(data: Dict[str, object]) -> PromptRequest:
    return PromptRequest(
        product=str(data.get("product") or "未命名产品"),
        image_type=str(data.get("image_type") or "main"),
        style=str(data.get("style") or "blue-business"),
        ratio=str(data.get("ratio") or data.get("size") or "1:1"),
        count=int(data.get("count") or data.get("n") or 1),
        platform=str(data.get("platform") or "淘宝"),
        store_name=(str(data.get("store_name")) if data.get("store_name") else None),
        watermark=(str(data.get("watermark")) if data.get("watermark") else None),
        keep_shape=bool(data.get("keep_shape", True)),
        remove_packaging=bool(data.get("remove_packaging", False)),
        language=str(data.get("language") or "zh"),
        extra=(str(data.get("extra")) if data.get("extra") else None),
    )
