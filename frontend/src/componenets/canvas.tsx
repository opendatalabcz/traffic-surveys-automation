import React, { useEffect, useRef, useState } from 'react';
import { useResizeDetector } from 'react-resize-detector';
import { useImageSize } from '../hooks';
import { Line, Point } from '../types';

type LineCanvasProps = {
  image: string;
  lines: Line[];
  onNewLine: (line: Line) => void;
};

export const LineCanvas = ({ image, lines, onNewLine }: LineCanvasProps) => {
  const { width, height, ref } = useResizeDetector<HTMLImageElement>();
  const { imageRelativeSize } = useImageSize(ref.current, width);

  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [ctx, setCtx] = useState<CanvasRenderingContext2D | null>();
  useEffect(() => setCtx(canvasRef.current?.getContext('2d')), [canvasRef]);

  const [unpairedPoint, setUnpairdPoint] = useState<Point | null>(null);

  useEffect(() => {
    if (!ctx) return;

    if (!lines.length) {
      ctx.clearRect(0, 0, width ?? 0, height ?? 0);
      return;
    }

    ctx.lineWidth = 6;

    lines.map(line => {
      ctx.beginPath();
      ctx.moveTo(line.start.displayX!, line.start.displayY!);
      ctx.lineTo(line.end.displayX!, line.end.displayY!);
      ctx.stroke();
    });
  }, [lines]);

  const createNewPoint = (point: Point) => {
    if (unpairedPoint) {
      onNewLine({ start: unpairedPoint, end: point, name: '' });
      setUnpairdPoint(null);
      return;
    }

    setUnpairdPoint(point);
  };

  const onCreateNewPoint = (event: React.MouseEvent) => {
    const offsets = canvasRef.current?.getBoundingClientRect();

    if (!offsets || !imageRelativeSize) return;

    createNewPoint({
      x: (event.clientX - offsets.left) * imageRelativeSize,
      y: (event.clientY - offsets.top) * imageRelativeSize,
      displayX: event.clientX - offsets.left,
      displayY: event.clientY - offsets.top,
    });
  };

  return (
    <div className="position-relative user-select-none">
      <img ref={ref} src={image} className="position-absolute top-0 start-0 img-fluid" />
      <canvas
        width={width}
        height={height}
        ref={canvasRef}
        className="position-absolute top-0 start-0"
        onMouseDown={onCreateNewPoint}
      ></canvas>
    </div>
  );
};
