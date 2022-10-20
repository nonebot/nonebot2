---
description: Changelog
toc_max_heading_level: 2
---

# 更新日志

## 最近更新

### 🚀 新功能

- Feature: 新增 dotenv 嵌套配置项支持 [@yanyongyu](https://github.com/yanyongyu) ([#1324](https://github.com/nonebot/nonebot2/pull/1324))
- Feature: 添加 State 响应器触发消息注入 [@A-kirami](https://github.com/A-kirami) ([#1315](https://github.com/nonebot/nonebot2/pull/1315))
- Remove: 移除无用的 namespace 声明 [@yanyongyu](https://github.com/yanyongyu) ([#1306](https://github.com/nonebot/nonebot2/pull/1306))

### 💫 杂项

- Plugin: 补充 novelai 插件信息 [@sena-nana](https://github.com/sena-nana) ([#1333](https://github.com/nonebot/nonebot2/pull/1333))
- Bot: 修改 Inkar Suki 描述 [@HornCopper](https://github.com/HornCopper) ([#1312](https://github.com/nonebot/nonebot2/pull/1312))
- Plugin: 修改插件 MCQQ MCRcon 主页地址 [@17TheWord](https://github.com/17TheWord) ([#1303](https://github.com/nonebot/nonebot2/pull/1303))

### 🍻 插件发布

- Plugin: kfcrazy [@yanyongyu](https://github.com/yanyongyu) ([#1339](https://github.com/nonebot/nonebot2/pull/1339))
- Plugin: 二次元图像鉴赏 [@yanyongyu](https://github.com/yanyongyu) ([#1337](https://github.com/nonebot/nonebot2/pull/1337))
- Plugin: ayaka 衍生插件 - 坏词撤回 [@yanyongyu](https://github.com/yanyongyu) ([#1335](https://github.com/nonebot/nonebot2/pull/1335))
- Plugin: ayaka 衍生插件 - 时区助手 [@yanyongyu](https://github.com/yanyongyu) ([#1332](https://github.com/nonebot/nonebot2/pull/1332))
- Plugin: ayaka 衍生插件 - 谁是卧底 [@yanyongyu](https://github.com/yanyongyu) ([#1330](https://github.com/nonebot/nonebot2/pull/1330))
- Plugin: ayaka 衍生插件 - 小游戏合集 [@yanyongyu](https://github.com/yanyongyu) ([#1328](https://github.com/nonebot/nonebot2/pull/1328))
- Plugin: bnhhsh -「不能好好说话！」 [@yanyongyu](https://github.com/yanyongyu) ([#1326](https://github.com/nonebot/nonebot2/pull/1326))
- Plugin: AI 绘图 [@yanyongyu](https://github.com/yanyongyu) ([#1323](https://github.com/nonebot/nonebot2/pull/1323))
- Plugin: novelai [@yanyongyu](https://github.com/yanyongyu) ([#1319](https://github.com/nonebot/nonebot2/pull/1319))
- Plugin: 游戏王小程序查价 [@yanyongyu](https://github.com/yanyongyu) ([#1317](https://github.com/nonebot/nonebot2/pull/1317))
- Plugin: 监测群事件 [@yanyongyu](https://github.com/yanyongyu) ([#1320](https://github.com/nonebot/nonebot2/pull/1320))
- Plugin: 轮盘禁言小游戏 [@yanyongyu](https://github.com/yanyongyu) ([#1311](https://github.com/nonebot/nonebot2/pull/1311))
- Plugin: 真白萌自动签到 [@yanyongyu](https://github.com/yanyongyu) ([#1308](https://github.com/nonebot/nonebot2/pull/1308))
- Plugin: BiliRequestAll [@yanyongyu](https://github.com/yanyongyu) ([#1302](https://github.com/nonebot/nonebot2/pull/1302))
- Plugin: 监听者 [@yanyongyu](https://github.com/yanyongyu) ([#1299](https://github.com/nonebot/nonebot2/pull/1299))

### 🍻 适配器发布

- Adapter: Ntchat [@yanyongyu](https://github.com/yanyongyu) ([#1314](https://github.com/nonebot/nonebot2/pull/1314))

## v2.0.0-rc.1

### 💥 破坏性变更

- Feature: `SUPERUSER` 权限匹配任意超管事件 [@AkiraXie](https://github.com/AkiraXie) ([#1275](https://github.com/nonebot/nonebot2/pull/1275))
- Remove: 移除过时的 State 注入参数 [@yanyongyu](https://github.com/yanyongyu) ([#1160](https://github.com/nonebot/nonebot2/pull/1160))
- Remove: 移除过时的 `nonebot.plugins` toml 配置 [@yanyongyu](https://github.com/yanyongyu) ([#1151](https://github.com/nonebot/nonebot2/pull/1151))
- Remove: 移除 Python 3.7 支持 [@yanyongyu](https://github.com/yanyongyu) ([#1148](https://github.com/nonebot/nonebot2/pull/1148))
- Remove: 删除过时的 Export 功能 [@yanyongyu](https://github.com/yanyongyu) ([#1125](https://github.com/nonebot/nonebot2/pull/1125))

### 🚀 新功能

- Feature: `SUPERUSER` 权限匹配任意超管事件 [@AkiraXie](https://github.com/AkiraXie) ([#1275](https://github.com/nonebot/nonebot2/pull/1275))
- Feature: 改进 `CommandGroup` 与 `MatcherGroup` 的结构 [@A-kirami](https://github.com/A-kirami) ([#1240](https://github.com/nonebot/nonebot2/pull/1240))
- Feature: 调整日志输出格式与等级 [@yanyongyu](https://github.com/yanyongyu) ([#1233](https://github.com/nonebot/nonebot2/pull/1233))
- Feature: 优化依赖注入结构 [@yanyongyu](https://github.com/yanyongyu) ([#1227](https://github.com/nonebot/nonebot2/pull/1227))
- Featue: `load_plugin` 支持 `pathlib.Path` [@Lancercmd](https://github.com/Lancercmd) ([#1194](https://github.com/nonebot/nonebot2/pull/1194))
- Feature: 新增事件类型过滤 rule [@yanyongyu](https://github.com/yanyongyu) ([#1183](https://github.com/nonebot/nonebot2/pull/1183))
- Feature: shell command 添加富文本支持 [@yanyongyu](https://github.com/yanyongyu) ([#1171](https://github.com/nonebot/nonebot2/pull/1171))

### 🐛 Bug 修复

- Fix: 内置规则和权限没有捕获错误 [@yanyongyu](https://github.com/yanyongyu) ([#1291](https://github.com/nonebot/nonebot2/pull/1291))
- Fix: 修复 User 会话权限更新嵌套问题 [@yanyongyu](https://github.com/yanyongyu) ([#1208](https://github.com/nonebot/nonebot2/pull/1208))
- Fix: 修复当消息与不支持的类型相加时抛出的异常类型错误 [@mnixry](https://github.com/mnixry) ([#1166](https://github.com/nonebot/nonebot2/pull/1166))

### 💫 杂项

- Fix: 修正 GenshinUID 的发布类型 [@A-kirami](https://github.com/A-kirami) ([#1243](https://github.com/nonebot/nonebot2/pull/1243))
- Remove: 移除未使用的导入 [@A-kirami](https://github.com/A-kirami) ([#1236](https://github.com/nonebot/nonebot2/pull/1236))
- Plugin: 更新插件米游社辅助工具 tag [@Ljzd-PRO](https://github.com/Ljzd-PRO) ([#1221](https://github.com/nonebot/nonebot2/pull/1221))
- Plugin: 修改插件多功能简易群管信息 [@HuYihe2008](https://github.com/HuYihe2008) ([#1180](https://github.com/nonebot/nonebot2/pull/1180))
- Plugin: 修改插件多功能简易群管信息 [@HuYihe2008](https://github.com/HuYihe2008) ([#1159](https://github.com/nonebot/nonebot2/pull/1159))
- Plugin: 修改 QQ 续火花插件信息 [@GC-ZF](https://github.com/GC-ZF) ([#1158](https://github.com/nonebot/nonebot2/pull/1158))
- Plugin: 修改插件多功能简易群管信息 [@HuYihe2008](https://github.com/HuYihe2008) ([#1154](https://github.com/nonebot/nonebot2/pull/1154))

### 🍻 插件发布

- Plugin: 文字识别 [@yanyongyu](https://github.com/yanyongyu) ([#1295](https://github.com/nonebot/nonebot2/pull/1295))
- Plugin: 在线编曲 [@yanyongyu](https://github.com/yanyongyu) ([#1293](https://github.com/nonebot/nonebot2/pull/1293))
- Plugin: 图灵机器人 [@yanyongyu](https://github.com/yanyongyu) ([#1289](https://github.com/nonebot/nonebot2/pull/1289))
- Plugin: PicStatus [@yanyongyu](https://github.com/yanyongyu) ([#1287](https://github.com/nonebot/nonebot2/pull/1287))
- Plugin: 阿里云盘福利码自动兑换 [@yanyongyu](https://github.com/yanyongyu) ([#1283](https://github.com/nonebot/nonebot2/pull/1283))
- Plugin: gal 角色语音生成 [@yanyongyu](https://github.com/yanyongyu) ([#1281](https://github.com/nonebot/nonebot2/pull/1281))
- Plugin: 漂流瓶 [@yanyongyu](https://github.com/yanyongyu) ([#1279](https://github.com/nonebot/nonebot2/pull/1279))
- Plugin: BWIKI 助手移植版 [@yanyongyu](https://github.com/yanyongyu) ([#1274](https://github.com/nonebot/nonebot2/pull/1274))
- Plugin: nonebot 物联网插件 [@yanyongyu](https://github.com/yanyongyu) ([#1265](https://github.com/nonebot/nonebot2/pull/1265))
- Plugin: 狼人杀插件 [@yanyongyu](https://github.com/yanyongyu) ([#1252](https://github.com/nonebot/nonebot2/pull/1252))
- Plugin: ayaka - 文字游戏开发辅助插件 [@yanyongyu](https://github.com/yanyongyu) ([#1254](https://github.com/nonebot/nonebot2/pull/1254))
- Plugin: 图像超分辨率重建 [@yanyongyu](https://github.com/yanyongyu) ([#1250](https://github.com/nonebot/nonebot2/pull/1250))
- Plugin: Minecraft Server 聊天同步 [@yanyongyu](https://github.com/yanyongyu) ([#1245](https://github.com/nonebot/nonebot2/pull/1245))
- Plugin: 查询 ETH 合并日期 [@yanyongyu](https://github.com/yanyongyu) ([#1232](https://github.com/nonebot/nonebot2/pull/1232))
- Plugin: 星际战甲事件查询 [@yanyongyu](https://github.com/yanyongyu) ([#1220](https://github.com/nonebot/nonebot2/pull/1220))
- Plugin: 米游社辅助工具 [@yanyongyu](https://github.com/yanyongyu) ([#1218](https://github.com/nonebot/nonebot2/pull/1218))
- Plugin: 原神每日材料查询 [@yanyongyu](https://github.com/yanyongyu) ([#1216](https://github.com/nonebot/nonebot2/pull/1216))
- Plugin: MC_QQ_MCRcon [@yanyongyu](https://github.com/yanyongyu) ([#1211](https://github.com/nonebot/nonebot2/pull/1211))
- Plugin: 原神角色展柜查询 [@yanyongyu](https://github.com/yanyongyu) ([#1209](https://github.com/nonebot/nonebot2/pull/1209))
- Plugin: 修仙模拟器 [@yanyongyu](https://github.com/yanyongyu) ([#1202](https://github.com/nonebot/nonebot2/pull/1202))
- Plugin: 赛博浅草寺 [@yanyongyu](https://github.com/yanyongyu) ([#1206](https://github.com/nonebot/nonebot2/pull/1206))
- Plugin: 不背单词 [@yanyongyu](https://github.com/yanyongyu) ([#1204](https://github.com/nonebot/nonebot2/pull/1204))
- Plugin: 自识别 todo [@yanyongyu](https://github.com/yanyongyu) ([#1193](https://github.com/nonebot/nonebot2/pull/1193))
- Plugin: 雨课堂自动签到 [@yanyongyu](https://github.com/yanyongyu) ([#1189](https://github.com/nonebot/nonebot2/pull/1189))
- Plugin: 反馈及通知 [@yanyongyu](https://github.com/yanyongyu) ([#1187](https://github.com/nonebot/nonebot2/pull/1187))
- Plugin: MagiaDice 骰娘及 TRPGLOG [@yanyongyu](https://github.com/yanyongyu) ([#1185](https://github.com/nonebot/nonebot2/pull/1185))
- Plugin: 面麻小助手 [@yanyongyu](https://github.com/yanyongyu) ([#1191](https://github.com/nonebot/nonebot2/pull/1191))
- Plugin: 话痨排行榜 [@yanyongyu](https://github.com/yanyongyu) ([#1182](https://github.com/nonebot/nonebot2/pull/1182))
- Plugin: 保存群聊闪照 [@yanyongyu](https://github.com/yanyongyu) ([#1179](https://github.com/nonebot/nonebot2/pull/1179))
- Plugin: 课表查询 [@yanyongyu](https://github.com/yanyongyu) ([#1168](https://github.com/nonebot/nonebot2/pull/1168))
- Plugin: 业余无线电助手 [@yanyongyu](https://github.com/yanyongyu) ([#1173](https://github.com/nonebot/nonebot2/pull/1173))
- Plugin: NoneBot 树形帮助插件 [@yanyongyu](https://github.com/yanyongyu) ([#1177](https://github.com/nonebot/nonebot2/pull/1177))
- Plugin: 工作性价比 [@yanyongyu](https://github.com/yanyongyu) ([#1175](https://github.com/nonebot/nonebot2/pull/1175))
- Plugin: 娶群友 [@yanyongyu](https://github.com/yanyongyu) ([#1170](https://github.com/nonebot/nonebot2/pull/1170))
- Plugin: PixivBot [@yanyongyu](https://github.com/yanyongyu) ([#1165](https://github.com/nonebot/nonebot2/pull/1165))
- Plugin: 日韩中 VITS 模型原神拟声 [@yanyongyu](https://github.com/yanyongyu) ([#1162](https://github.com/nonebot/nonebot2/pull/1162))
- Plugin: 每日人品 [@yanyongyu](https://github.com/yanyongyu) ([#1156](https://github.com/nonebot/nonebot2/pull/1156))
- Plugin: nonebot-plugin-drawer [@yanyongyu](https://github.com/yanyongyu) ([#1146](https://github.com/nonebot/nonebot2/pull/1146))
- Plugin: 小游戏合集 [@yanyongyu](https://github.com/yanyongyu) ([#1150](https://github.com/nonebot/nonebot2/pull/1150))
- Plugin: 简易群管（带入群欢迎） [@yanyongyu](https://github.com/yanyongyu) ([#1142](https://github.com/nonebot/nonebot2/pull/1142))
- Plugin: wiki 条目搜索、获取简介 [@yanyongyu](https://github.com/yanyongyu) ([#1133](https://github.com/nonebot/nonebot2/pull/1133))
- Plugin: bangumi 搜索 [@yanyongyu](https://github.com/yanyongyu) ([#1137](https://github.com/nonebot/nonebot2/pull/1137))
- Plugin: 疫情小助手-频道版 [@yanyongyu](https://github.com/yanyongyu) ([#1131](https://github.com/nonebot/nonebot2/pull/1131))
- Plugin: MC_QQ 通信 [@yanyongyu](https://github.com/yanyongyu) ([#1127](https://github.com/nonebot/nonebot2/pull/1127))
- Plugin: BAWiki [@yanyongyu](https://github.com/yanyongyu) ([#1129](https://github.com/nonebot/nonebot2/pull/1129))

### 🍻 机器人发布

- Bot: IdhagnBot [@yanyongyu](https://github.com/yanyongyu) ([#1267](https://github.com/nonebot/nonebot2/pull/1267))
- Bot: LittlePaimon [@yanyongyu](https://github.com/yanyongyu) ([#1256](https://github.com/nonebot/nonebot2/pull/1256))
- Bot: GenshinUID [@yanyongyu](https://github.com/yanyongyu) ([#1226](https://github.com/nonebot/nonebot2/pull/1226))
- Bot: 小白机器人 [@yanyongyu](https://github.com/yanyongyu) ([#1224](https://github.com/nonebot/nonebot2/pull/1224))

### 🍻 适配器发布

- Adapter: GitHub [@yanyongyu](https://github.com/yanyongyu) ([#1297](https://github.com/nonebot/nonebot2/pull/1297))
- Adapter: Console [@yanyongyu](https://github.com/yanyongyu) ([#1213](https://github.com/nonebot/nonebot2/pull/1213))

## v2.0.0-beta.5

### 🚀 新功能

- Feature: on_x 支持 expire_time 参数 [@Dobiichi-Origami](https://github.com/Dobiichi-Origami) ([#1106](https://github.com/nonebot/nonebot2/pull/1106))
- Feature: 正向驱动器 startup/shutdown hook 支持同步函数 [@synodriver](https://github.com/synodriver) ([#1104](https://github.com/nonebot/nonebot2/pull/1104))

### 🐛 Bug 修复

- Fix: 修复插件父子关系识别错漏 [@yanyongyu](https://github.com/yanyongyu) ([#1121](https://github.com/nonebot/nonebot2/pull/1121))
- Fix: run post hook 应该处理 matcher.state [@AkiraXie](https://github.com/AkiraXie) ([#1119](https://github.com/nonebot/nonebot2/pull/1119))
- Fix: 修复 setuptools 未安装导致 ImportError [@yanyongyu](https://github.com/yanyongyu) ([#1116](https://github.com/nonebot/nonebot2/pull/1116))
- Fix: 修复 typing 中 T_RunPostProcessor 类型的注释描述不正确 [@A-kirami](https://github.com/A-kirami) ([#1057](https://github.com/nonebot/nonebot2/pull/1057))

### 📝 文档

- Docs: 添加 nonemoji 并更新开发指南 [@yanyongyu](https://github.com/yanyongyu) ([#1088](https://github.com/nonebot/nonebot2/pull/1088))
- Docs: 修复 event message 类型注释错误 [@yanyongyu](https://github.com/yanyongyu) ([#1079](https://github.com/nonebot/nonebot2/pull/1079))
- Docs: 修复旧 Vuepress 文档缓存问题 [@StarHeartHunt](https://github.com/StarHeartHunt) ([#1077](https://github.com/nonebot/nonebot2/pull/1077))
- Docs: 更新 Readme 贡献图片 [@yanyongyu](https://github.com/yanyongyu) ([#1074](https://github.com/nonebot/nonebot2/pull/1074))
- Docs: 注销旧 Vuepress 文档的 Service Worker [@StarHeartHunt](https://github.com/StarHeartHunt) ([#1073](https://github.com/nonebot/nonebot2/pull/1073))
- Docs: 修改 `权限控制` 一节中主动调用的错误 [@MingxuanGame](https://github.com/MingxuanGame) ([#1072](https://github.com/nonebot/nonebot2/pull/1072))

### 💫 杂项

- Bot: 修改剑网三 bot 信息 [@JustUndertaker](https://github.com/JustUndertaker) ([#1107](https://github.com/nonebot/nonebot2/pull/1107))

### 🍻 插件发布

- Plugin: 「能不能好好说话？」缩写翻译 [@yanyongyu](https://github.com/yanyongyu) ([#1118](https://github.com/nonebot/nonebot2/pull/1118))
- Plugin: 推送钩子 [@yanyongyu](https://github.com/yanyongyu) ([#1115](https://github.com/nonebot/nonebot2/pull/1115))
- Plugin: 易命令 [@yanyongyu](https://github.com/yanyongyu) ([#1111](https://github.com/nonebot/nonebot2/pull/1111))
- Plugin: 群昵称时间 [@yanyongyu](https://github.com/yanyongyu) ([#1109](https://github.com/nonebot/nonebot2/pull/1109))
- Plugin: 处理好友添加和群邀请 [@yanyongyu](https://github.com/yanyongyu) ([#1099](https://github.com/nonebot/nonebot2/pull/1099))
- Plugin: 明日方舟寻访记录分析 [@yanyongyu](https://github.com/yanyongyu) ([#1097](https://github.com/nonebot/nonebot2/pull/1097))
- Plugin: b 站视频每日推送 [@yanyongyu](https://github.com/yanyongyu) ([#1095](https://github.com/nonebot/nonebot2/pull/1095))
- Plugin: 自动回复（文 i）插件 [@yanyongyu](https://github.com/yanyongyu) ([#1090](https://github.com/nonebot/nonebot2/pull/1090))
- Plugin: ACC 计算工具 [@yanyongyu](https://github.com/yanyongyu) ([#1093](https://github.com/nonebot/nonebot2/pull/1093))
- Plugin: OSU 查分插件 [@yanyongyu](https://github.com/yanyongyu) ([#1082](https://github.com/nonebot/nonebot2/pull/1082))
- Plugin: 战地 1、5 战绩查询工具 [@yanyongyu](https://github.com/yanyongyu) ([#1087](https://github.com/nonebot/nonebot2/pull/1087))
- Plugin: 一起燚 xN 吧 [@yanyongyu](https://github.com/yanyongyu) ([#1085](https://github.com/nonebot/nonebot2/pull/1085))
- Plugin: 米游币商品自动兑换 [@yanyongyu](https://github.com/yanyongyu) ([#1076](https://github.com/nonebot/nonebot2/pull/1076))
- Plugin: 赛马 [@yanyongyu](https://github.com/yanyongyu) ([#1069](https://github.com/nonebot/nonebot2/pull/1069))
- Plugin: PicMenu [@yanyongyu](https://github.com/yanyongyu) ([#1071](https://github.com/nonebot/nonebot2/pull/1071))
- Plugin: nonebot-plugin-bread [@yanyongyu](https://github.com/yanyongyu) ([#1064](https://github.com/nonebot/nonebot2/pull/1064))
- Plugin: 黑白名单 [@yanyongyu](https://github.com/yanyongyu) ([#1061](https://github.com/nonebot/nonebot2/pull/1061))
- Plugin: BitTorrent [@yanyongyu](https://github.com/yanyongyu) ([#1059](https://github.com/nonebot/nonebot2/pull/1059))

### 🍻 机器人发布

- Bot: SkadiBot [@yanyongyu](https://github.com/yanyongyu) ([#1113](https://github.com/nonebot/nonebot2/pull/1113))
- Bot: 真宵 Bot [@yanyongyu](https://github.com/yanyongyu) ([#1103](https://github.com/nonebot/nonebot2/pull/1103))

## v2.0.0-beta.4

### 🚀 新功能

- Feature: 添加插件元信息定义 [@yanyongyu](https://github.com/yanyongyu) ([#1046](https://github.com/nonebot/nonebot2/pull/1046))
- Feature: 日志记录自动检测终端是否支持彩色 [@BlueGlassBlock](https://github.com/BlueGlassBlock) ([#1034](https://github.com/nonebot/nonebot2/pull/1034))
- Feature: 优化插件加载内部逻辑 [@yanyongyu](https://github.com/yanyongyu) ([#1011](https://github.com/nonebot/nonebot2/pull/1011))

### 🐛 Bug 修复

- Fix: 修复 MessageSegment 在有额外数据时报错 [@yanyongyu](https://github.com/yanyongyu) ([#1055](https://github.com/nonebot/nonebot2/pull/1055))
- Fix: 修复环境变量无法覆盖 dotenv 内配置项值 [@yanyongyu](https://github.com/yanyongyu) ([#1052](https://github.com/nonebot/nonebot2/pull/1052))
- Fix: 修复依赖注入 bot event 参数 union 校验失败 [@yanyongyu](https://github.com/yanyongyu) ([#1001](https://github.com/nonebot/nonebot2/pull/1001))

### 📝 文档

- Docs：添加文档排版规范 [@j1g5awi](https://github.com/j1g5awi) ([#1005](https://github.com/nonebot/nonebot2/pull/1005))
- Docs: 更新 require 样例 [@yanyongyu](https://github.com/yanyongyu) ([#996](https://github.com/nonebot/nonebot2/pull/996))
- Docs: 更新 README 中的 QQ 频道图标 [@mnixry](https://github.com/mnixry) ([#997](https://github.com/nonebot/nonebot2/pull/997))
- Docs: 调整跨插件访问文档 [@AkiraXie](https://github.com/AkiraXie) ([#993](https://github.com/nonebot/nonebot2/pull/993))

### 🍻 插件发布

- Plugin: 历史上的今天 [@yanyongyu](https://github.com/yanyongyu) ([#1049](https://github.com/nonebot/nonebot2/pull/1049))
- Plugin: smart_reply [@yanyongyu](https://github.com/yanyongyu) ([#1054](https://github.com/nonebot/nonebot2/pull/1054))
- Plugin: nonebot_plugin_setu4 [@yanyongyu](https://github.com/yanyongyu) ([#1051](https://github.com/nonebot/nonebot2/pull/1051))
- Plugin: 命令重启机器人 [@yanyongyu](https://github.com/yanyongyu) ([#1038](https://github.com/nonebot/nonebot2/pull/1038))
- Plugin: 青年大学习自动提交 [@yanyongyu](https://github.com/yanyongyu) ([#1036](https://github.com/nonebot/nonebot2/pull/1036))
- Plugin: 疫情小助手 [@yanyongyu](https://github.com/yanyongyu) ([#1033](https://github.com/nonebot/nonebot2/pull/1033))
- Plugin: 谁艾特我了 [@yanyongyu](https://github.com/yanyongyu) ([#1031](https://github.com/nonebot/nonebot2/pull/1031))
- Plugin: Hikari-战舰世界水表查询 [@yanyongyu](https://github.com/yanyongyu) ([#1025](https://github.com/nonebot/nonebot2/pull/1025))
- Plugin: Warframe 时间查询 [@yanyongyu](https://github.com/yanyongyu) ([#1023](https://github.com/nonebot/nonebot2/pull/1023))
- Plugin: imagetools [@yanyongyu](https://github.com/yanyongyu) ([#1021](https://github.com/nonebot/nonebot2/pull/1021))
- Plugin: 明日方舟工具箱 [@yanyongyu](https://github.com/yanyongyu) ([#1019](https://github.com/nonebot/nonebot2/pull/1019))
- Plugin: B 站视频伪分享卡片 [@yanyongyu](https://github.com/yanyongyu) ([#1014](https://github.com/nonebot/nonebot2/pull/1014))
- Plugin: TETRIS Stats [@yanyongyu](https://github.com/yanyongyu) ([#1009](https://github.com/nonebot/nonebot2/pull/1009))
- Plugin: 签到插件 [@yanyongyu](https://github.com/yanyongyu) ([#1007](https://github.com/nonebot/nonebot2/pull/1007))
- Plugin: 数据库连接插件 [@yanyongyu](https://github.com/yanyongyu) ([#995](https://github.com/nonebot/nonebot2/pull/995))
- Plugin: 百度翻译 [@yanyongyu](https://github.com/yanyongyu) ([#992](https://github.com/nonebot/nonebot2/pull/992))
- Plugin: MockingBird 语音 [@yanyongyu](https://github.com/yanyongyu) ([#989](https://github.com/nonebot/nonebot2/pull/989))

### 🍻 机器人发布

- Bot: nya_bot [@yanyongyu](https://github.com/yanyongyu) ([#1045](https://github.com/nonebot/nonebot2/pull/1045))
- Bot: LiteyukiBot-轻雪机器人 [@yanyongyu](https://github.com/yanyongyu) ([#1003](https://github.com/nonebot/nonebot2/pull/1003))

### 🍻 适配器发布

- Adapter: OneBot V12 [@yanyongyu](https://github.com/yanyongyu) ([#1027](https://github.com/nonebot/nonebot2/pull/1027))

## v2.0.0-beta.3

### 💥 破坏性变更

- Fix: 添加 export 方法 Deprecation 警告 [@yanyongyu](https://github.com/yanyongyu) ([#983](https://github.com/nonebot/nonebot2/pull/983))
- Feature: 支持 WebSocket 连接同时获取 str 或 bytes [@yanyongyu](https://github.com/yanyongyu) ([#962](https://github.com/nonebot/nonebot2/pull/962))

### 🚀 新功能

- Feature: 支持 WebSocket 连接同时获取 str 或 bytes [@yanyongyu](https://github.com/yanyongyu) ([#962](https://github.com/nonebot/nonebot2/pull/962))
- Feature: 添加 `CommandStart` 依赖注入参数 [@MeetWq](https://github.com/MeetWq) ([#915](https://github.com/nonebot/nonebot2/pull/915))
- Feature: 添加 Rule, Permission 反向位运算支持 [@yanyongyu](https://github.com/yanyongyu) ([#872](https://github.com/nonebot/nonebot2/pull/872))
- Feature: 新增文本完整匹配规则 [@A-kirami](https://github.com/A-kirami) ([#797](https://github.com/nonebot/nonebot2/pull/797))

### 🐛 Bug 修复

- Fix: 修复依赖注入默认值参数在 `__eq__` 被重写时报错的问题 [@yanyongyu](https://github.com/yanyongyu) ([#971](https://github.com/nonebot/nonebot2/pull/971))
- Fix: 修复`MessageTemplate`在没有格式化说明符时行为不正确的问题 [@mnixry](https://github.com/mnixry) ([#947](https://github.com/nonebot/nonebot2/pull/947))
- Fix: Bot Hook 没有捕获跳过异常 [@yanyongyu](https://github.com/yanyongyu) ([#905](https://github.com/nonebot/nonebot2/pull/905))
- Fix: 修复部分事件响应器参数类型中冗余的 Optional [@A-kirami](https://github.com/A-kirami) ([#904](https://github.com/nonebot/nonebot2/pull/904))
- Fix: 修复 event 类型检查会对类型进行自动转换 [@yanyongyu](https://github.com/yanyongyu) ([#876](https://github.com/nonebot/nonebot2/pull/876))
- Fix: 修复 `on_fullmatch` 返回类型错误 [@yanyongyu](https://github.com/yanyongyu) ([#815](https://github.com/nonebot/nonebot2/pull/815))
- Fix: 修复 DataclassEncoder 嵌套 encode 的问题 [@AkiraXie](https://github.com/AkiraXie) ([#812](https://github.com/nonebot/nonebot2/pull/812))

### 📝 文档

- Docs: 修复定时任务一节中的部分拼写错误 [@Nova-Noir](https://github.com/Nova-Noir) ([#982](https://github.com/nonebot/nonebot2/pull/982))
- Fix: 商店搜索失效 [@yanyongyu](https://github.com/yanyongyu) ([#978](https://github.com/nonebot/nonebot2/pull/978))
- Docs: 添加 QQ 频道链接 [@StarHeartHunt](https://github.com/StarHeartHunt) ([#961](https://github.com/nonebot/nonebot2/pull/961))
- Docs: 添加 nonebug 单元测试文档 [@MingxuanGame](https://github.com/MingxuanGame) ([#929](https://github.com/nonebot/nonebot2/pull/929))
- Docs: 添加 pm2 部署文档 [@evlic](https://github.com/evlic) ([#853](https://github.com/nonebot/nonebot2/pull/853))
- Docs: 更新 GitHub Action 部署文档 [@kexue-z](https://github.com/kexue-z) ([#937](https://github.com/nonebot/nonebot2/pull/937))
- Docs: 添加自定义匹配规则文档 [@yanyongyu](https://github.com/yanyongyu) ([#914](https://github.com/nonebot/nonebot2/pull/914))
- Docs: 修复适配器文档内商店链接 [@yanyongyu](https://github.com/yanyongyu) ([#861](https://github.com/nonebot/nonebot2/pull/861))
- Docs: tips for finding adapters' document link [@StarHeartHunt](https://github.com/StarHeartHunt) ([#860](https://github.com/nonebot/nonebot2/pull/860))
- Docs: 添加对 `fastapi_reload` 在 Windows 平台额外影响的说明 [@CherryGS](https://github.com/CherryGS) ([#830](https://github.com/nonebot/nonebot2/pull/830))
- Docs: 修复 ci/cd action 中错误的版本号 [@Bubbleioa](https://github.com/Bubbleioa) ([#819](https://github.com/nonebot/nonebot2/pull/819))
- Docs: 减小更新日志 toc 最大显示等级 [@yanyongyu](https://github.com/yanyongyu) ([#813](https://github.com/nonebot/nonebot2/pull/813))
- Docs: 修改议题模板中的错误链接 [@he0119](https://github.com/he0119) ([#807](https://github.com/nonebot/nonebot2/pull/807))
- Docs: 修改消息模板文档中错误的样例 [@mnixry](https://github.com/mnixry) ([#806](https://github.com/nonebot/nonebot2/pull/806))
- Docs: 更新贡献指南 [@yanyongyu](https://github.com/yanyongyu) ([#798](https://github.com/nonebot/nonebot2/pull/798))

### 💫 杂项

- Plugin: nonebot-plugin-chess 改名为 nonebot-plugin-boardgame [@MeetWq](https://github.com/MeetWq) ([#953](https://github.com/nonebot/nonebot2/pull/953))
- Plugin: 网易云无损音乐下载更改 [@kitUIN](https://github.com/kitUIN) ([#924](https://github.com/nonebot/nonebot2/pull/924))
- Docs: 移除商店中的过期插件 [@j1g5awi](https://github.com/j1g5awi) ([#902](https://github.com/nonebot/nonebot2/pull/902))
- CI: 修复发布机器人的意外错误 [@he0119](https://github.com/he0119) ([#892](https://github.com/nonebot/nonebot2/pull/892))
- Docs: 替换和移除部分已经失效的插件 [@MeetWq](https://github.com/MeetWq) ([#879](https://github.com/nonebot/nonebot2/pull/879))
- Docs: 添加 netlify 标签 [@yanyongyu](https://github.com/yanyongyu) ([#816](https://github.com/nonebot/nonebot2/pull/816))
- Fix: 修改错误的插件 PyPI 项目名称 [@Lancercmd](https://github.com/Lancercmd) ([#804](https://github.com/nonebot/nonebot2/pull/804))
- CI: 添加更新日志自动更新 action [@yanyongyu](https://github.com/yanyongyu) ([#799](https://github.com/nonebot/nonebot2/pull/799))

### 🍻 插件发布

- Plugin: imageutils [@yanyongyu](https://github.com/yanyongyu) ([#985](https://github.com/nonebot/nonebot2/pull/985))
- Plugin: 摸鱼日历 [@yanyongyu](https://github.com/yanyongyu) ([#980](https://github.com/nonebot/nonebot2/pull/980))
- Plugin: 走迷宫 [@yanyongyu](https://github.com/yanyongyu) ([#977](https://github.com/nonebot/nonebot2/pull/977))
- Plugin: 语录娱乐 [@yanyongyu](https://github.com/yanyongyu) ([#973](https://github.com/nonebot/nonebot2/pull/973))
- Plugin: 国内新冠疫情数据查询 [@yanyongyu](https://github.com/yanyongyu) ([#975](https://github.com/nonebot/nonebot2/pull/975))
- Plugin: nonebot_plugin_eventdone [@yanyongyu](https://github.com/yanyongyu) ([#966](https://github.com/nonebot/nonebot2/pull/966))
- Plugin: 幻影坦克图片合成 [@yanyongyu](https://github.com/yanyongyu) ([#968](https://github.com/nonebot/nonebot2/pull/968))
- Plugin: 合成字符画(GIF) [@yanyongyu](https://github.com/yanyongyu) ([#964](https://github.com/nonebot/nonebot2/pull/964))
- Plugin: 国际象棋 [@yanyongyu](https://github.com/yanyongyu) ([#957](https://github.com/nonebot/nonebot2/pull/957))
- Plugin: NoneBot2 文档搜索 [@yanyongyu](https://github.com/yanyongyu) ([#952](https://github.com/nonebot/nonebot2/pull/952))
- Plugin: 中国象棋 [@yanyongyu](https://github.com/yanyongyu) ([#949](https://github.com/nonebot/nonebot2/pull/949))
- Plugin: B 站视频封面提取 [@yanyongyu](https://github.com/yanyongyu) ([#946](https://github.com/nonebot/nonebot2/pull/946))
- Plugin: 一言 [@yanyongyu](https://github.com/yanyongyu) ([#944](https://github.com/nonebot/nonebot2/pull/944))
- Plugin: 答案之书 [@yanyongyu](https://github.com/yanyongyu) ([#942](https://github.com/nonebot/nonebot2/pull/942))
- Plugin: 支付宝到账语音 [@yanyongyu](https://github.com/yanyongyu) ([#940](https://github.com/nonebot/nonebot2/pull/940))
- Plugin: nonebot-plugin-dida [@yanyongyu](https://github.com/yanyongyu) ([#934](https://github.com/nonebot/nonebot2/pull/934))
- Plugin: 随机唐可可 [@yanyongyu](https://github.com/yanyongyu) ([#931](https://github.com/nonebot/nonebot2/pull/931))
- Plugin: splatoon2 新闻 [@yanyongyu](https://github.com/yanyongyu) ([#917](https://github.com/nonebot/nonebot2/pull/917))
- Plugin: nonebot_plugin_draw [@yanyongyu](https://github.com/yanyongyu) ([#910](https://github.com/nonebot/nonebot2/pull/910))
- Plugin: 扫雷游戏 [@yanyongyu](https://github.com/yanyongyu) ([#907](https://github.com/nonebot/nonebot2/pull/907))
- Plugin: 汉兜 Handle [@yanyongyu](https://github.com/yanyongyu) ([#899](https://github.com/nonebot/nonebot2/pull/899))
- Plugin: 多适配器帮助函数 [@yanyongyu](https://github.com/yanyongyu) ([#897](https://github.com/nonebot/nonebot2/pull/897))
- Plugin: 语句抽象化 [@yanyongyu](https://github.com/yanyongyu) ([#894](https://github.com/nonebot/nonebot2/pull/894))
- Plugin: 快速搜索 [@yanyongyu](https://github.com/yanyongyu) ([#889](https://github.com/nonebot/nonebot2/pull/889))
- Plugin: wordle 猜单词 [@yanyongyu](https://github.com/yanyongyu) ([#891](https://github.com/nonebot/nonebot2/pull/891))
- Plugin: MediaWiki 查询 [@yanyongyu](https://github.com/yanyongyu) ([#886](https://github.com/nonebot/nonebot2/pull/886))
- Plugin: HikariSearch [@yanyongyu](https://github.com/yanyongyu) ([#884](https://github.com/nonebot/nonebot2/pull/884))
- Plugin: 第二个 leetcode 查询插件 [@yanyongyu](https://github.com/yanyongyu) ([#882](https://github.com/nonebot/nonebot2/pull/882))
- Plugin: 成分姬 [@yanyongyu](https://github.com/yanyongyu) ([#878](https://github.com/nonebot/nonebot2/pull/878))
- Plugin: Arcaea 查分插件 [@yanyongyu](https://github.com/yanyongyu) ([#875](https://github.com/nonebot/nonebot2/pull/875))
- Plugin: QQ 自动同意好友申请 [@yanyongyu](https://github.com/yanyongyu) ([#871](https://github.com/nonebot/nonebot2/pull/871))
- Plugin: 21 点游戏插件 [@yanyongyu](https://github.com/yanyongyu) ([#865](https://github.com/nonebot/nonebot2/pull/865))
- Plugin: 色图生成 [@yanyongyu](https://github.com/yanyongyu) ([#863](https://github.com/nonebot/nonebot2/pull/863))
- Plugin: bilibili 通知插件 [@yanyongyu](https://github.com/yanyongyu) ([#859](https://github.com/nonebot/nonebot2/pull/859))
- Plugin: 订阅推送管理 [@yanyongyu](https://github.com/yanyongyu) ([#855](https://github.com/nonebot/nonebot2/pull/855))
- Plugin: 动漫新闻 [@yanyongyu](https://github.com/yanyongyu) ([#852](https://github.com/nonebot/nonebot2/pull/852))
- Plugin: 游戏王卡查 [@yanyongyu](https://github.com/yanyongyu) ([#846](https://github.com/nonebot/nonebot2/pull/846))
- Plugin: 二维码识别与发送 [@yanyongyu](https://github.com/yanyongyu) ([#843](https://github.com/nonebot/nonebot2/pull/843))
- Plugin: mockingbird [@yanyongyu](https://github.com/yanyongyu) ([#841](https://github.com/nonebot/nonebot2/pull/841))
- Plugin: QQ 自动续火花 [@yanyongyu](https://github.com/yanyongyu) ([#839](https://github.com/nonebot/nonebot2/pull/839))
- Plugin: 每日一句 [@yanyongyu](https://github.com/yanyongyu) ([#832](https://github.com/nonebot/nonebot2/pull/832))
- Plugin: 原神抽卡记录分析 [@yanyongyu](https://github.com/yanyongyu) ([#829](https://github.com/nonebot/nonebot2/pull/829))
- Plugin: YetAnotherPicSearch [@yanyongyu](https://github.com/yanyongyu) ([#825](https://github.com/nonebot/nonebot2/pull/825))
- Plugin: 60s 读世界小插件 [@yanyongyu](https://github.com/yanyongyu) ([#810](https://github.com/nonebot/nonebot2/pull/810))
- Plugin: pixiv.net p 站查询图片 [@yanyongyu](https://github.com/yanyongyu) ([#803](https://github.com/nonebot/nonebot2/pull/803))

### 🍻 机器人发布

- Bot: 屑岛风 Bot [@yanyongyu](https://github.com/yanyongyu) ([#987](https://github.com/nonebot/nonebot2/pull/987))
- Bot: ShigureBot [@yanyongyu](https://github.com/yanyongyu) ([#959](https://github.com/nonebot/nonebot2/pull/959))
- Bot: Inkar Suki [@yanyongyu](https://github.com/yanyongyu) ([#955](https://github.com/nonebot/nonebot2/pull/955))

## v2.0.0-beta.2

- 修复 `receive`, `got` 在参数为空消息时依旧会反复询问
- 修复文档商店分页显示错误
- 修复插件导入失败时，依然存在于已导入插件列表中
- 移除 `state` 依赖注入所需的默认值 `State()`
- 增加 `fastapi` 配置项：是否将适配器路由包含在 schema 中
- 修改 `load_builtin_plugins` 函数，使其能够支持加载多个内置插件
- 新增 `load_builtin_plugin` 函数，用于加载单个内置插件
- 修改 `Message` 和 `MessageSegment` 类，完善 typing，转移 Mapping 构建支持至 pydantic validate
- 调整项目结构，分离内部定义与用户接口
- 新增 Bot 连接事件钩子 (如 `driver.on_bot_connect` ) 的依赖注入

## v2.0.0-beta.1

- 新增 `MessageTemplate` 对于 `str` 普通模板的支持
- 移除插件加载的 `NameSpace` 模式
- 修改 toml 加载插件时的键名为 `tool.nonebot` 以符合规范
- 新增 Handler 依赖注入支持，同步/异步支持
- 统一 `Processor`, `Rule`, `Permission`, `Processor` 使用 `Handler`
- 修改内置 `Rule`, `Permission` 如 `startswith`, `command` 等使用 class 实现
- 更换文档框架 (docusaurus) 以及主题 (docusaurus-theme-nonepress)
- 移除 Matcher `state_factory` 支持

## v2.0.0a16

- 新增 `MessageTemplate` 可用于 `Message` 的模板生成
- 新增 `matcher.got` `matcher.send` `matcher.pause` `matcher.reject` `matcher.finish` 支持 `MessageTemplate`
- 移除 `matcher.got` 原本的 `state format` 支持，由 `MessageTemplate` template 替代
- `adapter` 基类拆分为单独文件
- 修复 `fastapi` Driver Websocket 未能正确提供请求头部
- 新增 `fastapi` Driver 更多的 uvicorn 相关配置项
- 新增 `quart` Driver 更多的 uvicorn 相关配置项
- 修复 `endswith` Rule 错误的正则匹配
- 修复 `cqhttp` Adapter `image`, `record`, `video` 对 `BytesIO` 不正常的读取操作

## v2.0.0a15

- 修复 `fastapi` Driver 未能正确进行 reconnect
- 修复 `MessageSegment` 错误的 Mapping 映射

## v2.0.0a14

- 修改日志等级，支持输出等级自定义
- 修复日志输出模块名错误
- 修改 `Matcher` 属性 `module` 类型
- 新增 `Matcher` 属性 `plugin_name` `module_name` `module_prefix`
- 移除 `bot.call_api` 参数 `self_id` 切换机器人支持
- 修复 `type_updater` `permission_updater` 未传递的错误
- 修复 `type_updater` `permission_updater` 参数 `state` 错误
- 修复使用 `state_factory` 后导致无法在 session 内传递 `state`
- 重构 `Driver` 及连接信息抽象
- 新增正向 Driver(Client) 支持
- 新增 `aiohttp` 正向 Driver
- `fastapi` Driver 新增正向支持

## v2.0.0a13.post1

- 分离 `handler` 与 `matcher`
- 修复 `cqhttp` secret 校验出错
- 修复 `pydantic 1.8` 导致的 `alias` 问题
- 修改 `cqhttp` `ding` `session id`，不再允许跨群
- 修改 `shell_command` 存储 message
- 修复 `cqhttp` 检查 reply 失败退出
- 新增 `call_api` hook 接口
- 优化 `import hook`

## v2.0.0a11

- 修改 `nonebot` 项目结构，分离所有 `adapter`
- 修改插件加载逻辑，使用 `import hook` (PEP 302)
- 新增插件加载方式: `json`, `toml`
- 适配 `pydantic` ~1.8
- 移除 4 种内置事件类型限制，允许自定义事件类型
- 新增会话权限更新自定义，会话中断时更新权限以做到多人会话

## v2.0.0a10

- 新增 `Quart Driver` 支持
- 修复 `mirai` 协议适配命令处理以及消息转义

## v2.0.0a9

- 修复 `Message` 消息为 `None` 时的处理错误
- 修复 `Message.extract_plain_text` 返回为转义字符串的问题
- 修复命令处理错误地删除了后续空格
- 增加好友添加和加群请求事件 `approve`, `reject` 方法
- 新增 `mirai-api-http` 协议适配
- 修复 rule 运行时 state 覆盖问题，隔离 state
- 新增 `shell like command` 支持

## v2.0.0a8

- 修改 typing 类型注释
- 修改 event 基类接口
- 修复部分非法 CQ 码被识别导致报错
- 修复非 text 类型 CQ 码 data 未进行去转义
- 修复内置插件未进行去转义，修改内置插件为 cqhttp 定制
- 修复 `load_plugins` 加载不合法的包时出现 `spec` 为 `None` 的问题
- 出于**CQ 码安全性考虑**，使用 cqhttp 的 `bot.send` 或者 `matcher.send` 时默认对字符串进行转义
- 移动 cqhttp 相关 `Permission` 至 `nonebot.adapters.cqhttp` 包内

## v2.0.0a7

- 修复 cqhttp 检查 to me 时出现 IndexError
- 修复已失效的事件响应器仍会运行一次的 bug
- 修改 cqhttp 检查 reply 时未去除后续 at 以及空格
- 添加 get_plugin 获取插件函数
- 添加插件 export, require 方法
- **移除**内置 apscheduler 定时任务支持
- **移除**内置协议适配默认加载
- 新增**钉钉**协议适配
- 移除原有共享型 `MatcherGroup` 改为默认型 `MatcherGroup`

## v2.0.0a6

- 修复 block 失效问题 (hotfix)

## v2.0.0a5

- 更新插件指南文档
- 修复临时事件响应器运行后删除造成的多次响应问题
