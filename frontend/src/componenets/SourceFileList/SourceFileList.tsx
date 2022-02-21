import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import { SourceFileClient } from '../../api/source-file';
import { SourceFileProps } from '../../props';
import { SourceFile } from '../../types';

const SourceFileRow = ({ data }: SourceFileProps): JSX.Element => (
  <tr className="align-middle">
    <td>{data.id}</td>
    <td>{data.name}</td>
    <td>{data.path}</td>
    <td>{data.status}</td>
    <td>
      {data.file_exists ? (
        <i className="bi bi-check-circle text-success"></i>
      ) : (
        <i className="bi bi-x-circle text-danger"></i>
      )}
    </td>
    <td className="pe-0">
      {data.file_exists && (
        <button
          type="button"
          className="btn btn-sm btn-outline-success me-1"
          data-bs-toggle="modal"
          data-bs-target="#createNewTaskModal"
        >
          <i
            className="bi bi-plus"
            data-bs-toggle="tooltip"
            data-bs-placement="bottom"
            title="Create a new task for the source file."
          ></i>
        </button>
      )}
      <Link to={`/source_file/${data.id}`} className="btn btn-sm btn-outline-primary me-1">
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

export const SourceFileList = (): JSX.Element => {
  const [data, setData] = useState<SourceFile[]>([]);

  useEffect(() => {
    const sourceClient = new SourceFileClient();
    sourceClient.getSourceFiles().then(response => setData(response));
  }, []);

  return (
    <table className="table table-hover">
      <thead className="table-light">
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Path</th>
          <th>Status</th>
          <th>Exists</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        {data.map(row => (
          <SourceFileRow data={row} key={row.id} />
        ))}
      </tbody>
    </table>
  );
};
