"use client";
import { useEffect, useState } from "react";
import { ArrowUpRight, Hexagon } from "lucide-react";
import Brand from "./shared/Brand";
import Journey from "./landing/Journey";
import CommandCenter from "./dashboard/CommandCenter";

export default function Experience() {
  const [ready, setReady] = useState(false);
  useEffect(() => {
    let alive = true;
    const timer = setTimeout(() => {
      if (alive) setReady(true);
    }, 1800);
    document.fonts.ready.then(() => {
      if (alive) setReady(true);
    });
    return () => {
      alive = false;
      clearTimeout(timer);
    };
  }, []);
  return (
    <>
      <a className="skip-link" href="#command-center">
        Skip to command center
      </a>
      <div
        className={`loading-screen ${ready ? "loaded" : ""}`}
        aria-hidden={ready}
        role="status"
      >
        <Brand />
        <span>WHERE STRATEGY SHAPES DESTINY</span>
        <i />
      </div>
      <header className="site-header">
        <a className="wordmark" href="#top" aria-label="Tadbeer-o-Taqdeer home">
          <Hexagon size={28} strokeWidth={1.2} />
          <span>
            TADBEER<span className="wordmark-light">—O—TAQDEER</span>
            <small>QUANTUM RESILIENCE LAB</small>
          </span>
        </a>
        <nav aria-label="Main navigation">
          <a href="#story">The story</a>
          <a href="#method">The science</a>
          <a href="#command-center" className="nav-cta">
            Command center <ArrowUpRight size={14} />
          </a>
        </nav>
      </header>
      <main id="top">
        <Journey />
        <section id="method" className="method-section section-pad">
          <div>
            <span className="eyebrow">
              <i /> THE SCIENCE, WITHOUT THE FICTION
            </span>
            <h2>
              Six decisions.
              <br />
              <span>A connected future.</span>
            </h2>
          </div>
          <div className="method-copy">
            <p>
              A restored bridge is only the beginning. A hospital needs a road{" "}
              <em>and</em> power. Water needs access <em>and</em> a working
              pump.
            </p>
            <p>
              We encode these dependencies in a six-qubit QAOA experiment, then
              check every proposed plan against an exhaustive classical
              solution.
            </p>
            <a
              href="https://github.com/Umer-91/tadbeer-o-taqdeer/blob/phase-1-quantum/docs/MODEL.md"
              target="_blank"
              rel="noreferrer"
              className="text-link"
            >
              Explore the mathematical model <ArrowUpRight size={15} />
            </a>
          </div>
          <div className="method-strip">
            <div>
              <b>06</b>
              <span>binary interventions</span>
            </div>
            <div>
              <b>64</b>
              <span>states, exactly verifiable</span>
            </div>
            <div>
              <b>03</b>
              <span>interdependent lifelines</span>
            </div>
            <p>
              Real Qiskit circuits. Synthetic scenarios.
              <br />
              No claim of quantum advantage.
            </p>
          </div>
        </section>
        <CommandCenter />
      </main>
      <footer className="site-footer section-pad">
        <div>
          <Brand />
          <p>Where Strategy Shapes Destiny.</p>
        </div>
        <div>
          <span className="eyebrow">BUILT FOR A MORE RESILIENT TOMORROW</span>
          <p>Pakistan-inspired. Scientifically grounded.</p>
          <small>
            Research prototype · Fictional valley · No real-world infrastructure
            control
          </small>
        </div>
        <a href="#top" className="text-link">
          Back to the valley ↑
        </a>
      </footer>
    </>
  );
}
