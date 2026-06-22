"""Generate the README figures without optional plotting dependencies."""

from __future__ import annotations

import html
import math
from pathlib import Path

import numpy as np

from qrw import classical_distribution, quantum_distribution

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"


class SVG:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.items = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="white"/>',
            '<style>text{font-family:Arial,sans-serif;fill:#202124}.axis{stroke:#5f6368;stroke-width:1}'
            '.grid{stroke:#dadce0;stroke-width:1}.label{font-size:13px}.title{font-size:20px;font-weight:600}'
            '.legend{font-size:13px}</style>',
        ]

    def line(self, x1: float, y1: float, x2: float, y2: float, **attrs: object) -> None:
        self.items.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" {fmt(attrs)}/>')

    def rect(self, x: float, y: float, w: float, h: float, **attrs: object) -> None:
        self.items.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" {fmt(attrs)}/>')

    def circle(self, x: float, y: float, r: float, **attrs: object) -> None:
        self.items.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" {fmt(attrs)}/>')

    def polyline(self, points: list[tuple[float, float]], **attrs: object) -> None:
        value = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        self.items.append(f'<polyline points="{value}" {fmt(attrs)}/>')

    def text(self, x: float, y: float, value: str, **attrs: object) -> None:
        self.items.append(f'<text x="{x:.2f}" y="{y:.2f}" {fmt(attrs)}>{html.escape(value)}</text>')

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join([*self.items, "</svg>\n"]))


def fmt(attrs: dict[str, object]) -> str:
    def attribute_name(key: str) -> str:
        key = key[:-1] if key.endswith("_") else key
        return key.replace("_", "-")

    return " ".join(f'{attribute_name(key)}="{value}"' for key, value in attrs.items())


def distribution_figure() -> None:
    size, steps, start = 64, 20, 32
    quantum = quantum_distribution(size=size, steps=steps, start=start)
    classical = classical_distribution(size=size, steps=steps, start=start)
    offsets = np.arange(size) - start
    mask = np.abs(offsets) <= steps + 2
    xdata = offsets[mask]
    qdata = quantum[mask]
    cdata = classical[mask]

    svg = SVG(900, 520)
    left, top, width, height = 80, 65, 780, 370
    ymax = max(qdata.max(), cdata.max()) * 1.12
    sx = lambda x: left + (x - xdata.min()) / (xdata.max() - xdata.min()) * width
    sy = lambda y: top + height - y / ymax * height

    svg.text(450, 32, "Coherent quantum walk versus classical random walk", text_anchor="middle", class_="title")
    for value in np.linspace(0, ymax, 5):
        y = sy(value)
        svg.line(left, y, left + width, y, class_="grid")
        svg.text(left - 10, y + 4, f"{value:.2f}", text_anchor="end", class_="label")
    for value in range(-20, 21, 5):
        x = sx(value)
        svg.line(x, top + height, x, top + height + 5, class_="axis")
        svg.text(x, top + height + 23, str(value), text_anchor="middle", class_="label")
    svg.line(left, top + height, left + width, top + height, class_="axis")
    svg.line(left, top, left, top + height, class_="axis")

    bar_width = width / len(xdata) * 0.72
    for x, value in zip(xdata, cdata):
        svg.rect(sx(x) - bar_width / 2, sy(value), bar_width, top + height - sy(value), fill="#bdc1c6", opacity="0.65")
    points = [(sx(x), sy(value)) for x, value in zip(xdata, qdata)]
    svg.polyline(points, fill="none", stroke="#0057b8", stroke_width="2.5")
    for x, y in points:
        svg.circle(x, y, 3.2, fill="#0057b8")
    svg.text(450, 495, "displacement from initial position", text_anchor="middle", class_="label")
    svg.text(18, 260, "probability", transform="rotate(-90 18 260)", text_anchor="middle", class_="label")
    svg.rect(625, 72, 17, 12, fill="#bdc1c6", opacity="0.65")
    svg.text(648, 83, "classical", class_="legend")
    svg.line(725, 78, 746, 78, stroke="#0057b8", stroke_width="2.5")
    svg.circle(735, 78, 3.2, fill="#0057b8")
    svg.text(752, 83, "quantum", class_="legend")
    svg.text(450, 55, f"{steps} steps on a {size}-site cycle", text_anchor="middle", class_="label")
    svg.save(FIGURES / "quantum_vs_classical.svg")


