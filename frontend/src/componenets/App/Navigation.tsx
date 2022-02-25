import { Link, useLocation } from 'react-router-dom';

export const Navigation = () => {
  const location = useLocation();

  return (
    <ul className="nav nav-pills justify-content-end">
      <li className="nav-item">
        <Link to="/" className={`nav-link ${location.pathname == '/' ? 'active' : ''}`}>
          Source files
        </Link>
      </li>
    </ul>
  );
};
