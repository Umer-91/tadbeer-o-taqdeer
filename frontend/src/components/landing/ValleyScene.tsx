"use client";
import {
  Component,
  Suspense,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import type { ReactNode } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { Line, OrbitControls } from "@react-three/drei";
import * as THREE from "three";
import ValleyFallback from "./ValleyFallback";

const peaks = [
  [-4.7, -2.1, 2.8, 1.1],
  [-1.8, -3, 3.5, 1.3],
  [1.2, -2.6, 2.5, 1.05],
  [4.8, -2.1, 3.5, 1.15],
  [-4, 2.6, 1.8, 1.2],
  [0.2, 3.2, 2.6, 1.2],
  [3.8, 2.6, 2.2, 1.1],
];
function height(x: number, z: number) {
  const ridge = peaks.reduce(
    (sum, [px, pz, h, w]) =>
      sum + h * Math.exp(-((x - px) ** 2 + (z - pz) ** 2) / (w * w)),
    0,
  );
  const noise =
    (Math.sin(x * 4.7 + z * 3.2) * Math.cos(z * 5.1 - x * 1.3) + 1) * 0.12;
  const river = Math.exp(-((z - 0.35 * Math.sin(x * 0.7)) ** 2) / 0.3);
  return 0.18 + (ridge + noise) * (1 - river * 0.94);
}
function terrainGeometry() {
  const positions: number[] = [],
    colors: number[] = [];
  const nx = 70,
    nz = 44;
  const vertex = (i: number, j: number) => {
    const x = -7.5 + (15 * i) / nx,
      z = -4.5 + (9 * j) / nz;
    return [x, height(x, z), z];
  };
  for (let i = 0; i < nx; i++)
    for (let j = 0; j < nz; j++) {
      const x = -7.5 + (15 * (i + 0.5)) / nx,
        z = -4.5 + (9 * (j + 0.5)) / nz;
      if ((x / 7.5) ** 2 + (z / 4.5) ** 2 > 1) continue;
      const a = vertex(i, j),
        b = vertex(i + 1, j),
        c = vertex(i, j + 1),
        d = vertex(i + 1, j + 1);
      for (const triangle of [
        [a, c, b],
        [b, c, d],
      ]) {
        const elevation = triangle.reduce((s, p) => s + p[1], 0) / 3;
        const color = new THREE.Color(
          elevation > 2.9 ? "#a0a2ae" : elevation > 1.7 ? "#535060" : "#303242",
        );
        color.multiplyScalar(0.85 + 0.15 * Math.sin(i * 12.3 + j * 7.1) ** 2);
        for (const point of triangle) {
          positions.push(...point);
          colors.push(color.r, color.g, color.b);
        }
      }
    }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute(
    "position",
    new THREE.Float32BufferAttribute(positions, 3),
  );
  geometry.setAttribute("color", new THREE.Float32BufferAttribute(colors, 3));
  geometry.computeVertexNormals();
  return geometry;
}
type Point = [number, number, number];
function path(points: [number, number][]): Point[] {
  const curve = new THREE.CatmullRomCurve3(
    points.map(([x, z]) => new THREE.Vector3(x, 0, z)),
  );
  return curve.getPoints(70).map((v) => [v.x, height(v.x, v.z) + 0.09, v.z]);
}
function Building({
  x,
  z,
  label,
  hospital = false,
  onInspect,
}: {
  x: number;
  z: number;
  label: string;
  hospital?: boolean;
  onInspect: (label: string | null) => void;
}) {
  const [hover, setHover] = useState(false);
  return (
    <group
      position={[x, height(x, z) + 0.1, z]}
      onPointerOver={(e) => {
        e.stopPropagation();
        setHover(true);
        onInspect(label);
      }}
      onPointerOut={() => {
        setHover(false);
        onInspect(null);
      }}
    >
      <mesh position={[0, 0.16, 0]}>
        <boxGeometry args={hospital ? [0.65, 0.32, 0.45] : [0.3, 0.3, 0.3]} />
        <meshStandardMaterial
          color={hover ? "#b8a1f3" : hospital ? "#c9c6dc" : "#85899d"}
        />
      </mesh>
      {hospital ? (
        <>
          <mesh position={[0, 0.34, 0]}>
            <boxGeometry args={[0.6, 0.04, 0.4]} />
            <meshStandardMaterial color="#41465e" />
          </mesh>
          <mesh position={[0, 0.18, 0.23]}>
            <boxGeometry args={[0.05, 0.16, 0.015]} />
            <meshBasicMaterial color="#ff6d80" />
          </mesh>
          <mesh position={[0, 0.18, 0.24]}>
            <boxGeometry args={[0.15, 0.05, 0.015]} />
            <meshBasicMaterial color="#ff6d80" />
          </mesh>
        </>
      ) : (
        <mesh position={[0, 0.37, 0]} rotation={[0, Math.PI / 4, 0]}>
          <coneGeometry args={[0.25, 0.18, 4]} />
          <meshStandardMaterial color="#4c5470" />
        </mesh>
      )}
    </group>
  );
}
function CameraMotion({ stage }: { stage: number }) {
  const { camera, invalidate } = useThree();
  const moving = useRef(true);
  const destination = useMemo(
    () =>
      new THREE.Vector3(
        ...([
          [11, 9, 13],
          [10, 8, 12],
          [9, 10, 12],
          [10, 10, 14],
        ][stage] as Point),
      ),
    [stage],
  );
  useEffect(() => {
    moving.current = true;
    invalidate();
  }, [destination, invalidate]);
  useFrame((_, delta) => {
    if (!moving.current) return;
    camera.position.lerp(destination, Math.min(delta * 2, 1));
    camera.lookAt(0, 0.8, 0);
    if (camera.position.distanceTo(destination) < 0.025) moving.current = false;
    else invalidate();
  });
  return null;
}
function Landscape({
  stage,
  onInspect,
}: {
  stage: number;
  onInspect: (label: string | null) => void;
}) {
  const geometry = useMemo(() => terrainGeometry(), []);
  useEffect(() => () => geometry.dispose(), [geometry]);
  const river = useMemo(
    () =>
      path([
        [-7, 0],
        [-4, -0.15],
        [-2, -0.34],
        [0, 0],
        [3, 0.3],
        [6.7, -0.3],
      ]),
    [],
  );
  const roads = useMemo(
    () =>
      path([
        [-6.5, 0.9],
        [-4, 0.7],
        [-2, 1],
        [0.2, -0.7],
        [2, -1.05],
        [4.5, 0.8],
      ]),
    [],
  );
  const power = useMemo(
    () =>
      path([
        [-4, -1.3],
        [-2, -1],
        [0, -0.7],
        [2, -1.05],
        [3, 1.1],
      ]),
    [],
  );
  const water = useMemo(
    () =>
      path([
        [3, 1.1],
        [4.5, 1],
        [5.3, 0.5],
      ]),
    [],
  );
  return (
    <group rotation={[0, -0.08, 0]}>
      <mesh geometry={geometry}>
        <meshStandardMaterial
          vertexColors
          flatShading
          roughness={0.92}
          metalness={0.12}
        />
      </mesh>
      <mesh position={[0, -0.47, 0]} scale={[7.45, 1, 4.4]}>
        <cylinderGeometry args={[1, 0.84, 1.35, 64]} />
        <meshStandardMaterial color="#161522" roughness={0.95} />
      </mesh>
      <Line
        points={river}
        color={stage === 1 ? "#416f9f" : "#347ab0"}
        lineWidth={stage === 1 ? 13 : 8}
        transparent
        opacity={0.75}
      />
      <Line
        points={roads}
        color={stage === 1 ? "#ff5f6d" : "#48d8f3"}
        lineWidth={2}
      />
      <Line
        points={roads}
        color={stage === 1 ? "#ff5f6d" : "#48d8f3"}
        lineWidth={7}
        transparent
        opacity={0.12}
      />
      <Line
        points={power}
        color={stage === 1 ? "#ff5f6d" : "#ffbc61"}
        lineWidth={1.6}
        dashed
        dashSize={0.12}
        gapSize={0.06}
      />
      <Line points={water} color="#4a91ff" lineWidth={2.5} />
      {[-4, -2, 0].map((x) => (
        <group key={x} position={[x, height(x, -1) + 0.05, -1]}>
          <mesh position={[0, 0.35, 0]}>
            <cylinderGeometry args={[0.025, 0.035, 0.7, 6]} />
            <meshStandardMaterial color="#737780" />
          </mesh>
          <mesh position={[0, 0.7, 0]}>
            <boxGeometry args={[0.35, 0.035, 0.05]} />
            <meshStandardMaterial color="#9a93a0" />
          </mesh>
        </group>
      ))}
      <Building
        x={2}
        z={-1.05}
        label="VALLEY HOSPITAL"
        hospital
        onInspect={onInspect}
      />
      {[
        [-3.7, 0.85],
        [-3.2, 0.9],
        [-3.5, 1.3],
        [4.4, 1],
        [4.8, 1.2],
        [4.4, 1.5],
        [-0.6, 1.1],
        [-0.25, 1.25],
      ].map(([x, z], i) => (
        <Building
          key={i}
          x={x}
          z={z}
          onInspect={onInspect}
          label={i < 3 ? "VILLAGE A" : i < 6 ? "VILLAGE B" : "VILLAGE C"}
        />
      ))}
      <group
        position={[3, height(3, 1.1) + 0.15, 1.1]}
        onPointerOver={(e) => {
          e.stopPropagation();
          onInspect("WATER PUMP");
        }}
        onPointerOut={() => onInspect(null)}
      >
        <mesh>
          <cylinderGeometry args={[0.18, 0.18, 0.3, 12]} />
          <meshStandardMaterial color="#73a6c3" />
        </mesh>
      </group>
      <mesh position={[-0.5, 0.34, 0]} rotation={[0, -0.3, 0]}>
        <boxGeometry args={[0.3, 0.13, 1.25]} />
        <meshStandardMaterial color={stage === 1 ? "#aa4d5e" : "#a1a2b8"} />
      </mesh>
    </group>
  );
}
class CanvasBoundary extends Component<
  { children: ReactNode; fallback: ReactNode },
  { failed: boolean }
> {
  state = { failed: false };
  static getDerivedStateFromError() {
    return { failed: true };
  }
  render() {
    return this.state.failed ? this.props.fallback : this.props.children;
  }
}
export default function ValleyScene({
  stage,
  reduced,
}: {
  stage: number;
  reduced: boolean;
}) {
  const [lost, setLost] = useState(false);
  const [inspected, setInspected] = useState<string | null>(null);
  const [visible, setVisible] = useState(true);
  useEffect(() => {
    const update = () => setVisible(!document.hidden);
    document.addEventListener("visibilitychange", update);
    return () => document.removeEventListener("visibilitychange", update);
  }, []);
  if (lost) return <ValleyFallback stage={stage} />;
  return (
    <div className="scene-surface">
      <CanvasBoundary fallback={<ValleyFallback stage={stage} />}>
        <Canvas
          dpr={[1, 1.5]}
          camera={{ position: [11, 9, 13], fov: 37 }}
          frameloop={visible ? "demand" : "never"}
          gl={{ antialias: true, alpha: true, powerPreference: "low-power" }}
          onCreated={({ gl }) => {
            gl.domElement.addEventListener(
              "webglcontextlost",
              () => setLost(true),
              { once: true },
            );
          }}
          fallback={<ValleyFallback stage={stage} />}
          aria-label="Interactive 3D synthetic mountain valley"
        >
          <ambientLight intensity={0.65} />
          <directionalLight
            position={[-5, 10, 4]}
            intensity={2.8}
            color="#d1cfef"
          />
          <directionalLight
            position={[5, 5, -5]}
            intensity={3}
            color="#8460d4"
          />
          <pointLight position={[0, 3, 5]} intensity={8} color="#48d8f3" />
          <Suspense fallback={null}>
            <Landscape stage={stage} onInspect={setInspected} />
          </Suspense>
          {!reduced && <CameraMotion stage={stage} />}
          <OrbitControls
            makeDefault
            target={[0, 0.8, 0]}
            enableZoom={false}
            enablePan={false}
            enableDamping={!reduced}
            minPolarAngle={0.5}
            maxPolarAngle={1.25}
            minAzimuthAngle={-0.65}
            maxAzimuthAngle={1.25}
          />
        </Canvas>
      </CanvasBoundary>
      <div className="terrain-inspector" role="status" aria-live="polite">
        {inspected && (
          <span className="terrain-label selected">
            {inspected} · FICTIONAL INFRASTRUCTURE
          </span>
        )}
      </div>
    </div>
  );
}
