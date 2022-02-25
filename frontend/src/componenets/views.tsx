import { Link } from 'react-router-dom';
import { Point } from '../types';

type PointBadgeProps = {
  point: Point;
};

type TitleViewProps = {
  title: string;
  backLink: string;
};

export const LoadingView = () => (
  <div className="d-flex justify-content-center">
    <div className="spinner-grow" style={{ width: '2rem', height: '2rem' }} role="loading">
      <span className="visually-hidden">Loading...</span>
    </div>
  </div>
);

export const PointBadge = ({ point }: PointBadgeProps) => (
  <span className="badge bg-secondary">
    [{point.x.toFixed(1)}, {point.y.toFixed(1)}]
  </span>
);

export const TitleView = ({ title, backLink }: TitleViewProps) => {
  return (
    <div className="d-flex align-items-center mb-3">
      <Link to={backLink} className="fs-5 me-2">
        <i className="bi bi-arrow-left-circle"></i>
      </Link>
      <span className="fs-2">{title}</span>
    </div>
  );
};
