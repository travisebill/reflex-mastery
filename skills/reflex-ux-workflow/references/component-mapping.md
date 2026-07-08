# Component 對應 — 設計稿 → rx.* 對應表

> ui-ux-pro-max 出的 component 規格 → Reflex 實作

---

## 🧩 基本組件對應

| Design (Figma / Sketch) | Reflex 對應 | 備註 |
|------------------------|------------|------|
| `<Button primary>` | `rx.button(..., color_scheme="blue")` | 預設 variants |
| `<Button secondary>` | `rx.button(..., variant="outline")` | |
| `<Button ghost>` | `rx.button(..., variant="ghost")` | |
| `<Button danger>` | `rx.button(..., color_scheme="red")` | |
| `<Card>` | `rx.card(rx.vstack(...))` | |
| `<Modal>` | `rx.dialog(...)` 或 `rx.alert_dialog(...)` | 0.9+ |
| `<Input>` | `rx.input(...)` | |
| `<Textarea>` | `rx.text_area(...)` | |
| `<Select>` | `rx.select(...)` | |
| `<Checkbox>` | `rx.checkbox(...)` | |
| `<Switch>` | `rx.switch(...)` | |
| `<Radio>` | `rx.radio(...)` | |
| `<Slider>` | `rx.slider(...)` | |
| `<Badge>` | `rx.badge(...)` | |
| `<Avatar>` | `rx.avatar(...)` | |
| `<Spinner>` | `rx.spinner(...)` | |
| `<Progress>` | `rx.progress(...)` | |
| `<Tooltip>` | `rx.tooltip(...)` | |
| `<Toast>` | `rx.toast(...)` | event handler 內用 |
| `<Tabs>` | `rx.tabs(...)` | |
| `<Accordion>` | `rx.accordion(...)` | |
| `<Menu>` | `rx.menu(...)` | |
| `<Table>` | `rx.table(...)` | |
| `<Breadcrumb>` | `rx.breadcrumb(...)` | |

---

## 📐 布局組件

| Design | Reflex | 說明 |
|--------|--------|------|
| Stack vertical | `rx.vstack(...)` | 垂直堆疊 |
| Stack horizontal | `rx.hstack(...)` | 水平堆疊 |
| Container | `rx.container(...)` | 固定 max-width |
| Grid | `rx.grid(...)` | grid layout |
| Box | `rx.box(...)` | 通用 div |
| Flex | `rx.flex(...)` | flexbox |
| Center | `rx.center(...)` | 內容置中 |
| Wrap | `rx.wrap(...)` | 自動換行 |

```python
# 範例
rx.hstack(
    rx.vstack(
        rx.heading("Title"),
        rx.text("Description"),
    ),
    rx.button("Action"),
    spacing="4",
    align="center",
)
```

---

## 🎨 主題應用

```python
# 用 theme 的顏色
rx.button(
    "Click",
    bg="primary",
    color="white",
    _hover={"bg": "primary_hover"},
)

# 或用 color_scheme（推薦）
rx.button("Click", color_scheme="blue")  # 對應 theme.colors.primary
```

---

## 📝 表單 Pattern

### Input + Label

```python
rx.vstack(
    rx.text("Email"),
    rx.input(placeholder="you@example.com"),
    rx.text("Password"),
    rx.input(type="password"),
    rx.button("Sign in"),
    align="stretch",
)
```

### Form + Validation

```python
class FormState(rx.State):
    email: str = ""
    email_error: str = ""

    @rx.event
    def validate_email(self, value: str):
        self.email = value
        if "@" not in value:
            self.email_error = "Email 格式錯誤"
        else:
            self.email_error = ""

rx.vstack(
    rx.input(
        value=FormState.email,
        on_change=FormState.validate_email,
        border_color=rx.cond(FormState.email_error, "red.500", "border"),
    ),
    rx.cond(
        FormState.email_error,
        rx.text(FormState.email_error, color="red.500", font_size="sm"),
    ),
)
```

---

## 📊 表格 Pattern

