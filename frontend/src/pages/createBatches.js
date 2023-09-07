import React, { useState, useEffect } from 'react';
import styles from '../styles/createBatches.module.css';
import Navbar from '../components/Navbar';
import { createBatch, fetchTemplates } from '../services/apiService';
import TemplateOverlay from '../components/TemplateOverlay';

const createBatches = () => {
  const [templateType, setTemplateType] = useState('');
  const [outputType, setOutputType] = useState('');
  const [templateInput, setTemplateInput] = useState(0);
  const [dataInputs, setDataInputs] = useState(['']);
  const [responseBody, setResponseBody] = useState('');
  const [showOverlay, setShowOverlay] = useState(false);
  const [existingTemplates, setExistingTemplates] = useState([]);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const data = dataInputs.map((input) => JSON.parse(input));
      const response = await createBatch(templateType, templateInput, data);

      setResponseBody(JSON.stringify(response, null, 2));
      console.log('Response:', response);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  //multiple input
  const addDataInput = () => {
    setDataInputs([...dataInputs, '']);
  };
  const removeDataInput = (index) => {
    const updatedDataInputs = [...dataInputs];
    updatedDataInputs.splice(index, 1);
    setDataInputs(updatedDataInputs);
  };
  const handleDataInputChange = (index, value) => {
    const updatedDataInputs = [...dataInputs];
    updatedDataInputs[index] = value;
    setDataInputs(updatedDataInputs);
  };

  //existing template
  useEffect(() => {
    const loadTemplates = async () => {
      try {
        const templates = await fetchTemplates();
        setExistingTemplates(templates);
      } catch (error) {
        console.error('Error loading templates:', error);
      }
    };

    if (showOverlay) {
      loadTemplates();
    }
  }, [showOverlay]);

  const toggleOverlay = () => {
    setShowOverlay(!showOverlay);
  };

  return (
    <>
      <Navbar />
      <section className={styles.generatorSection}>
        <div className={styles.leftColumn}>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className={styles.gridContainer}>
              <div className={styles.inputBox}>
                <p className={styles.inputHeading}>Template Type</p>
                <div>
                  <select
                    value={templateType}
                    onChange={(e) => setTemplateType(e.target.value)}
                    className={styles.formInput1}
                  >
                    <option value="">Select a template type</option>
                    <option value="JINJA">JINJA</option>
                    <option value="EJS">EJS</option>
                    <option value="JSTL">JSTL</option>
                  </select>
                </div>
              </div>
              <div className={styles.inputBox}>
                <p className={styles.inputHeading}>Output Type</p>
                <div>
                  <select
                    value={outputType}
                    onChange={(e) => setOutputType(e.target.value)}
                    className={styles.formInput1}
                  >
                    <option value="">Select an output type</option>
                    <option value="png">PNG</option>
                    <option value="jpeg">JPEG</option>
                    <option value="html">DOC</option>
                    <option value="pdf">PDF</option>
                    <option value="qr">QR</option>
                  </select>
                </div>
              </div>
            </div>

            <div className={styles.inputBox}>
              <p className={styles.inputHeading}>Template Input</p>
              <div className={styles.templateButtonContainer}>
                <button
                  onClick={() => {
                    toggleOverlay();
                  }}
                  className={styles.templateButton}
                >
                  Choose from existing templates
                </button>
              </div>
              {showOverlay ? (
                <div>
                  <h3 className={styles.overlayHeading}>
                    Select a Suitable Template
                  </h3>
                  <TemplateOverlay
                    onClose={toggleOverlay}
                    existingTemplates={existingTemplates}
                    onTemplateSelect={setTemplateInput}
                  />
                </div>
              ) : (
                <textarea
                  value={templateInput}
                  onChange={(e) => setTemplateInput(e.target.value)}
                  className={`${styles.formInput2} ${styles.nonExpandable}`}
                  placeholder="Enter string for Template Input"
                />
              )}
            </div>

            {dataInputs.map((dataInput, index) => (
              <div key={index} className={styles.inputBox}>
                <p className={styles.inputHeading}>
                  Data Input {index + 1}
                  {index === dataInputs.length - 1 && (
                    <button
                      type="button"
                      onClick={addDataInput}
                      className={styles.addInputButton}
                    >
                      + Add Data Input
                    </button>
                  )}
                </p>
                <div className={styles.dataInputContainer}>
                  <textarea
                    value={dataInput}
                    onChange={(e) =>
                      handleDataInputChange(index, e.target.value)
                    }
                    className={`${styles.formInput3} ${styles.nonExpandable}`}
                    placeholder="Enter JSON object for Data Input"
                  />
                  {index !== 0 && (
                    <button
                      type="button"
                      onClick={() => removeDataInput(index)}
                      className={styles.deleteInputButton}
                    >
                      &#128465;
                    </button>
                  )}
                </div>
              </div>
            ))}
            <input
              type="submit"
              value="Submit"
              className={styles.submitButton}
            />
          </form>
        </div>
        <div className={styles.rightColumn}>
          <div className={styles.responseContainer}>
            <h3 className={styles.responseHeading}>Progress of generation</h3>
            <pre className={styles.responseText}>{responseBody}</pre>
          </div>
        </div>
      </section>
    </>
  );
};

export default createBatches;
