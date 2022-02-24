import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Formik, Form, Field, FieldArray } from 'formik';

import { TaskClient } from '../../api/task';
import { Line, Point } from '../../types';
import { LineCanvas } from '../canvas';
import { LoadingView, PointBadge } from '../views';

type LinesFormProps = {
  lines: Line[];
  onClear: () => void;
  onSave: (lines: Line[]) => void;
};

const LinesForm = ({ lines, onClear, onSave }: LinesFormProps) => {
  return (
    <Formik initialValues={{ lines: lines }} enableReinitialize={true} onSubmit={values => onSave(values.lines)}>
      {({ values, handleSubmit }) => (
        <Form onSubmit={handleSubmit}>
          <div className="btn-group col-12">
            <button type="button" className="btn btn-outline-secondary" onClick={onClear}>
              Clear
            </button>
            <button type="submit" className="btn btn-outline-success">
              Save
            </button>
          </div>
          <FieldArray name="lines">
            {({ remove }) => (
              <div>
                {values.lines.map((line, index) => (
                  <div className="row row-cols-sm-auto g-3 align-items-center my-1" key={index}>
                    <div className="col-12">
                      <Field
                        className="form-control"
                        name={`lines[${index}].name`}
                        value={line.name}
                        placeholder={`Point ${index + 1}`}
                      />
                    </div>
                    <div className="col-12">
                      <div className="row mb-1">
                        <PointBadge point={line.start} />
                      </div>
                      <div className="row">
                        <PointBadge point={line.end} />
                      </div>
                    </div>
                    <button type="button" onClick={() => remove(index)}>
                      -
                    </button>
                  </div>
                ))}
              </div>
            )}
          </FieldArray>
        </Form>
      )}
    </Formik>
  );
};

export const TaskVisualization = () => {
  const client = new TaskClient();

  const { taskId } = useParams();
  const [image, setImage] = useState<string>();

  const [lines, setLines] = useState<Line[]>([]);
  const [singlePoint, setSinglePoint] = useState<Point | null>(null);

  useEffect(() => {
    if (taskId) client.getVisualization(parseInt(taskId)).then(data => setImage(URL.createObjectURL(data)));
  }, [taskId]);

  const createNewPoint = (point: Point) => {
    if (singlePoint) {
      setLines([...lines, { start: singlePoint, end: point, name: '' }]);
      setSinglePoint(null);
      return;
    }

    setSinglePoint(point);
  };

  const saveLines = (lines: Line[]) => {
    if (taskId) client.createLines(parseInt(taskId), lines).then(data => console.log(data));
  };

  return (
    <div className="row">
      <div className="col-9">
        {image ? <LineCanvas image={image} lines={lines} onClick={createNewPoint} /> : <LoadingView />}
      </div>

      <div className="col-3">
        <LinesForm lines={lines} onClear={() => setLines([])} onSave={lines => saveLines(lines)} />
      </div>
    </div>
  );
};
