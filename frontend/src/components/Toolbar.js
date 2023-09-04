// components/Toolbar.js
import React from 'react';
import Image from 'next/image';
import styles from '../styles/toolbar.module.css';
import processingImg from '../../public/images/processing.png';
import completedImg from '../../public/images/completed.png';
import failedImg from '../../public/images/failed.png';
import queueImg from '../../public/images/queue.png';

const Toolbar = () => {
  return (
    <div className={styles.toolbar}>
      <div className={styles.toolbarIcon}>
        <Image src={processingImg} alt="Icon 1" />
        <a href="#" className={styles.link}>
          Processing: 5
        </a>
      </div>
      <div className={styles.toolbarIcon}>
        <Image src={completedImg} alt="Icon 1" />
        <a href="#" className={styles.link}>
          Completed: 3
        </a>
      </div>
      <div className={styles.toolbarIcon}>
        <Image src={failedImg} alt="Icon 1" />
        <a href="#" className={styles.link}>
          Failed: 1
        </a>
      </div>
      <div className={styles.toolbarIcon}>
        <Image src={queueImg} alt="Icon 1" />
        <a href="#" className={styles.link}>
          In Queue: 4
        </a>
      </div>
    </div>
  );
};

export default Toolbar;
