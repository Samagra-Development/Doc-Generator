import React from 'react';
import Image from 'next/image';
import { FiShare2 } from 'react-icons/fi';
import styles from '../styles/card.module.css';

const Card = ({ title, content, output, status, footer }) => {
  return (
    <div className={styles.card}>
      <div className={styles.cardHeader}></div>
      <h3>{title}</h3>
      <p>{content}</p>
      <p>{output}</p>
      <p>{status}</p>

      <div className={styles.blueLine}></div>
      <div className={styles.footer}>
        <p className={styles.footerContent}>Created at: {footer}</p>

        <FiShare2 className={styles.cardIcon} />
      </div>
    </div>
  );
};

export default Card;
