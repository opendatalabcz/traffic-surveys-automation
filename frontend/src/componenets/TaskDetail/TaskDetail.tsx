import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

import { TaskClient } from '../../api/task';
import { Lines, Task } from '../../types';
import { PointBadge, TitleView } from '../views';

type LinesRowProps = {
  data: Lines;
};

const LinesRow = ({ data }: LinesRowProps) => (
  <tr className="align-middle">
    <td>
      <div className="vstack gap-1 text-end">
        {data.lines.map((line, index) => (
          <span key={index}>{line.name}</span>
        ))}
      </div>
    </td>
    <td>
      <div className="vstack gap-2">
        {data.lines.map((line, index) => (
          <div className="hstack gap-1" key={index}>
            <PointBadge point={line.start} />
            <PointBadge point={line.end} />
          </div>
        ))}
      </div>
    </td>
    <td>
      <Link to={`/count/${data.id}`} className="btn btn-sm btn-outline-primary me-1">
        <i className="bi bi-eye"></i>
        <span className="ms-1">Show</span>
      </Link>
      <Link to={`/count/${data.id}`} className="btn btn-sm btn-outline-info me-1">
        <i className="bi bi-cloud-arrow-down"></i>
        <span className="ms-1">Download</span>
      </Link>
      <Link to={`/count/${data.id}`} className="btn btn-sm btn-outline-danger me-1">
        <i className="bi bi-trash"></i>
        <span className="ms-1">Delete</span>
      </Link>
    </td>
  </tr>
);

export const TaskDetail = () => {
  const { taskId } = useParams();
  const taskClient = new TaskClient();

  const [data, setData] = useState<Task>();

  useEffect(() => {
    if (taskId !== undefined) taskClient.getTask(parseInt(taskId)).then(data => setData(data));
  }, [taskId]);

  return (
    <div>
      <TitleView title="Task lines" backLink={`/source_file/${data?.source_file_id}`} />

      <div className="d-flex justify-content-end my-1">
        <Link to={`/task/${data?.id}/visualization`} className="btn btn-outline-success">
          <i className="bi bi-plus"></i>
          New visualization
        </Link>
      </div>

      <table className="table">
        <thead className="table-light">
          <tr>
            <th>Name</th>
            <th>Points</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {data?.lines.map(row => (
            <LinesRow data={row} key={row.id} />
          ))}
        </tbody>
      </table>
    </div>
  );
};
