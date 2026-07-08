# Design Tokens → rx.theme() 對應

> 把 ui-ux-pro-max 出的 design tokens 套到 Reflex app

---

## 📐 rx.theme() 結構

```python
import reflex as rx

theme = {
    "colors": {
        # 顏色 token
    },
    "spacing": {
        # spacing scale
    },
    "font_sizes": {
        # typography scale
    },
    "fonts": {
        # font family
    },
    "sizes": {
        # 寬高
    },
    "radii": {
        # border radius
    },
    "shadows": {
        # shadow
    },
    "breakpoints": {
        # 響應式
    },
}

app = rx.App(theme=rx.theme(theme))
```

> 完整 schema：https://reflex.dev/docs/styling/theming

---

## 🎨 Colors 對應

### ui-ux-pro-max tokens

```json
{
  "primary": "#3B82F6",
  "primary_hover": "#2563EB",
  "primary_active": "#1D4ED8",
  "secondary": "#10B981",
  "background": "#FFFFFF",
  "surface": "#F9FAFB",
  "text_primary": "#1F2937",
  "text_secondary": "#6B7280",
  "border": "#E5E7EB",
  "error": "#EF4444",
  "warning": "#F59E0B",
  "success": "#10B981",
  "info": "#3B82F6"
}
```

### Reflex theme

```python
theme = {
    "colors": {
        "primary": "#3B82F6",
        "primary_hover": "#2563EB",
        "primary_active": "#1D4ED8",
        "secondary": "#10B981",
        "background": "#FFFFFF",
        "surface": "#F9FAFB",
        "text_primary": "#1F2937",
        "text_secondary": "#6B7280",
        "border": "#E5E7EB",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "success": "#10B981",
        "info": "#3B82F6",
    }
}

app = rx.App(theme=rx.theme(theme))
```

使用：
```python
rx.button("Click me", color="primary", bg="surface")
```

---

## 📏 Spacing 對應

### ui-ux-pro-max

```json
{
  "xs": "4px",
  "sm": "8px",
  "md": "16px",
  "lg": "24px",
  "xl": "32px",
  "2xl": "48px"
}
```

### Reflex（用 1-9 數字對應）

```python
theme = {
    "spacing": {
        "1": "4px",   # xs
        "2": "8px",   # sm
        "3": "16px",  # md
        "4": "24px",  # lg
        "5": "32px",  # xl
        "6": "48px",  # 2xl
    }
}
```

使用：
```python
rx.box(padding="3", margin="2")  # 16px / 8px
```

---

## 🔤 Typography 對應

### ui-ux-pro-max

```json
{
  "h1": "32px / 40px / bold",
  "h2": "24px / 32px / bold",
  "h3": "20px / 28px / semibold",
  "body": "16px / 24px / normal",
  "caption": "12px / 16px / normal"
}
```

### Reflex

```python
theme = {
    "font_sizes": {
        "h1": "2rem",    # 32px
        "h2": "1.5rem",  # 24px
        "h3": "1.25rem", # 20px
        "body": "1rem",  # 16px
        "caption": "0.75rem",  # 12px
    },
    "fonts": {
        "heading": "Inter, system-ui, sans-serif",
        "body": "Inter, system-ui, sans-serif",
        "mono": "JetBrains Mono, monospace",
    },
    "line_heights": {
        "tight": "1.25",
        "normal": "1.5",
        "relaxed": "1.75",
    },
    "font_weights": {
        "normal": "400",
        "medium": "500",
        "semibold": "600",
        "bold": "700",
    },
}
```

使用：
```python
rx.heading("Title", font_size="h1", font_weight="bold", line_height="tight")
```

---

## 🔘 Border Radius 對應

### ui-ux-pro-max

```json
{
  "sm": "4px",
  "md": "8px",
  "lg": "12px",
  "xl": "16px",
  "full": "9999px"
}
```

### Reflex

```python
theme = {
    "radii": {
        "sm": "4px",
        "md": "8px",
        "lg": "12px",
        "xl": "16px",
        "full": "9999px",
    }
}
```

使用：
```python
rx.button("Click", border_radius="md")
```

---

## 🌑 Shadow 對應

```python
theme = {
    "shadows": {
        "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
        "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
    }
}
```

使用：
```python
rx.box(box_shadow="md", padding="4")
```

---

## 📱 Breakpoints 對應

```python
theme = {
    "breakpoints": {
        "sm": "640px",
        "md": "768px",
        "lg": "1024px",
        "xl": "1280px",
    }
}
```

使用（Reflex 0.9+）：
```python
rx.box(
    width="100%",
    width=rx.breakpoints(md="50%", lg="33%"),  # md 以上 50%, lg 以上 33%
)
```

---

## 🌓 Dark Mode

如果 ui-ux-pro-max 給 dark mode tokens：

```python
theme = {
    "colors": {
        "primary": "#3B82F6",
        # ... light mode
    }
}

# Dark mode (Reflex 0.9+)
dark_theme = {
    "colors": {
        "primary": "#60A5FA",
        "background": "#0F172A",
        "surface": "#1E293B",
        "text_primary": "#F1F5F9",
        "text_secondary": "#94A3B8",
        "border": "#334155",
    }
}

app = rx.App(
    theme=rx.theme(theme),
    # dark_theme=rx.theme(dark_theme),  # 0.9+ 支援
)
```

---

## 🔄 完整對應範例

ui-ux-pro-max 給：
```json
{
  "colors": {
    "primary": "#3B82F6",
    "background": "#FFFFFF",
    "text": "#1F2937"
  },
  "spacing": {
    "sm": "8px",
    "md": "16px"
  },
  "fontSizes": {
    "h1": "32px",
    "body": "16px"
  }
}
```

對應的 `rxconfig.py`：
```python
import reflex as rx

config = rx.Config(
    app_name="my_app",
    theme=rx.theme({
        "colors": {
            "primary": "#3B82F6",
            "background": "#FFFFFF",
            "text": "#1F2937",
        },
        "spacing": {
            "1": "4px",
            "2": "8px",
            "3": "16px",
        },
        "font_sizes": {
            "h1": "2rem",
            "body": "1rem",
        },
    })
)
```

---

## ⚠️ 注意事項

### 1. Reflex 0.8 vs 0.9 差異
- 0.8：`rx.theme()` 在 `rxconfig.py` 設
- 0.9：`rx.App(theme=...)` 在 app 設

### 2. 顏色命名轉換
- JS 用 kebab-case：`primary-hover`
- Python 用 snake_case：`primary_hover`

### 3. 單位
- spacing：px 或 rem 都行，建議 rem（響應式友好）
- font_size：建議 rem

---

## 🔗 延伸

- [when-to-call.md](./when-to-call.md)
- [handoff-format.md](./handoff-format.md)
- [component-mapping.md](./component-mapping.md)
