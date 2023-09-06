import React, { useState } from 'react';
import styles from '../styles/generator.module.css';
import Navbar from '../components/Navbar';
import { generateRender } from '../services/apiService';
import TemplateOverlay from '../components/TemplateOverlay';

const Generator = () => {
  const [templateType, setTemplateType] = useState('');
  const [outputType, setOutputType] = useState('');
  const [templateInput, setTemplateInput] = useState('');
  const [dataInput, setDataInput] = useState('');
  const [responseBody, setResponseBody] = useState('');
  const [isNewTemplate, setIsNewTemplate] = useState(false);
  const [showOverlay, setShowOverlay] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const data = JSON.parse(dataInput);
      const response = await generateRender(templateType, templateInput, data);

      setResponseBody(JSON.stringify(response, null, 2));
      console.log('Response:', response);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  const existingTemplates = [
    { heading: 'Template 1', text: 'This is template 1.' },
    { heading: 'Template 2', text: 'This is template 2.' },
  ];
  const toggleOverlay = () => {
    setShowOverlay(!showOverlay);
  };

  const toggleTemplateInput = () => {
    setIsNewTemplate(!isNewTemplate);
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

            {/* <div className={styles.inputBox}>
              <p className={styles.inputHeading}>Template Input</p>
              <textarea
                value={templateInput}
                onChange={(e) => setTemplateInput(e.target.value)}
                className={`${styles.formInput2} ${styles.nonExpandable}`}
                placeholder="Enter string for Template Input"
              />
            </div> */}
            <div className={styles.inputBox}>
              <p className={styles.inputHeading}>Data Input</p>
              <textarea
                value={dataInput}
                onChange={(e) => setDataInput(e.target.value)}
                className={`${styles.formInput3} ${styles.nonExpandable}`}
                placeholder="Enter JSON object for Data Input"
              />
            </div>
            <input
              type="submit"
              value="Submit"
              className={styles.submitButton}
            />
          </form>
        </div>
        <div className={styles.rightColumn}>
          <div className={styles.responseContainer}>
            <h3 className={styles.responseHeading}>Rendered Document</h3>
            <pre className={styles.responseText}>{responseBody}</pre>
          </div>
        </div>
      </section>
    </>
  );
};

export default Generator;
