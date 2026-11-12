# Frontend design and provenance

## Identity

**تدبیر و تقدیر**, then **TADBEER-O-TAQDEER**, then **Where Strategy Shapes Destiny.** The Urdu name appears in loading, hero, and footer. Each is a single selectable Unicode text block with `lang="ur"`, `dir="rtl"`, no letter spacing, and no character-by-character animation. Whole-block reveal preserves Nastaliq shaping.

Noto Nastaliq Urdu is self-hosted from `@fontsource/noto-nastaliq-urdu`; fallbacks are Jameel Noori Nastaleeq, Urdu Typesetting, then serif. Manrope is self-hosted for the English UI. The site makes no Google Fonts request at runtime. Both fonts use SIL OFL 1.1; complete notices are distributed in `frontend/public/licenses/`. Sources: [Noto Nastaliq](https://github.com/notofonts/nastaliq), [Manrope](https://github.com/sharanda/manrope). GSAP is distributed under its [standard license](https://gsap.com/community/standard-license/), not represented as MIT.

## Scene and visual system

Obsidian #06070B, violet #895CFF, road cyan #48D8F3, electricity amber #FFBC61, water blue #4A91FF, damage coral #FF5F6D. No stock images, AI images, copied terrain, maps, or remote model assets. Geometry and SVGs were authored procedurally for this project. The valley is fictional and is not a geographic claim.

The island uses a triangulated height field, river depression, low-poly peaks, a bridge, buildings, poles, a hospital, and a water pump. Three.js draws actual meshes and line networks. Orbit controls support dragging; building hover exposes labels. GSAP scroll triggers select valley, shock, dependency, and response camera/story states. These are explicitly labeled illustrations, not restoration outputs.

The dashboard is deliberately more legible and restrained than the landing sequence. Action IDs drive route highlighting. Service metrics, scores, measurements, QASM, and comparisons come from validated API responses. Node and route inspection works through pointer and keyboard controls. The chart stays empty until computations exist.

## Performance and access

The 3D bundle is loaded separately. Terrain geometry is reused, textures are absent, DPR is capped at 1.5, and rendering is demand-driven. Hidden-tab rendering pauses. Reduced-motion preference removes camera easing and decorative animation; 2D terrain is available explicitly and on renderer failure/context loss. No user-agent FPS or hardware-performance claim is made.

Form labels, radio groups, keyboard range adjustment, visible focus, a skip link, live request feedback, cancellation, and responsive stacked panels are included. Large Nastaliq line boxes protect ascenders and descenders. The mathematical model remains unchanged in `backend/raasta`.
