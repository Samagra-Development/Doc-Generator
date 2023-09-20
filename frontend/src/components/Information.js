// components/Information.js
import React from 'react';
import styles from '../styles/information.module.css';

const Information = () => {
  return (
    <section className={styles['information-section']}>
      <div className={styles['information-content']}>
        <div className={styles['information-text']}>
          <h2 className={styles['information-heading']}>
            Welcome to Our Website
          </h2>
          <p className={styles['information-paragraph']}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat.
          </p>
          <div className={styles['information-buttons']}>
            <button className={styles['information-button']}>Learn More</button>
            <button className={styles['information-button']}>Contact Us</button>
          </div>
        </div>
        <div className={styles['information-image']}>
          <img src="/path/to/your/image.jpg" alt="Information Image" />
        </div>
      </div>
    </section>
  );
};

export default Information;
