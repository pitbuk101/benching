import { useRef, useEffect, useState } from 'react';
import { geoOrthographic, geoPath, Timer, timer as timerFun } from 'd3';
import worldCords from './worldCords.json';

interface RotatingEarthProps {
  rotationSpeed?: number;
}

const RotatingEarth: React.FC<RotatingEarthProps> = ({
  rotationSpeed = 0.02,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const [hoveredCountry, setHoveredCountry] = useState<{
    name: string;
    savings: string;
  } | null>(null);
  const [mousePosition, setMousePosition] = useState<{
    x: number;
    y: number;
  } | null>(null);

  // 🔥 Store fixed savings values using useRef so they remain constant
  const savingsOpportunities = useRef<Record<string, string>>({
    'United States': '10%',
    China: '1%',
    India: '20%',
    Germany: '15.20%',
    Brazil: '17.20%',
    Russia: '5%',
    Canada: '80%',
    Australia: '90%',
  });

  useEffect(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    if (!context) return;

    const width = canvas.clientWidth;
    const height = canvas.clientHeight;

    canvas.width = width * window.devicePixelRatio;
    canvas.height = height * window.devicePixelRatio;
    context.scale(window.devicePixelRatio, window.devicePixelRatio);

    const projection = geoOrthographic()
      .scale(Math.min(width, height) / 2.5)
      .translate([width / 2, height / 2])
      .precision(0.5);

    const path = geoPath(projection, context);
    const world = worldCords;

    let timer: Timer | null = null;

    // 🌍 Animation Loop
    timer = timerFun(() => {
      if (!context) return;
      context.clearRect(0, 0, width, height);

      projection.rotate([Date.now() * rotationSpeed, -15]);

      context.beginPath();
      path({ type: 'Sphere' });
      context.fillStyle = '#222222';
      context.fill();

      context.beginPath();
      path({ type: 'Sphere' });
      context.strokeStyle = '#000';
      context.lineWidth = 0.5;
      context.stroke();

      let foundCountry: { name: string; savings: string } | null = null;

      world.features.forEach((feature: any) => {
        context.beginPath();
        path(feature);
        context.fillStyle = '#1666ff';
        context.fill();
        context.strokeStyle = '#333';
        context.stroke();

        const countryName = feature.properties.name;
        if (savingsOpportunities.current[countryName]) {
          const centroid = path.centroid(feature);
          if (centroid && !isNaN(centroid[0]) && !isNaN(centroid[1])) {
            context.fillStyle = 'white';
            context.font = `${Math.max(width / 80, 10)}px sans-serif`;
            context.textAlign = 'center';
            context.fillText(
              `${countryName} (${savingsOpportunities.current[countryName]})`,
              centroid[0],
              centroid[1],
            );
          }
        }

        // ✅ Detect Hovered Country
        if (
          mousePosition &&
          context.isPointInPath(mousePosition.x, mousePosition.y)
        ) {
          foundCountry = {
            name: countryName,
            savings: savingsOpportunities.current[countryName],
          };
        }
      });

      setHoveredCountry(foundCountry);
    });

    // ✅ Mouse Move Handler
    const handleMouseMove = (event: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      setMousePosition({
        x: (event.clientX - rect.left) * window.devicePixelRatio,
        y: (event.clientY - rect.top) * window.devicePixelRatio,
      });
    };

    canvas.addEventListener('mousemove', handleMouseMove);

    return () => {
      if (timer) timer.stop();
      canvas.removeEventListener('mousemove', handleMouseMove);
    };
  }, [rotationSpeed, mousePosition]);

  // ✅ Tooltip Positioning
  useEffect(() => {
    if (tooltipRef.current && hoveredCountry) {
      tooltipRef.current.style.left = `${mousePosition?.x ?? 0 / window.devicePixelRatio + 10}px`;
      tooltipRef.current.style.top = `${mousePosition?.y ?? 0 / window.devicePixelRatio + 10}px`;
    }
  }, [hoveredCountry, mousePosition]);

  return (
    <div className="earth-container" style={{ position: 'relative' }}>
      <canvas ref={canvasRef} />
      <div
        ref={tooltipRef}
        className="tooltip"
        style={{
          position: 'absolute',
          padding: '6px',
          background: 'rgba(0, 0, 0, 0.7)',
          color: '#fff',
          borderRadius: '4px',
          fontSize: '12px',
          pointerEvents: 'none',
          opacity: hoveredCountry ? 1 : 0,
          transition: 'opacity 0.2s',
        }}
      >
        {hoveredCountry && (
          <>
            <strong>{hoveredCountry.name}</strong>
            <br />
            Savings Opportunity: {hoveredCountry.savings}
          </>
        )}
      </div>
    </div>
  );
};

export default RotatingEarth;
