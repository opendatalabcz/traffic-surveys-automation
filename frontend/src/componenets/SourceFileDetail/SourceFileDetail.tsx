import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

import { SourceFileClient } from '../../api/source-file';
import { TaskStatus } from '../../enums';
import { DetectionModelMapping, SourceFileTaskColorMapping, TrackingModelMapping } from '../../mappings';
import { SourceFileWithTasks, Task } from '../../types';
import { LoadingView, TitleView } from '../views';

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
    <td className="text-end">{data.status}</td>
    <td className="text-end">
      {data.status == TaskStatus.completed && (
        <div>
          <Link to={`/task/${data.id}`} className="btn btn-sm btn-outline-primary me-1">
            <i className="bi bi-distribute-vertical"></i>
            <span className="ms-1">Lines</span>
          </Link>
          <Link to={`/task/${data.id}`} className="btn btn-sm btn-outline-primary me-1">
            <i className="bi bi-play"></i>
            <span className="ms-1">Play</span>
          </Link>
        </div>
      )}
    </td>
  </tr>
);

const Detail = ({ data }: DetailProps) => (
  <div>
    <div className="d-flex align-items-center">
      <span className="fs-4 fw-bold me-1">{data.name}</span>
      <span className="fs-5 text-muted me-1">{data.path}</span>
      <span className={`fs-6 badge ${SourceFileTaskColorMapping[data.status]}`}>{data.status}</span>
    </div>

    <table className="table table-hover">
      <thead className="table-light">
        <tr>
          <th>#</th>
          <th>Models</th>
          <th className="text-end">Status</th>
          <th className="text-end">Actions</th>
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

  return (
    <div>
      <TitleView title="Source file detail" backLink="/" />

      {data ? <Detail data={data} /> : <LoadingView />}
    </div>
  );
};
