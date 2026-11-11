const M = { top: 20, right: 70, bottom: 36, left: 48 };

function frame(sel, height = 340) {
  const el = d3.select(sel);
  el.selectAll("*").remove();
  const width = el.node().clientWidth || 640;
  const svg = el.append("svg").attr("viewBox", `0 0 ${width} ${height}`);
  return { svg, iw: width - M.left - M.right, ih: height - M.top - M.bottom };
}

function lineChart(sel, data, { x, y, series, yLabel }) {
  const { svg, iw, ih } = frame(sel);
  const g = svg.append("g").attr("transform", `translate(${M.left},${M.top})`);
  const groups = d3.groups(data, d => d[series]);

  const xs = d3.scaleLinear().domain(d3.extent(data, d => d[x])).range([0, iw]);
  const ys = d3.scaleLinear().domain(d3.extent(data, d => d[y])).nice().range([ih, 0]);
  const color = d3.scaleOrdinal().domain(groups.map(d => d[0])).range(d3.schemeTableau10);

  g.append("g").attr("class", "axis").attr("transform", `translate(0,${ih})`)
    .call(d3.axisBottom(xs).tickFormat(d3.format("d")));
  g.append("g").attr("class", "axis").call(d3.axisLeft(ys).ticks(5));
  g.append("text").attr("class", "annotation").attr("y", -6).text(yLabel);

  const line = d3.line().x(d => xs(d[x])).y(d => ys(d[y]));

  g.selectAll("path.series").data(groups).join("path")
    .attr("class", "series")
    .attr("fill", "none")
    .attr("stroke", d => color(d[0]))
    .attr("stroke-width", 2)
    .attr("d", d => line(d[1]));

  g.selectAll("text.label").data(groups).join("text")
    .attr("class", "annotation label")
    .attr("x", iw + 6)
    .attr("y", d => ys(d[1].at(-1)[y]) + 4)
    .attr("fill", d => color(d[0]))
    .text(d => d[0]);

  return { xs, ys, color, g, iw, ih };
}

function render(data) {
  const spec = { x: "year", y: "value", series: "scenario", yLabel: "Anomaly (C)" };

  lineChart("#chart-hook", data, spec);
  lineChart("#chart-and", data, spec);
  lineChart("#chart-therefore", data, spec);

  const but = lineChart("#chart-but", data, spec);
  const rule = but.g.append("line").attr("class", "annotation-leader").attr("y1", 0).attr("y2", but.ih);
  const slider = document.getElementById("year");
  const out = document.getElementById("year-out");

  const moveTo = year => {
    out.textContent = year;
    rule.attr("x1", but.xs(year)).attr("x2", but.xs(year));
  };

  slider.oninput = e => moveTo(+e.target.value);
  moveTo(+slider.value);
}

let rows = [];

d3.csv("data/sample.csv", d3.autoType).then(data => {
  rows = d3.sort(data, d => d.year);
  render(rows);
});

window.addEventListener("resize", () => {
  clearTimeout(window.__rt);
  window.__rt = setTimeout(() => rows.length && render(rows), 150);
});
