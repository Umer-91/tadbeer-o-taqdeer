"use client";
import { useEffect, useRef, useState } from "react";
import dynamic from "next/dynamic";
import { ArrowDown, ArrowUpRight, Move, Layers2 } from "lucide-react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Brand from "../shared/Brand";
import ValleyFallback from "./ValleyFallback";

const ValleyScene = dynamic(() => import("./ValleyScene"), {
  ssr: false,
  loading: () => <ValleyFallback stage={0} />,
});
const chapters = [
  {
    number: "02",
    tag: "THE SHOCK",
    title: (
      <>
        One flood.
        <br />A thousand
        <br />
        <em>connections lost.</em>
      </>
    ),
    copy: "When a bridge falls, the damage travels further than the river. Hospital access, electricity, and safe water can fail together.",
  },
  {
    number: "03",
    tag: "THE DEPENDENCY",
    title: (
      <>
        Recovery is
        <br />a connected
        <br />
        <em>decision.</em>
      </>
    ),
    copy: "Roads bring repair crews. Electricity powers care. Access and power keep water flowing. Restoring them together changes the outcome.",
  },
  {
    number: "04",
    tag: "THE RESPONSE",
    title: (
      <>
        Limited resources.
        <br />
        <em>Deliberate choices.</em>
      </>
    ),
    copy: "Choose a scenario. Set a budget. Compare a quantum-sampled plan with exact and greedy baselines. Every service score remains verifiable.",
  },
];
export default function Journey() {
  const root = useRef<HTMLElement>(null);
  const [stage, setStage] = useState(0);
  const [flat, setFlat] = useState(false);
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setReduced(media.matches);
    update();
    media.addEventListener("change", update);
    gsap.registerPlugin(ScrollTrigger);
    const ctx = gsap.context(() => {
      const sections = gsap.utils.toArray<HTMLElement>(".story-panel");
      sections.forEach((section, i) =>
        ScrollTrigger.create({
          trigger: section,
          start: "top 55%",
          end: "bottom 55%",
          onEnter: () => setStage(i),
          onEnterBack: () => setStage(i),
        }),
      );
      if (!media.matches)
        gsap.fromTo(
          ".hero-copy",
          { y: 22, opacity: 0 },
          { y: 0, opacity: 1, duration: 1.4, delay: 0.25, ease: "power2.out" },
        );
    }, root);
    return () => {
      ctx.revert();
      media.removeEventListener("change", update);
    };
  }, []);
  return (
    <section
      ref={root}
      className={`journey stage-${stage}`}
      aria-label="The valley restoration story"
    >
      <div
        className="journey-visual"
        aria-label="Illustrative synthetic valley"
      >
        <div className="orbital-glow" />
        <div className="valley-frame">
          {flat ? (
            <ValleyFallback stage={stage} />
          ) : (
            <ValleyScene stage={stage} reduced={reduced} />
          )}
        </div>
        <div className="scene-caption">
          <span className="mini-cross">+</span>
          <span>
            FICTIONAL PAKISTAN-INSPIRED VALLEY
            <br />
            <b>CINEMATIC ILLUSTRATION · NOT COMPUTED</b>
          </span>
        </div>
        <div className="scene-controls">
          <span>
            <Move size={13} /> {flat ? "2D overview" : "Drag to explore"}
          </span>
          <button
            type="button"
            aria-pressed={flat}
            onClick={() => setFlat((v) => !v)}
          >
            <Layers2 size={14} /> {flat ? "View 3D" : "View 2D"}
          </button>
        </div>
      </div>
      <div className="journey-copy">
        <section className="hero story-panel" aria-labelledby="hero-title">
          <div className="hero-copy">
            <div className="eyebrow hero-kicker">
              <span className="status-dot" /> QUANTUM-ASSISTED DISASTER RECOVERY
            </div>
            <h1 id="hero-title">
              <Brand />
              <span className="english-title">TADBEER-O-TAQDEER</span>
            </h1>
            <p className="tagline">Where Strategy Shapes Destiny.</p>
            <p className="hero-description">
              When everything is connected,
              <br className="mobile-break" /> every recovery decision matters.
            </p>
            <a className="primary-button" href="#command-center">
              Enter Command Center <ArrowUpRight size={16} />
            </a>
          </div>
          <div className="hero-bottom">
            <a href="#story">
              <ArrowDown size={16} />
              <span>SCROLL TO DISCOVER</span>
            </a>
            <div className="lifeline-legend">
              <span>
                <i className="road" /> Roads
              </span>
              <span>
                <i className="power" /> Electricity
              </span>
              <span>
                <i className="water" /> Water
              </span>
            </div>
            <span className="mono">01 / THE VALLEY</span>
          </div>
        </section>
        {chapters.map((chapter, i) => (
          <article
            key={chapter.number}
            id={i === 0 ? "story" : undefined}
            className="chapter story-panel"
          >
            <div className="chapter-copy">
              <span className="eyebrow">
                <b>{chapter.number}</b> / {chapter.tag}
              </span>
              <h2>{chapter.title}</h2>
              <p>{chapter.copy}</p>
              {i === 2 && (
                <a href="#command-center" className="text-link">
                  Explore the command center <ArrowUpRight size={16} />
                </a>
              )}
              <div className="chapter-progress">
                {[0, 1, 2, 3].map((n) => (
                  <i key={n} className={stage >= n ? "active" : ""} />
                ))}
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
