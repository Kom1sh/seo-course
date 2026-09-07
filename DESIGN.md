---
name: seo-course-deck
description: "Дизайн-контракт HTML-деки «Поиск и ИИ-выдача» для Школы Икс. Донор токенов — Miro (awesome-design-md): белый холст, канареечный маркер, пастельные стикеры. Не скин, а словарь."
colors:
  canvas: "#FFFFFF"
  surface: "#F7F8FA"
  surface-soft: "#FAFBFC"
  ink: "#1C1C1E"
  charcoal: "#2E2E33"
  slate: "#5C6170"
  steel: "#7A7E8A"
  hairline: "#E0E2E8"
  hairline-strong: "#C9CCD4"
  yellow: "#FFD02F"
  yellow-deep: "#FCB900"
  yellow-light: "#FFF4C4"
  yellow-dark: "#746019"
  blue: "#4262FF"
  blue-pressed: "#2A41B6"
  teal: "#0FBCB0"
  teal-light: "#C3FAF5"
  moss-dark: "#187574"
  rose-light: "#FDE0F0"
  rose-dark: "#8A1F5C"
  coral: "#FF9999"
  coral-light: "#FFC6C6"
  coral-dark: "#600000"
  orange-light: "#FFE6CD"
  lavender: "#EDEAFF"
  lavender-dark: "#3F3A8F"
  success: "#00B473"
  dark-canvas: "#1C1C1E"
  on-dark: "#FFFFFF"
  on-dark-muted: "rgba(255,255,255,0.64)"
typography:
  display-xl: {fontFamily: Unbounded, fontSize: 72px, fontWeight: 600, lineHeight: 1.02, letterSpacing: -0.02em}
  display-lg: {fontFamily: Unbounded, fontSize: 54px, fontWeight: 600, lineHeight: 1.06, letterSpacing: -0.02em}
  heading: {fontFamily: Unbounded, fontSize: 34px, fontWeight: 600, lineHeight: 1.14, letterSpacing: -0.01em}
  card-title: {fontFamily: Unbounded, fontSize: 24px, fontWeight: 500, lineHeight: 1.2}
  body-lg: {fontFamily: Golos Text, fontSize: 28px, fontWeight: 400, lineHeight: 1.38}
  body: {fontFamily: Golos Text, fontSize: 22px, fontWeight: 400, lineHeight: 1.42}
  stat: {fontFamily: Unbounded, fontSize: 84px, fontWeight: 600, lineHeight: 1, letterSpacing: -0.03em}
  eyebrow: {fontFamily: JetBrains Mono, fontSize: 14px, fontWeight: 600, lineHeight: 1.2, letterSpacing: 0.12em, textTransform: uppercase}
  mono: {fontFamily: JetBrains Mono, fontSize: 18px, fontWeight: 500, lineHeight: 1.4}
rounded: {sm: 8px, md: 12px, lg: 16px, xl: 28px, full: 9999px}
spacing: {xs: 8px, sm: 12px, md: 16px, lg: 24px, xl: 32px, xxl: 48px, frame-x: 84px, frame-y: 60px}
components:
  pill-ink: {background: "{colors.ink}", color: "{colors.on-dark}", rounded: "{rounded.full}", typography: "{typography.eyebrow}"}
  pill-yellow: {background: "{colors.yellow}", color: "{colors.ink}", rounded: "{rounded.full}"}
  card: {background: "{colors.surface}", rounded: "{rounded.lg}", padding: "{spacing.lg}", border: "1px solid {colors.hairline}"}
  sticky: {rounded: "{rounded.xl}", padding: "{spacing.xl}", shadow: none}
  browser-frame: {background: "{colors.canvas}", rounded: "{rounded.lg}", border: "1px solid {colors.hairline}", shadow: "rgba(5,0,56,0.08) 0 12px 32px -4px"}
  highlight: {background: "{colors.yellow}", padding: "0 .12em", boxDecorationBreak: clone}
---

## Overview
Дека — лекция для студентов 1–3 курсов: 16:9, кадр 1600×900, читается с проектора с последнего ряда.
Характер: доска в аудитории. Белый холст, крупный гротеск, один маркер-выделитель, пастельные стикеры
для группировки смыслов, настоящие скриншоты и графики по живым данным. Ни одного декоративного пятна.

## Colors
- **Yellow** — маркер: ровно одно выделение на слайд (ключевая фраза заголовка) плюс номера разделов. Текст поверх жёлтого — только чернила.
- Пастели — не украшение, а смысловая кодировка, одна на тему: **teal** = сканирование/робот, **lavender** = индекс, **yellow-light** = ранжирование/выдача, **rose** = ИИ и GEO, **coral** = ошибка/риск, **orange-light** = кейсы.
- **Blue** — только ссылки, URL и всё «гуглово». **Success** — только результат «стало».
- Тёмные слайды (dark-canvas) — разделители секций, для ритма. На них жёлтый допустим для крупных цифр.

## Typography
Unbounded — заголовки, цифры, названия карточек (широкий, плакатный, кириллица родная). Golos Text — весь текст.
JetBrains Mono — надзаголовки (eyebrow), URL, запросы, код. Никаких курсивов, никакого 700 у Unbounded (600 — потолок).
Минимальный кегль на слайде — 18px (подписи графиков и источники). Основной текст 22–28px.

## Layout
Рамка кадра 84×60px. Шапка: eyebrow-пилюля слева, счётчик справа. Заголовок 1–2 строки. Тело — сетка из 2–4 колонок с зазором 20–28px,
`minmax(0,1fr)` и `min-width:0` у детей. Низ кадра — заметка или источник, никогда не пусто более чем на 20% высоты.

## Elevation & Depth
Плоско. Тень только у browser-frame (скриншоты сайтов и макет выдачи). Карточки — заливка surface плюс hairline.

## Shapes
Карточки 16px, стикеры 28px, пилюли и бейджи — full. Логотипы — на белых плитках 16px в фирменном цвете.

## Components
pill-ink (шапка), sticky (тематические блоки), card (факты), browser-frame (скриншот с тремя точками и адресной строкой),
stat (большая цифра + подпись), chart (inline SVG фиксированного размера, подписи HTML), tile (логотип), serp-mock (макет выдачи).

## Do's and Don'ts
- Делать: одна мысль на слайд; заголовок = утверждение, а не тема; каждая цифра с источником и датой; скриншоты только в browser-frame.
- Делать: логотипы в фирменном цвете на белом; иконки только смысловые; графики из данных, не рисунки «для настроения».
- Не делать: градиенты, тени на карточках, пятна и блобы, жёлтый текст на белом, больше двух пастелей на слайде, стоковые иллюстрации людей.
- Не делать: абзацы длиннее трёх строк; текст мельче 18px; Unbounded в наборном тексте; эмодзи.
