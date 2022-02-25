import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { SourceFileDetail } from '../SourceFileDetail/SourceFileDetail';

import { SourceFileList } from '../SourceFileList/SourceFileList';
import { TaskDetail } from '../TaskDetail/TaskDetail';
import { TaskVisualization } from '../TaskDetail/TaskVisualization';
import { Navigation } from './Navigation';

const Header = () => {
  return (
    <div id="header" className="row col-12 my-1">
      <h2 className="col-6">Traffic Survey Automator</h2>

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
