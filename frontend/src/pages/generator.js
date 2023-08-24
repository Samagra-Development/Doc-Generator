// pages/generator.js
import React, { useState } from 'react';
import styles from '../styles/generator.module.css';
import Navbar from '@/components/Navbar';

const Generator = () => {
  const [templateType, setTemplateType] = useState('');
  const [outputType, setOutputType] = useState('');
  const [templateInput, setTemplateInput] = useState('');
  const [dataInput, setDataInput] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Template type:', templateType);
    console.log('Output type:', outputType);
    console.log('Template Input:', templateInput);
    console.log('Data input:', dataInput);
    setTemplateType('');
    setOutputType('');
    setTemplateInput('');
    setDataInput('');
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
                    <option value="html">HTML</option>
                    <option value="pdf">PDF</option>
                    <option value="doc">DOC</option>
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
                    <option value="html">HTML</option>
                    <option value="pdf">PDF</option>
                    <option value="doc">DOC</option>
                  </select>
                </div>
              </div>
            </div>

            <div className={styles.inputBox}>
              <p className={styles.inputHeading}>Template Input</p>
              <textarea
                value={templateInput}
                onChange={(e) => setTemplateInput(e.target.value)}
                className={`${styles.formInput2} ${styles.nonExpandable}`}
                placeholder="Enter text for Template Input"
              />
            </div>
            <div className={styles.inputBox}>
              <p className={styles.inputHeading}>Data Input</p>
              <textarea
                value={dataInput}
                onChange={(e) => setDataInput(e.target.value)}
                className={`${styles.formInput3} ${styles.nonExpandable}`}
                placeholder="Enter text for Data Input"
              />
            </div>
            <input
              type="submit"
              value="Submit"
              className={styles.submitButton}
            />
          </form>
        </div>
        <div className={styles.rightColumn}></div>
      </section>
    </>
  );
};

export default Generator;
