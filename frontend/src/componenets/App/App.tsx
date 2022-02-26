import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { SourceFileDetail } from '../SourceFileDetail/SourceFileDetail';

import { SourceFileList } from '../SourceFileList/SourceFileList';
import { TaskDetail } from '../TaskDetail/TaskDetail';
import { TaskVisualization } from '../TaskDetail/TaskVisualization';
import { Navigation } from './Navigation';

const Header = () => {
  return (
    <div id="header" className="d-flex align-items-center row py-1">
      <p className="col-6 justify-content-start display-6 my-0">Traffic Survey Automator</p>

      <div className="col-6 justify-content-end">
        <Navigation />
      </div>
    </div>
  );
};

const Content = () => (
  <Routes>
    <Route path="/" element={<SourceFileList />} />
    <Route path="/source_file/:id" element={<SourceFileDetail />} />
    <Route path="/task/:taskId" element={<TaskDetail />} />
    <Route path="/task/:taskId/visualization" element={<TaskVisualization />} />
  </Routes>
);

export const App = () => (
  <Router>
    <div className="container">
      <Header />

      <div id="content">
        <Content />
      </div>
    </div>
  </Router>
);
