import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Table from 'react-bootstrap/Table';

import { Counts } from '../../types';

type LinesCountsModalProps = {
  data?: Counts;
  handleClose: () => void;
};

export const LinesCountsModal = ({ data, handleClose }: LinesCountsModalProps) => {
  const downloadCsv = () => {
    if (!data) return;

    let csvContent = 'Line,' + data.names.join(',') + '\n';
    csvContent += data.counts.map((counts, index) => data.names[index] + ',' + counts.join(',')).join('\n');

    const hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvContent);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'lines_count_export.csv';
    hiddenElement.click();
  };

  return (
    <Modal show={data !== undefined} onHide={handleClose} backdrop="static" keyboard={false} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>Vehicle counts</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Table>
          <tbody>
            <tr>
              <td className="border-bottom-0"></td>
              {data?.names.map(key => (
                <td className="fw-bold text-center border-bottom border-dark">{key}</td>
              ))}
            </tr>

            {data?.counts.map((innerList, index) => (
              <tr>
                <td className="fw-bold text-end border-end border-dark border-bottom-0">{data.names[index]}</td>

                {innerList.map((value, innerIndex) => (
                  <td className={`text-center ${innerIndex == index ? 'text-muted' : ''}`}>{value}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </Table>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        <Button variant="success" onClick={downloadCsv}>
          Download
        </Button>
      </Modal.Footer>
    </Modal>
  );
};
