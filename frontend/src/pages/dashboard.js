import React from 'react';
import Navbar from '@/components/Navbar';
import Toolbar from '@/components/Toolbar';
import { FiBookmark, FiDownload, FiShare2 } from 'react-icons/fi';
import styles from '../styles/dashboard.module.css';
import Card from '../components/Card';
import AddDocsCard from '../components/AddDocsCard';

const Home = () => {
  const cardsData = [
    {
      title: 'Student Reports',
      content: 'This is the content of Card 1.',
      footer: 'Last Updated: 22/12/2023 18:55:45',
    },
    {
      title: 'Govt Docs',
      content: 'This is the content of Card 2.',
      footer: 'Last Updated: 22/8/2023 01:50:15',
    },
    {
      title: 'ID Cards',
      content: 'This is the content of Card 2.',
      footer: 'Last Updated: 5/6/2023 20:06:45',
    },
    // Add more card data objects here
  ];

  return (
    <div className={styles.dashboardSection}>
      <Navbar />
      <div className={styles.wrapper}>
        <Toolbar />
        <div className={styles.headerRow}>
          <div className={styles.headingWrapper}>
            <h2 className={styles.heading}>Docs Library</h2>
          </div>
          <div className={styles.rightAlign}>
            <input
              type="text"
              className={styles.searchInput}
              placeholder="Search..."
            />
            <select className={styles.dropdown}>
              <option value="option1">Option 1</option>
              <option value="option2">Option 2</option>
              <option value="option3">Option 3</option>
              <option value="option4">Option 4</option>
            </select>
          </div>
        </div>
        <div className={styles.blueLine}></div>
        <div className={styles.cardsSection}>
          <AddDocsCard />

          {cardsData.map((card, index) => (
            <Card
              key={index}
              title={card.title}
              content={card.content}
              footer={card.footer}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;
