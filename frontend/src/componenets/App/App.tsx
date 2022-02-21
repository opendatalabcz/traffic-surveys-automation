import { BrowserRouter as Router, Link, Routes, Route, useLocation } from 'react-router-dom';
import { SourceFileDetail } from '../SourceFileDetail/SourceFileDetail';

import { SourceFileList } from '../SourceFileList/SourceFileList';
import { TaskDetail } from '../TaskDetail/TaskDetail';

const Header = () => {
  const location = useLocation();

  return (
    <div id="header" className="row col-12 my-1">
      <h2 className="col-6">Traffic Survey Automator</h2>

      <div className="col-6">
        <ul className="nav nav-pills justify-content-end">
          <li className="nav-item">
            <Link to="/" className={`nav-link ${location.pathname == '/' ? 'active' : ''}`}>
              Home
            </Link>
          </li>
        </ul>
      </div>
    </div>
  );
};

const Content = () => (
  <Routes>
    <Route path="/" element={<SourceFileList />} />
    <Route path="/source_file/:id" element={<SourceFileDetail />} />
    <Route path="/task/:taskId" element={<TaskDetail />} />
  </Routes>
);

export const App = () => (
  <Router>
    <div className="container">
      <Header />

      <div id="content" className="row col-md-12">
        <Content />
      </div>
    </div>
  </Router>
);
