import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Formik, Form, Field, FieldArray } from 'formik';
import * as Yup from 'yup';

import { TaskClient } from '../../api/task';
import { Line } from '../../types';
import { LineCanvas } from '../canvas';
import { PointBadge, LoadingView, TitleView } from '../views';

type FormValues = {
  lines: Line[];
};

const FormSchema = Yup.object().shape({
  lines: Yup.array()
    .of(
      Yup.object().shape({
        name: Yup.string().required('Name is required.'),
        start: Yup.object().required('Start point is required.'),
        end: Yup.object().required('End point is required.'),
      })
    )
    .required('Must have lines.')
    .min(1, 'You have to draw at least one line.'),
});

export const TaskVisualization = () => {
  const client = new TaskClient();
  const navigation = useNavigate();
  const formInitialValues: FormValues = { lines: [] };

  const { taskId } = useParams();
  const [image, setImage] = useState<string>();

  useEffect(() => {
    if (taskId) client.getVisualization(parseInt(taskId)).then(data => setImage(URL.createObjectURL(data)));
  }, [taskId]);

  const saveLines = (lines: Line[]) => {
    if (taskId) client.createLines(parseInt(taskId), lines).then(() => navigation(`/task/${taskId}`));
  };

  return (
    <div>
      <TitleView title="New visualization" backLink={`/task/${taskId}`} />

      <Formik
        initialValues={formInitialValues}
        validationSchema={FormSchema}
        onSubmit={values => saveLines(values.lines)}
      >
        {({ values, isValid, isSubmitting, dirty, handleSubmit, setFieldValue }) => (
          <Form onSubmit={handleSubmit}>
            <FieldArray name="lines">
              {({ push }) => (
                <div className="row">
                  <div className="col-9">
                    {image ? <LineCanvas image={image} lines={values.lines} onNewLine={push} /> : <LoadingView />}
                  </div>

                  <div className="col-3">
                    <div className="btn-group col-12">
                      <button
                        type="button"
                        className="btn btn-outline-secondary"
                        onClick={() => setFieldValue('lines', [])}
                      >
                        Clear
                      </button>
                      <button
                        type="submit"
                        className="btn btn-outline-success"
                        disabled={!dirty || !isValid || isSubmitting}
                      >
                        Save
                      </button>
                    </div>

                    {values.lines.map((line, index) => (
                      <div className="hstack gap-1 my-2" key={index}>
                        <Field
                          className="form-control"
                          name={`lines[${index}].name`}
                          value={line.name}
                          placeholder={`Line ${index + 1}`}
                        />
                        <div className="vstack gap-1">
                          <PointBadge point={line.start} />
                          <PointBadge point={line.end} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </FieldArray>
          </Form>
        )}
      </Formik>
    </div>
  );
};
