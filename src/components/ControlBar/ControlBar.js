import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";

import { filterPrioriTiesParallel, filterPrioritiesFirewall} from "../../redux/DatasetSlice"; 

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

  const priority = ["Info", "Notice", "Critical", "Warning", "Error"];
  const [activePriorities, setActivePriorities] = useState([...priority]);
  //const [isTickVisible, setIsTickVisible] = useState(true)
  const [isTickVisible1, setIsTickVisible1] = useState(true);
  const [isTickVisible2, setIsTickVisible2] = useState(true);
  const [isTickVisible3, setIsTickVisible3] = useState(true);
  const [isTickVisible4, setIsTickVisible4] = useState(true);
  const [isTickVisible5, setIsTickVisible5] = useState(true);


  // Selectors
  const stackedbarchart_data_copy = useSelector((state) => state.state.stackedbarchart_data_copy);
  const heatmap_data_copy = useSelector((state) => state.state.heatmap_data_copy);
  const parallelsets_data_copy = useSelector((state) => state.state.parallelsets_data_copy);

  //Function to  priorities for stackedbarchart
  const handlePrioritiesFirewall = (event) => {
    const pass = ['Warning', 'Yes']
    dispatch(filterPrioritiesFirewall(pass));
    //dispatch(filterPrioritiesFirewall(event.target.value));
  };

    // Function to handle toggle of priorities
    const togglePriority = (priority) => {
      setActivePriorities((prev) => {
        const isActive = prev.includes(priority);
        const updated = isActive
          ? prev.filter((p) => p !== priority) // Remove the priority if it's active
          : [...prev, priority]; // Add the priority if it's inactive
        dispatch(filterPrioritiesFirewall(updated)); // Dispatch updated priorities
        return updated;
      });
    };


  return (


      <div className="control-item">
        {numericVariables.map((priority) => (
          <button
            key={priority}
            onClick={() => togglePriority(priority)}
          >
             {priority}{" "}
            {activePriorities.includes(priority) ? "✔" : <span style={{ color: "red" }}>X</span>}
          </button>
        ))}
      </div>


  );
}

export default ControlBar;