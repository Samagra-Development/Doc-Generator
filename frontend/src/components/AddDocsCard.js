import React from 'react';
import { FiPlus } from 'react-icons/fi';
import { useRouter } from 'next/router';

import styles from '../styles/addDocsCard.module.css';

const AddDocsCard = () => {
  const router = useRouter();

  const handleAddDocs = () => {
    router.push('/createBatches');
  };

  return (
    <div className={styles.addDocsCard} onClick={handleAddDocs}>
      <div className={styles.centerContent}>
        <div className={styles.addIcon}>
          <FiPlus />
        </div>
        <h3 className={styles.cardHeading}>Create a Batch</h3>
      </div>
    </div>
  );
};

export default AddDocsCard;
