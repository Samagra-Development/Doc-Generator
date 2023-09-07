import React, { useState } from 'react';
import styles from '../styles/templateOverlay.module.css';

const templateData = [
  { heading: 'Template 1', text: 'This is template 1.' },
  { heading: 'Template 2', text: 'This is template 2.' },
];
const TemplateOverlay = ({ onClose, existingTemplates, onTemplateSelect }) => {
  const editBox = (index) => {
    console.log(`Editing box ${index}`);
  };

  const deleteBox = (index) => {
    const updatedBoxes = [...boxes];
    updatedBoxes.splice(index, 1);
    setBoxes(updatedBoxes);
  };

  const hideOverlay = () => {
    onClose();
  };

  return (
    <div className={styles.overlay} onClick={hideOverlay}>
      <div
        className={styles.overlayContent}
        onClick={(e) => e.stopPropagation()}
      >
        <h2>Choose from Existing Templates</h2>
        <button className={styles.closeButton} onClick={onClose}>
          &times;
        </button>
        <div className={styles.boxContainer}>
          {existingTemplates.map((template, index) => (
            <div
              key={index}
              className={styles.box}
              onClick={() => {
                onTemplateSelect(template.id);
                onClose();
              }}
            >
              <div className={styles.boxHeader}>
                <button onClick={() => editBox(index)}>Edit</button>
                <button onClick={() => deleteBox(index)}>Delete</button>
              </div>
              <h3>{template.id}</h3>
              <p>{template.content}</p>
              <h4>{template.templatType}</h4>
            </div>
          ))}
        </div>
        <div className={styles.blueLine}></div>
        <div className={styles.viewMoreText}>View more</div>
      </div>
    </div>
  );
};

export default TemplateOverlay;