def evolution_figure() -> None:
    max_steps, size, start = 40, 128, 64
    offsets = np.arange(-max_steps, max_steps + 1)
    data = np.array([
        quantum_distribution(size=size, steps=step, start=start)[start + offsets]
        for step in range(max_steps + 1)
    ])
    scale = np.sqrt(data / max(data.max(), 1e-15))

    svg = SVG(900, 540)
    left, top, width, height = 85, 60, 740, 410
    cell_w, cell_h = width / len(offsets), height / len(data)
    svg.text(455, 32, "Quantum-walk probability through time", text_anchor="middle", class_="title")
    for row in range(len(data)):
        for col in range(len(offsets)):
            value = scale[row, col]
            red = int(247 - 229 * value)
            green = int(250 - 151 * value)
            blue = int(255 - 71 * value)
            svg.rect(left + col * cell_w, top + row * cell_h, cell_w + 0.15, cell_h + 0.15, fill=f"rgb({red},{green},{blue})")
    svg.rect(left, top, width, height, fill="none", stroke="#5f6368")
    for value in range(-40, 41, 10):
        x = left + (value + max_steps + 0.5) * cell_w
        svg.text(x, top + height + 22, str(value), text_anchor="middle", class_="label")
    for value in range(0, 41, 10):
        y = top + (value + 0.7) * cell_h
        svg.text(left - 12, y, str(value), text_anchor="end", class_="label")
    svg.text(left + width / 2, 515, "displacement", text_anchor="middle", class_="label")
    svg.text(22, top + height / 2, "step", transform=f"rotate(-90 22 {top + height / 2})", text_anchor="middle", class_="label")
    for index in range(101):
        value = index / 100
        red = int(247 - 229 * value)
        green = int(250 - 151 * value)
        blue = int(255 - 71 * value)
        svg.rect(845, top + (100 - index) * 3.2, 16, 3.4, fill=f"rgb({red},{green},{blue})")
    svg.text(853, top - 7, "high", text_anchor="middle", class_="label")
    svg.text(853, top + 340, "low", text_anchor="middle", class_="label")
    svg.save(FIGURES / "quantum_evolution.svg")


def variance(probability: np.ndarray, offsets: np.ndarray) -> float:
    mean = float(np.dot(offsets, probability))
    return float(np.dot(offsets**2, probability) - mean**2)


def variance_figure() -> None:
    size, start, max_steps = 256, 128, 64
    offsets = np.arange(size) - start
    steps = np.arange(1, max_steps + 1)
    quantum = np.array([variance(quantum_distribution(size=size, steps=int(t), start=start), offsets) for t in steps])
    classical = np.array([variance(classical_distribution(size=size, steps=int(t), start=start), offsets) for t in steps])
    fit_slice = steps >= 8
    q_slope = np.polyfit(np.log(steps[fit_slice]), np.log(quantum[fit_slice]), 1)[0]
    c_slope = np.polyfit(np.log(steps[fit_slice]), np.log(classical[fit_slice]), 1)[0]

    svg = SVG(900, 520)
    left, top, width, height = 85, 60, 750, 370
    xmin, xmax = 1.0, float(max_steps)
    ymin, ymax = 0.7, max(quantum.max(), classical.max()) * 1.25
    sx = lambda x: left + math.log(x / xmin) / math.log(xmax / xmin) * width
    sy = lambda y: top + height - math.log(y / ymin) / math.log(ymax / ymin) * height
    svg.text(460, 32, "Ballistic quantum spreading versus classical diffusion", text_anchor="middle", class_="title")
    for value in (1, 2, 4, 8, 16, 32, 64):
        x = sx(value)
        svg.line(x, top, x, top + height, class_="grid")
        svg.text(x, top + height + 22, str(value), text_anchor="middle", class_="label")
    for value in (1, 10, 100, 1000):
        if value <= ymax:
            y = sy(value)
            svg.line(left, y, left + width, y, class_="grid")
            svg.text(left - 10, y + 4, str(value), text_anchor="end", class_="label")
    svg.line(left, top + height, left + width, top + height, class_="axis")
    svg.line(left, top, left, top + height, class_="axis")
    qpoints = [(sx(t), sy(v)) for t, v in zip(steps, quantum)]
    cpoints = [(sx(t), sy(v)) for t, v in zip(steps, classical)]
    svg.polyline(qpoints, fill="none", stroke="#0057b8", stroke_width="2.7")
    svg.polyline(cpoints, fill="none", stroke="#c5221f", stroke_width="2.7")
    svg.text(460, 492, "steps (log scale)", text_anchor="middle", class_="label")
    svg.text(20, 245, "position variance (log scale)", transform="rotate(-90 20 245)", text_anchor="middle", class_="label")
    svg.line(550, 78, 575, 78, stroke="#0057b8", stroke_width="2.7")
    svg.text(584, 83, f"quantum slope = {q_slope:.2f}", class_="legend")
    svg.line(550, 101, 575, 101, stroke="#c5221f", stroke_width="2.7")
    svg.text(584, 106, f"classical slope = {c_slope:.2f}", class_="legend")
    svg.save(FIGURES / "variance_scaling.svg")


def main() -> int:
    distribution_figure()
    evolution_figure()
    variance_figure()
    for path in sorted(FIGURES.glob("*.svg")):
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
