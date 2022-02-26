import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { LinesClient } from '../../api/lines';
import { TaskClient } from '../../api/task';
import { Counts, Lines, Task } from '../../types';
import { PointBadge, TitleView } from '../views';
import { LinesCountsModal } from './LinesCountsModal';

type LinesRowProps = {
  data: Lines;
  onShowCounts: (linesId: number) => void;
  onDelete: (linesId: number) => void;
};

const LinesRow = ({ data, onShowCounts, onDelete }: LinesRowProps) => (
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
      <button type="button" className="btn btn-sm btn-outline-primary me-1" onClick={() => onShowCounts(data.id)}>
        <i className="bi bi-eye"></i>
        <span className="ms-1">Show</span>
      </button>
      <button type="button" className="btn btn-sm btn-outline-danger me-1" onClick={() => onDelete(data.id)}>
        <i className="bi bi-trash"></i>
        <span className="ms-1">Delete</span>
      </button>
    </td>
  </tr>
);

export const TaskDetail = () => {
  const { taskId } = useParams();
  const taskClient = new TaskClient();
  const linesClient = new LinesClient();

  const [data, setData] = useState<Task>();
  const [countsData, setCountsData] = useState<Counts>();

  useEffect(() => {
    if (taskId !== undefined) taskClient.getTask(parseInt(taskId)).then(data => setData(data));
  }, [taskId]);

  const showCounts = (linesId: number) => {
    linesClient.getCounts(linesId).then(data => setCountsData(data));
  };

  const deleteLinesRow = (linesId: number) => {
    if (data) {
      linesClient
        .delete(linesId)
        .then(() => setData({ ...data, lines: data.lines.filter(line => line.id != linesId) }));
    }
  };

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
            <LinesRow data={row} onShowCounts={showCounts} onDelete={deleteLinesRow} key={row.id} />
          ))}
        </tbody>
      </table>

      <LinesCountsModal data={countsData} handleClose={() => setCountsData(undefined)} />
    </div>
  );
};
