import React from 'react';
import { FiBookmark, FiDownload, FiShare2 } from 'react-icons/fi';
import styles from '../styles/card.module.css';

const Card = ({ title, content, footer, imageUrl }) => {
  return (
    <div className={styles.card}>
      <div className={styles.cardHeader}>
        <img src={imageUrl} alt={title} className={styles.cardImage} />
        <FiBookmark className={styles.bookmarkIcon} />
      </div>
      <h3>{title}</h3>
      <p>{content}</p>

      <div className={styles.blueLine}></div>
      <div className={styles.footer}>
        <p className={styles.footerContent}>{footer}</p>

        <FiDownload className={styles.cardIcon} />
        <FiShare2 className={styles.cardIcon} />
      </div>
    </div>
  );
};

export default Card;
