import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";

import { filterPrioritiesIds} from "../../redux/DatasetSlice"; 

// Lista delle variabili numeriche
const numericVariables = [
  "3",
  "2",
  "1",
];


function ControlBar() {
  const dispatch = useDispatch();

  const priority = ["3", "2", "1"];
  const [activePriorities, setActivePriorities] = useState([...priority]);
  //const [isTickVisible, setIsTickVisible] = useState(true)
  const [isTickVisible1, setIsTickVisible1] = useState(true);
  const [isTickVisible2, setIsTickVisible2] = useState(true);
  const [isTickVisible3, setIsTickVisible3] = useState(true);




    // Function to handle toggle of priorities
    const togglePriority = (priority) => {
      setActivePriorities((prev) => {
        const isActive = prev.includes(priority);
        const updated = isActive
          ? prev.filter((p) => p !== priority) // Remove the priority if it's active
          : [...prev, priority]; // Add the priority if it's inactive
        dispatch(filterPrioritiesIds(updated)); // Dispatch updated priorities
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