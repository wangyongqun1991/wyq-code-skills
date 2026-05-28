---
name: logistics-saas-design
description: "This skill should be used when users need to design or implement logistics SaaS UI interfaces following the Transix design system. It provides comprehensive guidance on color schemes (purple gradient theme), typography (Inter Display), component styles, layout structures, and visual hierarchy for modern logistics management platforms. Use this skill for creating landing pages, dashboards, data visualization components, pricing modules, and responsive designs for logistics software."
---

# 物流 SaaS UI 界面设计 Skill

## 概述

本 skill 提供完整的物流 SaaS 平台 UI/UX 设计规范，基于 Transix 物流管理平台设计系统。包含配色方案、字体规范、组件样式、布局结构、数据可视化等完整设计指南，适用于现代物流管理软件的前端开发与设计。

**适用场景：**
-  **Landing Page 设计** - 产品首页、营销页面
-  **Dashboard 看板** - 数据统计、图表展示
- 📱 **响应式适配** - 桌面端与移动端设计
- 🎯 **组件库构建** - 按钮、卡片、表单等 UI 组件
- 📈 **数据可视化** - 折线图、柱状图、环形图等
- 💰 **定价模块** - 价格展示、套餐选择

## 核心设计理念

### 1. 现代化视觉语言
- 使用渐变效果营造科技感
- 圆角设计增强亲和力
- 充足的留白提升可读性
- 层次分明的信息架构

### 2. 数据驱动设计
- 强调数据可视化和统计展示
- 大号数字突出关键指标
- 多种图表类型展示业务数据
- 实时更新的数据反馈

### 3. 品牌一致性
- 统一的紫色主题贯穿全局
- 一致的组件样式和交互
- 清晰的视觉层次体系
- 跨设备体验的一致性

## 设计规范详解

### 一、配色方案（Color System）

#### 主色调 - 紫色渐变系列
```css
/* 主色 - 紫色渐变 */
--primary-gradient-start: #8B5CF6;    /* 浅紫 */
--primary-gradient-end: #6D28D9;      /* 深紫 */
--primary-solid: #7C3AED;             /* 纯紫 */

/* 应用场景 */
- 主要按钮背景
- 装饰性圆形元素
- 高亮状态指示
- CTA（Call-to-Action）区域
```

#### 辅助色系
```css
/* 橙色/黄色系 - 强调色 */
--accent-orange: #F59E0B;
--accent-yellow: #FBBF24;

/* 蓝色系 - 数据展示 */
--data-blue-light: #60A5FA;
--data-blue-medium: #3B82F6;
--data-blue-dark: #2563EB;

/* 中性色系 */
--neutral-white: #FFFFFF;
--neutral-gray-50: #F9FAFB;
--neutral-gray-100: #F3F4F6;
--neutral-gray-200: #E5E7EB;
--neutral-gray-300: #D1D5DB;
--neutral-gray-500: #6B7280;
--neutral-gray-700: #374151;
--neutral-gray-900: #111827;
```

#### 渐变色应用示例
```css
/* 紫色渐变背景 */
.gradient-purple {
  background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
}

/* 多色数据渐变 */
.gradient-data {
  background: linear-gradient(90deg, 
    #8B5CF6 0%, 
    #F59E0B 50%, 
    #60A5FA 100%
  );
}
```

### 二、字体规范（Typography）

#### 主字体家族
```css
/* 主字体：Inter Display */
font-family: 'Inter Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* 特点 */
- 现代无衬线字体
- 优秀的数字显示效果
- 多字重支持（Regular, Medium, SemiBold, Bold）
- 适合数据密集型界面
```

#### 字号层级体系
```css
/* 标题层级 */
h1: 48px / 56px line-height   /* Hero Section 主标题 */
h2: 36px / 44px line-height   /* 章节标题 */
h3: 24px / 32px line-height   /* 子标题 */
h4: 20px / 28px line-height   /* 小标题 */

/* 正文层级 */
body-large: 18px / 28px       /* 重要文本 */
body-base: 16px / 24px        /* 标准正文 */
body-small: 14px / 20px       /* 辅助说明 */
caption: 12px / 16px          /* 标签、注释 */

/* 数据展示 */
display-xl: 64px / 72px       /* 超大数字（如：6220）*/
display-lg: 48px / 56px       /* 大数字（如：5.0M）*/
display-md: 36px / 44px       /* 中等数字（如：82.08）*/
```

#### 字重使用规范
```css
/* Regular (400) */
- 正文内容
- 次要信息

/* Medium (500) */
- 导航菜单
- 按钮文字
- 表格表头

/* SemiBold (600) */
- 小标题
- 强调文本
- 数据标签

/* Bold (700) */
- 大标题
- 关键数字
- CTA 按钮
```

