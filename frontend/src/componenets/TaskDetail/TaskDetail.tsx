import { useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';
import CanvasDraw from 'react-canvas-draw';

import { TaskClient } from '../../api/task';
import { Task } from '../../types';

type VisualizationDetailProps = {
  client: TaskClient;
  taskId: number;
};

const VisualizationDetail = ({ client, taskId }: VisualizationDetailProps) => {
  const [image, setImage] = useState<string>();
  const canvas = useRef<CanvasDraw>(null);

  useEffect(() => {
    client.getVisualization(taskId).then(data => setImage(URL.createObjectURL(data)));
  }, [taskId]);

  return (
    <div className="col-12">
      <div className="btn-group offset-9 col-3 my-1">
        <button type="button" className="btn btn-outline-secondary" onClick={() => canvas.current?.clear()}>
          Clear
        </button>
        <button type="button" className="btn btn-outline-success">
          Save
        </button>
      </div>

      {image && (
        <CanvasDraw
          ref={canvas}
          imgSrc={image}
          hideGrid={true}
          brushColor="#00000"
          brushRadius={3}
          hideInterface={true}
          canvasWidth={1280}
          canvasHeight={720}
        />
      )}
      {!image && (
        <div className="d-flex justify-content-center">
          <div className="spinner-grow" style={{ width: '3rem', height: '3rem' }} role="loading">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      )}
    </div>
  );
};

export const TaskDetail = () => {
  const { taskId } = useParams();
  const taskClient = new TaskClient();

  const [data, setData] = useState<Task>();

  useEffect(() => {
    if (taskId !== undefined) taskClient.getTask(parseInt(taskId)).then(data => setData(data));
  }, [taskId]);

  return (
    <div className="col-12">
      {data && data.output_method == 'file' && <VisualizationDetail client={taskClient} taskId={data.id} />}
    </div>
  );
};
