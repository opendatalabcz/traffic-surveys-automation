import { Point } from '../types';

type PointBadgeProps = {
  point: Point;
};

export const LoadingView = () => (
  <div className="d-flex justify-content-center">
    <div className="spinner-grow" style={{ width: '3rem', height: '3rem' }} role="loading">
      <span className="visually-hidden">Loading...</span>
    </div>
  </div>
);

export const PointBadge = ({ point }: PointBadgeProps) => (
  <span className="badge bg-secondary">
    [{point.x.toFixed(1)}, {point.y.toFixed(1)}]
  </span>
);