### 三、间距系统（Spacing System）

遵循 8px 网格系统，确保视觉节奏一致。

```css
/* 基础间距单位 */
--spacing-1: 4px;
--spacing-2: 8px;
--spacing-3: 12px;
--spacing-4: 16px;
--spacing-5: 24px;
--spacing-6: 32px;
--spacing-8: 48px;
--spacing-10: 64px;
--spacing-12: 96px;
--spacing-16: 128px;

/* 应用场景 */
- 元素内边距：spacing-2 ~ spacing-4
- 组件间距：spacing-4 ~ spacing-6
- 区块间距：spacing-8 ~ spacing-12
- 页面级间距：spacing-12 ~ spacing-16
```

### 四、圆角规范（Border Radius）

```css
/* 小圆角 */
--radius-sm: 4px;   /* 输入框、小按钮 */

/* 中圆角 */
--radius-md: 8px;   /* 卡片、标准按钮 */

/* 大圆角 */
--radius-lg: 12px;  /* 大型卡片、模态框 */

/* 全圆角 */
--radius-full: 9999px; /* 头像、徽章、胶囊按钮 */
```

### 五、阴影效果（Shadows）

```css
/* 轻微阴影 */
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);

/* 标准阴影 */
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
              0 2px 4px -1px rgba(0, 0, 0, 0.06);

/* 强烈阴影 */
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 
              0 4px 6px -2px rgba(0, 0, 0, 0.05);

/* 悬浮阴影 */
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 
              0 10px 10px -5px rgba(0, 0, 0, 0.04);
```

## 组件设计规范

### 1. 按钮（Buttons）

#### 主要按钮（Primary Button）
```css
.btn-primary {
  background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
  color: #FFFFFF;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(139, 92, 246, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
}
```

#### 次要按钮（Secondary Button）
```css
.btn-secondary {
  background: #FFFFFF;
  color: #7C3AED;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  border: 2px solid #7C3AED;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: #F3F0FF;
}
```

#### 幽灵按钮（Ghost Button）
```css
.btn-ghost {
  background: transparent;
  color: #7C3AED;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 16px;
  border: none;
  cursor: pointer;
}

.btn-ghost:hover {
  background: rgba(124, 58, 237, 0.1);
}
```

### 2. 卡片（Cards）

#### 标准卡片
```css
.card {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}
```

#### 数据卡片
```css
.data-card {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 20px;
  border-left: 4px solid #8B5CF6;
}

.data-card .label {
  font-size: 14px;
  color: #6B7280;
  margin-bottom: 8px;
}

.data-card .value {
  font-size: 36px;
  font-weight: 700;
  color: #111827;
  font-family: 'Inter Display', sans-serif;
}
```

#### 功能特性卡片
```css
.feature-card {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 32px;
  text-align: center;
  border: 1px solid #E5E7EB;
}

.feature-card .icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}
```

### 3. 导航栏（Navigation Bar）

```css
.navbar {
  background: #FFFFFF;
  height: 72px;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-logo {
  font-size: 24px;
  font-weight: 700;
  color: #7C3AED;
}

.navbar-menu {
  display: flex;
  gap: 32px;
}

.navbar-item {
  font-size: 16px;
  color: #374151;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s ease;
}

.navbar-item:hover {
  color: #7C3AED;
}
```

### 4. 数据展示组件

#### 大号数字显示
```css
.stat-number {
  font-size: 64px;
  font-weight: 700;
  color: #111827;
  font-family: 'Inter Display', sans-serif;
  line-height: 1;
  letter-spacing: -0.02em;
}

.stat-label {
  font-size: 14px;
  color: #6B7280;
  margin-top: 8px;
  font-weight: 500;
}
```

#### 数据标签
```css
.data-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  background: #F3F0FF;
  color: #7C3AED;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 600;
}
```

### 5. 定价卡片（Pricing Card）

```css
.pricing-card {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 40px 32px;
  text-align: center;
  border: 2px solid #E5E7EB;
  position: relative;
  overflow: hidden;
}

.pricing-card.featured {
  border-color: #8B5CF6;
  background: linear-gradient(to bottom, #F3F0FF 0%, #FFFFFF 100%);
}

.pricing-card .price {
  font-size: 48px;
  font-weight: 700;
  color: #111827;
  font-family: 'Inter Display', sans-serif;
}

.pricing-card .period {
  font-size: 16px;
  color: #6B7280;
}

.pricing-card .feature-list {
  list-style: none;
  padding: 0;
  margin: 32px 0;
  text-align: left;
}

.pricing-card .feature-item {
  padding: 8px 0;
  color: #374151;
  display: flex;
  align-items: center;
  gap: 12px;
}
```

## 布局结构规范

### 1. Hero Section（顶部横幅）

