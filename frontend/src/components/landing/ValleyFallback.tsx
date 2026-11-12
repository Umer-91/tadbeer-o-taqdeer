export default function ValleyFallback({ stage }: { stage: number }) {
  const road = stage === 1 ? "#ff5f6d" : "#48d8f3";
  return (
    <div className="valley-fallback">
      <svg
        viewBox="0 0 1000 550"
        role="img"
        aria-label="Stylized 2D valley: road, electricity, and water networks linking fictional villages and hospital"
      >
        <defs>
          <linearGradient id="rock" x2="0.2" y2="1">
            <stop stopColor="#494256" />
            <stop offset="1" stopColor="#14141f" />
          </linearGradient>
          <linearGradient id="river" x2="1" y2="0">
            <stop stopColor="#133d68" />
            <stop offset="1" stopColor="#459cb8" />
          </linearGradient>
        </defs>
        <path
          d="M80 330 500 495 920 290 510 110Z"
          fill="#11131f"
          stroke="#40334f"
        />
        <path d="m80 330 420 165 420-205v38L500 535 80 371Z" fill="#0e0e17" />
        {[
          { x: 270, y: 310, w: 190, h: 195 },
          { x: 460, y: 270, w: 210, h: 220 },
          { x: 660, y: 250, w: 150, h: 150 },
          { x: 710, y: 350, w: 160, h: 230 },
          { x: 355, y: 405, w: 155, h: 175 },
        ].map((m, i) => (
          <g key={i}>
            <path
              d={`M${m.x - m.w / 2} ${m.y} ${m.x} ${m.y - m.h} ${m.x + m.w / 2} ${m.y}Z`}
              fill="url(#rock)"
              stroke="#494352"
            />
            <path
              d={`M${m.x} ${m.y - m.h} ${m.x + 20} ${m.y - 35} ${m.x + m.w / 2} ${m.y}Z`}
              fill="#151622"
            />
            <path
              d={`m${m.x - 20} ${m.y - m.h + 45} 20-45 27 53-23-12Z`}
              fill="#9c98a8"
              opacity=".45"
            />
          </g>
        ))}
        <path
          d="M190 340q160-110 240 0t180 5 210-60"
          stroke="url(#river)"
          strokeWidth="21"
          fill="none"
        />
        <path
          d="M150 310 310 340 450 300 580 355 780 320"
          stroke={road}
          strokeWidth="3"
          fill="none"
        />
        <path
          d="M400 220 560 290 610 380"
          stroke="#ffbc61"
          strokeWidth="2"
          strokeDasharray="5 7"
          fill="none"
        />
        {[
          { x: 310, y: 340, n: "VILLAGE A" },
          { x: 560, y: 290, n: "HOSPITAL" },
          { x: 610, y: 380, n: "WATER PUMP" },
        ].map((p) => (
          <g key={p.n}>
            <circle cx={p.x} cy={p.y} r="5" fill="#e5e2f5" />
            <text
              x={p.x + 13}
              y={p.y - 10}
              fill="#b7b5c7"
              fontSize="11"
              letterSpacing="2"
            >
              {p.n}
            </text>
          </g>
        ))}
      </svg>
      <span className="fallback-note">
        SIMPLIFIED 2D TERRAIN · ILLUSTRATION
      </span>
    </div>
  );
}
