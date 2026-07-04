# 淘宝产品图 AI 生成 Skill

这是一个可上传 Skill、也可发布到 GitHub 的 AI 电商图片生成项目。它参考了 Ultimate-AI-Media-Generator-Skill 的结构：`SKILL.md`、提示词库、工作流、Python CLI、API Key 配置和通用 API 调用层。

## 主要功能

- 生成淘宝/天猫/京东/拼多多产品主图提示词
- 支持 1:1 主图
- 支持 1440x1920px 详情图
- 支持白底精修图
- 支持一次生成 5 张或 10 张独立图片请求
- 默认保持产品形状、角度、结构不变
- 支持蓝色商务风、深蓝商务风、红色促销风、苹果官网极简风、白底精修风
- 支持通用图片 API 接入
- 支持本地预估消耗

## 快速使用

生成 5 张淘宝主图提示词：

```bash
python3 scripts/taobao_media.py prompt \
  --product "汽车减震器" \
  --image-type main \
  --style blue-business \
  --ratio 1:1 \
  --count 5 \
  --store-name "广州君成贸易有限公司"
```

把一个 JSON 请求展开成 5 张独立图片请求：

```bash
python3 scripts/taobao_media.py batch \
  --json examples/taobao-main-image.json \
  --output batch-payloads.json
```

本地预估消耗：

```bash
python3 scripts/taobao_media.py quote --json '{"media_type":"image","model":"standard-image","count":5,"resolution":"1k"}'
```

配置 API：

```bash
python3 scripts/taobao_media.py setup-api-key "你的_api_key" \
  --api-base "https://你的接口域名" \
  --image-endpoint "/generate-image"
```

生成图片请求：

```bash
python3 scripts/taobao_media.py generate-image --json examples/taobao-main-image.json
```

只查看发送内容，不真正提交：

```bash
python3 scripts/taobao_media.py generate-image --dry-run --json examples/taobao-main-image.json
```

## 适合你的场景

- “给这款产品设计 5 张淘宝主图”
- “比例 1:1，蓝色简约商务风”
- “改成 1440x1920px 详情图”
- “白底精修，只展示产品”
- “产品形状不要改变”
- “去掉包装盒”
- “把店铺名放到每张图上”

## 发布到 GitHub 后的安装方式

```bash
npx skills add 你的GitHub名/taobao-product-image-generator --all
```