```html
<!-- Hero Section 结构 -->
<section class="hero">
  <div class="container">
    <div class="hero-content">
      <h1 class="hero-title">
        POWERING LOGISTICS<br/>
        TEAMS ACROSS GLOBAL<br/>
        SUPPLY CHAINS
      </h1>
      <p class="hero-subtitle">
        BUILT FOR THE FUTURE OF LOGISTICS
      </p>
      <div class="hero-cta">
        <button class="btn-primary">Get Started</button>
        <button class="btn-secondary">Learn More</button>
      </div>
      <div class="hero-stats">
        <div class="stat-item">
          <span class="stat-number">6,220</span>
          <span class="stat-label">Active Users</span>
        </div>
      </div>
    </div>
    <div class="hero-visual">
      <!-- 装饰性圆形渐变元素 -->
      <div class="gradient-circle"></div>
    </div>
  </div>
</section>
```

### 2. Dashboard Layout（看板布局）

```css
.dashboard {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 100vh;
}

.sidebar {
  background: #FFFFFF;
  border-right: 1px solid #E5E7EB;
  padding: 24px;
}

.main-content {
  padding: 32px;
  background: #F9FAFB;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}
```

### 3. 响应式断点

```css
/* 移动优先响应式设计 */

/* 超小屏幕 */
@media (max-width: 640px) {
  .container {
    padding: 0 16px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .charts-section {
    grid-template-columns: 1fr;
  }
}

/* 小屏幕 */
@media (min-width: 641px) and (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 大屏幕 */
@media (min-width: 1025px) {
  .container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 32px;
  }
}
```

## 图标风格规范

### 线性图标（Line Icons）
- 线条粗细：2px
- 统一颜色：当前文本颜色或主题色
- 尺寸：16px、24px、32px、48px
- 风格：简约、清晰、一致

### 填充图标（Filled Icons）
- 用于重要操作和状态指示
- 使用主题色填充
- 保持与线性图标相同的轮廓

### 图标使用场景
```css
/* 导航图标 */
.nav-icon {
  width: 24px;
  height: 24px;
  stroke-width: 2;
  color: #6B7280;
}

/* 功能图标 */
.feature-icon {
  width: 32px;
  height: 32px;
  stroke-width: 2;
  color: #7C3AED;
}

/* 大图标 */
.hero-icon {
  width: 48px;
  height: 48px;
  stroke-width: 2;
  color: #FFFFFF;
}
```

## 数据可视化规范

### 1. 图表类型选择

- **折线图**：趋势分析、时间序列数据
- **柱状图**：对比分析、分类数据
- **环形图**：占比分析、构成比例
- **面积图**：累积数据、流量变化
- **散点图**：相关性分析

### 2. 图表配色

```css
/* 数据系列颜色 */
--chart-color-1: #8B5CF6;  /* 紫色 */
--chart-color-2: #F59E0B;  /* 橙色 */
--chart-color-3: #60A5FA;  /* 蓝色 */
--chart-color-4: #10B981;  /* 绿色 */
--chart-color-5: #EF4444;  /* 红色 */
```

### 3. 图表样式

```css
.chart-container {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}

.chart-legend {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #6B7280;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}
```

## 工作流程

### 1. 需求分析阶段

当用户提出物流 SaaS 界面设计需求时：

1. **明确设计目标**
   - 确定页面类型（Landing Page、Dashboard、功能页等）
   - 了解核心功能和数据展示需求
   - 确认目标用户群体

2. **收集设计素材**
   - 参考 `references/design_assets/` 中的截图和设计稿
   - 提取配色、字体、组件样式等规范
   - 确认响应式要求

### 2. 设计实现阶段

#### 步骤 1：建立基础样式
```css
/* 1. 定义 CSS 变量 */
:root {
  /* 配色 */
  --primary-gradient-start: #8B5CF6;
  --primary-gradient-end: #6D28D9;
  /* ... 其他变量 */
  
  /* 字体 */
  --font-primary: 'Inter Display', sans-serif;
  
  /* 间距 */
  --spacing-4: 16px;
  /* ... 其他间距 */
}

/* 2. 设置全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-primary);
  color: var(--neutral-gray-900);
  background: var(--neutral-gray-50);
  line-height: 1.5;
}
```

#### 步骤 2：构建页面结构
根据页面类型选择合适的布局模板：
- Landing Page → Hero + Features + Pricing + CTA
- Dashboard → Sidebar + Stats Grid + Charts
- 功能页 → Header + Content + Footer

#### 步骤 3：应用组件样式
使用预定义的组件类：
- `.btn-primary`、`.btn-secondary` 等按钮
- `.card`、`.data-card` 等卡片
- `.navbar` 导航栏
- `.stat-number` 数据展示

