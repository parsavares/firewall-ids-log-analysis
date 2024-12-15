import React, { useState } from "react";


function ControlBar({labelsList, activeLabels, setActiveLabels}) {

  //const [activeLabels, setActiveLabels] = useState([...labelsList]);

    console.log(labelsList);
    // Function to handle toggle of priorities
    const togglePriority = (label) => {
      setActiveLabels((prev) => {
        const isActive = prev.includes(label);
        const updated = isActive
          ? prev.filter((p) => p !== label) // Remove the priority if it's active
          : [...prev, label]; // Add the priority if it's inactive
        return updated;
      });
    };

    if (labelsList === undefined || labelsList.length === 0 || labelsList === null) { 
      return null;
    }

    return (
        <div className="control-item">
          {labelsList.map((label) => (
            <button
              key={label}
              onClick={() => togglePriority(label)}>
              {label}{" "}
              {activeLabels.includes(label) ? "✔" : <span style={{ color: "red" }}>X</span>}
            </button>
          ))}
        </div>
    );
}

export default ControlBar;