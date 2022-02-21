// import { Formik } from 'formik';
// import { SourceFileProps } from '../../props';

// const ModalHeader = (): JSX.Element => (
//   <div className="modal-header">
//     <h5 className="modal-title">Create new task</h5>
//   </div>
// );

export type FormRowProps = {
  title: string;
  name: string;
  content: JSX.Element;
};

// const FormRow = ({ title, name, content }: FormRowProps): JSX.Element => (
//   <div className="mb-3 form-floating">
//     {content}
//     <label htmlFor={name}>{title}</label>
//   </div>
// );

// export const NewTaskModal = ({ data }: SourceFileProps) => {
//   const initialValues = {outputMethod: 'file', detectionModel: 'efficentdet_d6', trackingModel: 'simple_sort', parameters: {}};

//   return (<div id="createNewTaskModal" className="modal fade" data-bs-backdrop="static" data-bs-keyboard="false">
//     <div className="modal-dialog modal-lg">
//       <div className="modal-content">
//         <Formik
//           initialValues={initialValues}
//           validate={}
//           onSubmit={}
//         >
//           {({
//             values,
//             errors,
//             touched,
//             handleChange,
//             handleBlur,
//             handleSubmit,
//             isSubmitting,
//             /* and other goodies */
//           }) => (
//             <form onSubmit={handleSubmit}>
//               <ModalHeader />

//               <div className="modal-body">
//                 <FormRow title="Output type" name=outputMethod">
//                   <select className="form-select" id="formOutputType" name="output_method">
//                     <option value="file">File</option>
//                     <option value="video">Video</option>
//                   </select>
//                 </FormRow>

//                 <div className="mb-3 form-floating">
//                   <select className="form-select" id="formDetectionModel" name="detection_model">
//                     <option value="efficientdet_d6">EfficientDet D6</option>
//                     <option value="efficientdet_d5_adv_prop">EfficientDet D5 AdvProp</option>
//                   </select>
//                   <label htmlFor="formDetectionModel">Detection model</label>
//                 </div>

//                 <div className="mb-3 form-floating">
//                   <select className="form-select" id="formTrackingModel" name="tracking_model">
//                     <option value="simple_sort">Simple SORT</option>
//                     <option value="deep_sort">Deep SORT</option>
//                   </select>
//                   <label htmlFor="formTrackingModel">Tracking model</label>
//                 </div>

//                 <div className="mb-3 form-floating">
//                   <input type="text" className="form-control" id="formParameters" name="parameters" value="{}" />
//                   <label htmlFor="formParameters">Parameters</label>
//                 </div>
//               </div>

//               <div className="modal-footer">
//                 <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">
//                   Close
//                 </button>
//                 <button type="submit" className="btn btn-success">
//                   Create
//                 </button>
//               </div>
//             </form>
//           )}
//         </Formik>
//       </div>
//     </div>
//   </div>
// )
// };
