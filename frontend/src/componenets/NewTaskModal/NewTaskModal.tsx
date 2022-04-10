import { Form as FormikForm, Formik, useField } from 'formik';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Modal from 'react-bootstrap/Modal';
import { DetectionModel, TrackingModel } from '../../enums';
import { useTaskConfiguration } from '../../hooks';
import { DetectionModelMapping, TrackingModelMapping } from '../../mappings';
import { SourceFile } from '../../types';
import { FormRow } from '../views';

type InitialValuesProps = {
  name: string;
  detectionModel: string;
  trackingModel: string;
  parameters: { [id: string]: string };
};

type SourceFileProps = {
  data?: SourceFile;
  handleClose: () => void;
  handleSave: (sourceFileId: number, values: InitialValuesProps) => void;
};

type ParametersPickerProps = {
  onFieldChange: (fieldName: string, value: number) => void;
};

const ParametersPicker = ({ onFieldChange }: ParametersPickerProps) => {
  const config = useTaskConfiguration();
  const [field] = useField<{ [id: string]: string }>('parameters');

  return (
    <div className="border rounded px-2 py-2">
      {Object.entries(config)
        .sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0))
        .map((value, index) => (
          <InputGroup size="sm" className="mb-3" key={index}>
            <InputGroup.Text className="col-5">{value[0]}</InputGroup.Text>
            <Form.Control
              type="number"
              value={field.value[value[0]] ?? value[1] ?? 0}
              onChange={event => onFieldChange(value[0], event.target.value as unknown as number)}
            />
          </InputGroup>
        ))}
    </div>
  );
};

export const NewTaskModal = ({ data, handleClose, handleSave }: SourceFileProps) => {
  const initialValues: InitialValuesProps = {
    name: data?.name ?? '',
    detectionModel: DetectionModel.efficientdet_d6.toString(),
    trackingModel: TrackingModel.simple_sort.toString(),
    parameters: {},
  };

  const generateOptions = (mapping: { [id: string]: string }) =>
    Object.entries(mapping).map((value, index) => (
      <option value={value[0]} key={index}>
        {value[1]}
      </option>
    ));

  return (
    <Formik initialValues={initialValues} enableReinitialize={true} onSubmit={values => handleSave(data!.id, values)}>
      {({ handleSubmit, setFieldValue }) => (
        <Modal show={data !== undefined} onHide={handleClose} backdrop="static" keyboard={false} size="lg">
          <Modal.Header closeButton>
            <Modal.Title>New task</Modal.Title>
          </Modal.Header>
          <FormikForm onSubmit={handleSubmit}>
            <Modal.Body>
              <FormRow title="Name" name="name" type="text"></FormRow>

              <FormRow title="Detection model" name="detectionModel" as="select">
                {generateOptions(DetectionModelMapping)}
              </FormRow>

              <FormRow title="Tracking model" name="trackingModel" as="select">
                {generateOptions(TrackingModelMapping)}
              </FormRow>

              <ParametersPicker onFieldChange={(field, value) => setFieldValue(`parameters.${field}`, value)} />
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={handleClose}>
                Close
              </Button>
              <Button variant="success" type="submit">
                Create
              </Button>
            </Modal.Footer>
          </FormikForm>
        </Modal>
      )}
    </Formik>
  );
};