```python
rx.table.root(
    rx.table.header(
        rx.table.row(
            rx.table.column_header_cell("Name"),
            rx.table.column_header_cell("Status"),
            rx.table.column_header_cell(""),
        ),
    ),
    rx.table.body(
        rx.foreach(
            State.users,
            lambda user: rx.table.row(
                rx.table.cell(user["name"]),
                rx.table.cell(user["status"]),
                rx.table.cell(rx.button("Edit")),
            ),
        ),
    ),
)
```

---

## 🪟 Modal / Dialog

```python
class State(rx.State):
    show_modal: bool = False

    @rx.event
    def open_modal(self):
        self.show_modal = True

    @rx.event
    def close_modal(self):
        self.show_modal = False

rx.dialog.root(
    rx.dialog.trigger(rx.button("Open", on_click=State.open_modal)),
    rx.dialog.content(
        rx.dialog.header("Confirm"),
        rx.dialog.body("Are you sure?"),
        rx.dialog.footer(
            rx.dialog.close(rx.button("Cancel")),
            rx.button("Yes", on_click=State.confirm),
        ),
    ),
    open=State.show_modal,
    on_open_change=State.set_show_modal,
)
```

---

## 🧭 Tabs

```python
class State(rx.State):
    active_tab: str = "overview"

rx.tabs.root(
    rx.tabs.list(
        rx.tabs.trigger("Overview", value="overview"),
        rx.tabs.trigger("Settings", value="settings"),
    ),
    rx.tabs.content(
        rx.text("Overview content"),
        value="overview",
    ),
    rx.tabs.content(
        rx.text("Settings content"),
        value="settings",
    ),
    value=State.active_tab,
    on_change=State.set_active_tab,
)
```

---

## 🍞 Breadcrumb

```python
rx.breadcrumb(
    rx.breadcrumb_item(rx.breadcrumb_link("Home", href="/")),
    rx.breadcrumb_separator(),
    rx.breadcrumb_item(rx.breadcrumb_link("Projects", href="/projects")),
    rx.breadcrumb_separator(),
    rx.breadcrumb_item(rx.breadcrumb_link("Current", href="#")),
)
```

---

## 🔄 載入 / 錯誤 / 空狀態

### Loading

```python
rx.cond(
    State.loading,
    rx.spinner(),
    rx.text(State.data),
)
```

### Error

```python
rx.cond(
    State.error != "",
    rx.callout(
        State.error,
        icon="alert-triangle",
        color_scheme="red",
    ),
)
```

### Empty

```python
rx.cond(
    State.items.length() == 0,
    rx.center(
        rx.vstack(
            rx.icon("inbox", size=48, color="gray.400"),
            rx.text("No items", color="gray.500"),
            rx.button("Add first item", on_click=State.add),
        ),
        padding="40px",
    ),
    rx.foreach(State.items, item_card),
)
```

---

## 🆕 Custom Component

ui-ux-pro-max 設計的 component 不存在於 rx.* 時，自製：

```python
def stat_card(title: str, value: str, change: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text(title, color="gray.500", font_size="sm"),
            rx.heading(value, size="xl"),
            rx.text(change, color="green.500", font_size="sm"),
            align="start",
            spacing="1",
        ),
    )

# 用法
rx.hstack(
    stat_card("Users", "1,234", "+12%"),
    stat_card("Revenue", "$5,678", "+8%"),
)
```

---

## 🎯 不存在於 Reflex 的常見設計

| Design 想要 | 解法 |
|------------|------|
| Date picker | `rx.input(type="date")` 或 third-party |
| Time picker | `rx.input(type="time")` |
| Color picker | `rx.input(type="color")` |
| File upload | `rx.upload(...)` |
| Rich text editor | third-party（TipTap / Lexical） |
| Drag and drop | 自製（用 `rx.box` + on_drop） |
| Charts | third-party（Recharts / Plotly） |
| Map | third-party（Mapbox / Leaflet） |
| Data grid (advanced) | third-party（AG Grid / TanStack） |
| Animation | Framer Motion（要包成 component） |

---

## 🔗 延伸

- [when-to-call.md](./when-to-call.md)
- [design-tokens-mapping.md](./design-tokens-mapping.md)
- [accessibility.md](./accessibility.md)
