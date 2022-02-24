import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

import { TaskClient } from '../../api/task';
import { Lines, Task } from '../../types';
import { PointBadge } from '../views';

type LinesRowProps = {
  data: Lines;
};

const LinesRow = ({ data }: LinesRowProps) => (
  <tr className="align-middle">
    <td>
      <ul className="list-group list-group-horizontal">
        {data.lines.map(line => (
          <li className="list-group-item">{line.name}</li>
        ))}
      </ul>
    </td>
    <td>
      <ul className="list-group list-group-horizontal">
        {data.lines.map(line => (
          <li className="list-group-item">
            <PointBadge point={line.start} />
            <PointBadge point={line.end} />
          </li>
        ))}
      </ul>
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
      <div className="row my-1">
        <h3 className="col-6">Task lines</h3>

        <ul className="nav justify-content-end col-6">
          <li className="nav-item">
            <Link to={`/task/${data?.id}/visualization`} className="btn btn-outline-success">
              <i className="bi bi-plus"></i>
              New visualization
            </Link>
          </li>
        </ul>
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