#### 步骤 4：添加响应式适配
使用媒体查询确保多设备兼容：
- 移动端（< 640px）
- 平板端（641px - 1024px）
- 桌面端（> 1024px）

### 3. 质量检查阶段

完成设计后，验证以下要点：

- [ ] 配色符合紫色主题规范
- [ ] 字体使用 Inter Display 或等效字体
- [ ] 间距遵循 8px 网格系统
- [ ] 圆角统一（8px/12px/全圆角）
- [ ] 按钮有悬停和激活状态
- [ ] 卡片有适当的阴影效果
- [ ] 响应式断点正确应用
- [ ] 数据可视化清晰易读
- [ ] 无障碍访问考虑（对比度、键盘导航）

## 最佳实践

### 1. 视觉层次建立

```css
/* 通过大小、颜色、间距建立层次 */
.primary-info {
  font-size: 36px;
  font-weight: 700;
  color: #111827;
}

.secondary-info {
  font-size: 16px;
  font-weight: 500;
  color: #6B7280;
}

.tertiary-info {
  font-size: 14px;
  font-weight: 400;
  color: #9CA3AF;
}
```

### 2. 渐变效果使用原则

- **适度使用**：避免过度使用渐变导致视觉疲劳
- **方向一致**：通常使用 135° 或 90° 渐变方向
- **对比度足够**：确保渐变背景上的文字可读
- **性能优化**：使用 CSS 渐变而非图片

### 3. 数据展示技巧

- **突出关键数字**：使用大号字体和高对比度
- **提供上下文**：每个数字都应有明确的标签
- **可视化趋势**：使用图表展示变化趋势
- **实时更新**：对于动态数据，提供刷新机制

### 4. 移动端适配策略

- **触控友好**：按钮最小 44px × 44px
- **简化导航**：使用汉堡菜单或底部导航
- **优化加载**：减少首屏资源体积
- **手势支持**：支持滑动、缩放等手势

## 常见问题排查

### 问题 1：渐变效果不显示

**原因**：浏览器不支持或 CSS 语法错误

**解决方案**：
```css
/* 添加浏览器前缀 */
.gradient {
  background: -webkit-linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
  background: -moz-linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
  background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
}
```

### 问题 2：字体加载失败

**原因**：Inter Display 字体未正确引入

**解决方案**：
```html
<!-- Google Fonts 引入 -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- 或使用本地字体文件 -->
@font-face {
  font-family: 'Inter Display';
  src: url('/fonts/Inter-Display.woff2') format('woff2');
}
```

### 问题 3：响应式布局错乱

**原因**：媒体查询断点不正确或 Flexbox/Grid 配置错误

**解决方案**：
- 检查媒体查询的 min/max-width 值
- 使用 `flex-wrap: wrap` 允许换行
- 为 Grid 设置 `auto-fit` 和 `minmax()`

### 问题 4：阴影效果过重

**原因**：阴影参数设置过大

**解决方案**：
```css
/* 减轻阴影 */
.card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
```

## 参考资料

- **原始设计来源**：[Transix Logistics SaaS - Behance](https://www.behance.net/gallery/249758629/Transix-Logistics-SaaS-Landing-Page-UI-UX-Design)
- **字体资源**：[Inter Font Family](https://rsms.me/inter/)
- **图标库推荐**：[Heroicons](https://heroicons.com/)、[Lucide Icons](https://lucide.dev/)
- **色彩工具**：[Coolors](https://coolors.co/)、[Adobe Color](https://color.adobe.com/)
- **详细设计素材**：`references/design_assets/` 目录中的截图和规范文档

## 附录：快速参考卡

### 常用颜色速查
| 用途 | 颜色值 | 示例 |
|------|--------|------|
| 主色渐变起点 | #8B5CF6 | 按钮、装饰 |
| 主色渐变终点 | #6D28D9 | 按钮、装饰 |
| 强调色 | #F59E0B | 数据高亮 |
| 数据蓝 | #60A5FA | 图表 |
| 文字深色 | #111827 | 标题 |
| 文字浅色 | #6B7280 | 正文 |
| 背景灰 | #F9FAFB | 页面背景 |

### 常用字号速查
| 用途 | 字号 | 字重 |
|------|------|------|
| Hero 标题 | 48px | 700 |
| 章节标题 | 36px | 700 |
| 大数字 | 64px | 700 |
| 正文 | 16px | 400 |
| 小字 | 14px | 400 |

### 常用间距速查
| 用途 | 间距值 |
|------|--------|
| 元素内边距 | 16px - 24px |
| 组件间距 | 24px - 32px |
| 区块间距 | 48px - 96px |

---

**版本**：v1.0  
**最后更新**：2026-05-28  
**维护者**：wyqCode Skills Team
