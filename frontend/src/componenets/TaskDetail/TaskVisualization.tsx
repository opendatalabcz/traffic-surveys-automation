import { useEffect, useState } from 'react';
// import CanvasDraw from 'react-canvas-draw';
import { useParams } from 'react-router-dom';
import { TaskClient } from '../../api/task';
import { Canvas } from '../canvas';
import { LoadingView } from '../views';

export const TaskVisualization = () => {
  const { taskId } = useParams();
  const client = new TaskClient();
  const [image, setImage] = useState<string>();
  // const canvas = useRef<CanvasDraw>(null);

  useEffect(() => {
    if (taskId) client.getVisualization(parseInt(taskId)).then(data => setImage(URL.createObjectURL(data)));
  }, [taskId]);

  return (
    <div className="row">
      <div className="col-9">{image ? <Canvas imageSrc={image} /> : <LoadingView />}</div>

      <div className="col-3">
        <div className="btn-group col-12">
          <button type="button" className="btn btn-outline-secondary">
            Clear
          </button>
          <button type="button" className="btn btn-outline-success">
            Save
          </button>
        </div>
      </div>

      {/* {image && (
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
      )} */}
    </div>
  );
};
