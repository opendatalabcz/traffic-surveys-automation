import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import { SourceFileClient } from '../../api/source-file';
import { SourceFile } from '../../types';
import { NewTaskModal } from '../NewTaskModal/NewTaskModal';
import { TitleView } from '../views';

type SourceFileRowProps = {
  data: SourceFile;
  onCreateNewTask: (sourceFile: SourceFile) => void;
};

const SourceFileRow = ({ data, onCreateNewTask }: SourceFileRowProps): JSX.Element => (
  <tr className="align-middle">
    <td>{data.id}</td>
    <td>{data.name}</td>
    <td>{data.path}</td>
    <td className="text-end">{data.status}</td>
    <td className="text-end">
      {data.file_exists ? (
        <i className="bi bi-check-circle text-success"></i>
      ) : (
        <i className="bi bi-x-circle text-danger"></i>
      )}
    </td>
    <td className="text-end">
      {data.file_exists && (
        <button type="button" className="btn btn-sm btn-outline-success me-1" onClick={() => onCreateNewTask(data)}>
          <i className="bi bi-plus"></i>
          <span className="ms-1">New task</span>
        </button>
      )}
      <Link to={`/source_file/${data.id}`} className="btn btn-sm btn-outline-primary me-1">
        <i className="bi bi-search"></i>
        <span className="ms-1">Detail</span>
      </Link>
    </td>
  </tr>
);

export const SourceFileList = (): JSX.Element => {
  const sourceClient = new SourceFileClient();

  const [data, setData] = useState<SourceFile[]>([]);
  const [newTaskSourceFile, setNewTaskSourceFile] = useState<SourceFile>();

  const readSourceFiles = () => {
    sourceClient.getSourceFiles().then(response => setData(response));
  };

  const discoverSourceFiles = () => {
    sourceClient.discoverSourceFiles().then(data => setData(data));
  };

  useEffect(readSourceFiles, []);

  return (
    <div>
      <TitleView title="All source files" />

      <div className="d-flex justify-content-end my-1">
        <button type="button" className="btn btn-outline-success" onClick={discoverSourceFiles}>
          <i className="bi bi-search me-1"></i>
          Discover source files
        </button>
      </div>

      <table className="table table-hover">
        <thead className="table-light">
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Path</th>
            <th className="text-end">Status</th>
            <th className="text-end">Exists</th>
            <th className="text-end">Actions</th>
          </tr>
        </thead>

        <tbody>
          {data.map(row => (
            <SourceFileRow data={row} onCreateNewTask={data => setNewTaskSourceFile(data)} key={row.id} />
          ))}
        </tbody>
      </table>

      <NewTaskModal
        data={newTaskSourceFile}
        handleClose={() => setNewTaskSourceFile(undefined)}
        handleSave={(id, values) =>
          sourceClient
            .createTask(
              id,
              values.name,
              values.detectionModel,
              values.trackingModel,
              values.outputMethod,
              values.parameters
            )
            .then(() => setNewTaskSourceFile(undefined))
        }
      />
    </div>
  );
};
