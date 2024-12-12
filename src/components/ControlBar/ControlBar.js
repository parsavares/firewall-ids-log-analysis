import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { filterPrioriTiesParallel, filterPrioritiesStacked} from "../../redux/DatasetSlice"; 

// Lista delle variabili numeriche
const numericVariables = [
  "Info",
  "Notice",
  "Critical",
  "Warning",
  "Error"
];


function ControlBar() {
  const dispatch = useDispatch();

  // Selectors
  const stackedbarchart_data_copy = useSelector((state) => state.state.stackedbarchart_data_copy);
  const heatmap_data_copy = useSelector((state) => state.state.heatmap_data_copy);
  const parallelsets_data_copy = useSelector((state) => state.state.parallelsets_data_copy);

  //Function to  priorities for stackedbarchart
  const handlePrioritiesStacked = (event) => {
    dispatch(filterPrioritiesStacked(event.target.value));
  };

  
  //const handleYAxisChange = (event) => {
  //  dispatch(setYAxis(event.target.value)); 
  //};

  return (
    <div className="control-bar">
      <div className="control-item">
        <label htmlFor="xAxisSelect">Select priorities:</label>
        <select id="xAxisSelect" value={stackedbarchart_data_copy} onChange={handlePrioritiesStacked}>
          {numericVariables.map((variable) => (
            <option key={variable} value={variable}>
              {variable}
            </option>
          ))}
        </select>
      </div>

      
      
    </div>
  );
}

export default ControlBar;