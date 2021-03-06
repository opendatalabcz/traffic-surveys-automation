import { Link } from 'react-router-dom';
import { Field } from 'formik';
import Form from 'react-bootstrap/Form';
import { Point } from '../types';

type PointBadgeProps = {
  point: Point;
};

type FormRowProps = {
  title: string;
  name: string;
  as?: string;
  type?: string;
  children?: JSX.Element[];
};

type TitleViewProps = {
  title: string;
  backLink?: string;
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
    [{point.x.toFixed(0)}, {point.y.toFixed(0)}]
  </span>
);

export const FormRow = (props: FormRowProps): JSX.Element => (
  <Form.Group className="form-floating mb-3">
    <Field type={props.type} as={props.as} name={props.name} className={props.as ? 'form-select' : 'form-control'}>
      {props.children}
    </Field>
    <label htmlFor={props.name}>{props.title}</label>
  </Form.Group>
);

export const TitleView = ({ title, backLink }: TitleViewProps) => {
  return (
    <div className="d-flex align-items-center mb-3">
      {backLink && (
        <Link to={backLink} className="fs-5 me-2">
          <i className="bi bi-arrow-left-circle"></i>
        </Link>
      )}
      <span className="fs-2">{title}</span>
    </div>
  );
};
