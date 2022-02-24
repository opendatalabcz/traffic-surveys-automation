import React, { useEffect, useRef, useState } from 'react';
import { useResizeDetector } from 'react-resize-detector';
import { Line, Point } from '../types';

type LineCanvasProps = {
  image: string;
  lines: Line[];
  onClick: (point: Point) => void;
};

export const LineCanvas = ({ image, lines, onClick }: LineCanvasProps) => {
  const { width, height, ref } = useResizeDetector();

  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [ctx, setCtx] = useState<CanvasRenderingContext2D | null>();
  useEffect(() => setCtx(canvasRef.current?.getContext('2d')), [canvasRef]);

  useEffect(() => {
    if (!ctx) return;

    if (!lines.length) {
      ctx.clearRect(0, 0, width ?? 0, height ?? 0);
      return;
    }

    ctx.lineWidth = 6;

    lines.map(line => {
      ctx.beginPath();
      ctx.moveTo(line.start.x, line.start.y);
      ctx.lineTo(line.end.x, line.end.y);
      ctx.stroke();
    });
  }, [lines]);

  const draw = (event: React.MouseEvent) => {
    const offsets = canvasRef.current?.getBoundingClientRect();

    if (!offsets) return;

    onClick({ x: event.clientX - offsets.left, y: event.clientY - offsets.top });
  };

  return (
    <div className="position-relative user-select-none">
      <img ref={ref} src={image} className="position-absolute top-0 start-0 img-fluid" />
      <canvas
        width={width}
        height={height}
        ref={canvasRef}
        className="position-absolute top-0 start-0"
        onMouseDown={draw}
      ></canvas>
    </div>
  );
};
