import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

import { SourceFileClient } from '../../api/source-file';
import { SourceFileWithTasks, Task } from '../../types';

type DetailProps = {
  data: SourceFileWithTasks;
};

type TaskRowProps = {
  data: Task;
};

const TaskRow = ({ data }: TaskRowProps) => (
  <tr className="align-middle">
    <td>{data.id}</td>
    <td>
      {data.models[0]}, {data.models[1]}
    </td>
    <td>{data.output_method}</td>
    <td>{data.status}</td>
    <td className="pe-0">
      <Link to={`/task/${data.id}`} className="btn btn-sm btn-outline-primary me-1">
        <i
          className="bi bi-search"
          data-bs-toggle="tooltip"
          data-bs-placement="top"
          title="Show source file details."
        ></i>
      </Link>
      <button className="btn btn-sm btn-outline-danger">
        <i className="bi bi-trash" data-bs-toggle="tooltip" data-bs-placement="top" title="Delete the source file."></i>
      </button>
    </td>
  </tr>
);

const Detail = ({ data }: DetailProps) => (
  <div className="col-12">
    <h3>Source file: {data.name}</h3>
    <h4>
      Path: {data.path}, Status: {data.status}
    </h4>
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
  const { id } = useParams();

  const [data, setData] = useState<SourceFileWithTasks>();

  useEffect(() => {
    const sourceClient = new SourceFileClient();

    if (id !== undefined) sourceClient.getSourceFile(parseInt(id)).then(data => setData(data));
  }, [id]);

  if (data !== undefined) return <Detail data={data} />;

  return <React.Fragment />;
};
