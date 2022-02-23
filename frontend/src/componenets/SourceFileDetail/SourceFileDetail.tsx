import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

import { SourceFileClient } from '../../api/source-file';
import { OutputType, TaskStatus } from '../../enums';
import { DetectionModelMapping, TrackingModelMapping } from '../../mappings';
import { SourceFileWithTasks, Task } from '../../types';

type DetailProps = {
  data: SourceFileWithTasks;
};

type TaskRowProps = {
  data: Task;
};

const TaskRow = ({ data }: TaskRowProps) => (
  <tr className={`align-middle ${data.status != TaskStatus.completed && 'table-secondary'}`}>
    <td>{data.id}</td>
    <td>
      <span className="badge bg-primary me-1">{DetectionModelMapping[data.models[0]]}</span>
      <span className="badge bg-secondary">{TrackingModelMapping[data.models[1]]}</span>
    </td>
    <td>{data.output_method}</td>
    <td>{data.status}</td>
    <td>
      {data.output_method == OutputType.file && data.status == TaskStatus.completed && (
        <Link to={`/task/${data.id}`} className="btn btn-sm btn-outline-primary me-1">
          <i className="bi bi-distribute-vertical"></i>
          <span className="ms-1">Lines</span>
        </Link>
      )}
      {data.output_method == OutputType.video && data.status == TaskStatus.completed && (
        <Link to={`/task/${data.id}`} className="btn btn-sm btn-outline-primary me-1">
          <i className="bi bi-play"></i>
          <span className="ms-1">Play</span>
        </Link>
      )}
    </td>
  </tr>
);

const Detail = ({ data }: DetailProps) => (
  <div className="col-12">
    <h3>Source file detail</h3>
    <h5>
      Name: {data.name}, Path: {data.path}, Status: {data.status}
    </h5>
    <table className="table table-hover">
      <thead className="table-light">
        <tr>
          <th>#</th>
          <th>Models</th>
          <th>Method</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        {data.tasks.map(row => (
          <TaskRow data={row} key={row.id} />
        ))}
      </tbody>
    </table>
  </div>
);

export const SourceFileDetail = () => {
  const sourceClient = new SourceFileClient();
  const { id } = useParams();

  const [data, setData] = useState<SourceFileWithTasks>();

  useEffect(() => {
    if (id !== undefined) sourceClient.getSourceFile(parseInt(id)).then(data => setData(data));
  }, [id]);

  return <div className="md-12">{data && <Detail data={data} />}</div>;
};
