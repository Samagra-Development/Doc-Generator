import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import Toolbar from '../components/Toolbar';
import styles from '../styles/dashboard.module.css';
import Card from '../components/Card';
import AddDocsCard from '../components/AddDocsCard';
import { fetchBatches } from '../services/apiService';

const Home = () => {
  const [batches, setBatches] = useState([]);
  const [selectedStatus, setSelectedStatus] = useState('all');
  useEffect(() => {
    const fetchBatchesData = async () => {
      try {
        const data = await fetchBatches();
        setBatches(data);
      } catch (error) {
        console.error(error.message);
      }
    };

    fetchBatchesData();
  }, []);

  const filteredBatches =
    selectedStatus === 'all'
      ? batches
      : batches.filter((batch) => batch.status === selectedStatus);

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
              <option value="all">All</option>
              <option value="done">Done</option>
              <option value="queue">In queue</option>
              <option value="stop">Stopped</option>
            </select>
          </div>
        </div>
        <div className={styles.blueLine}></div>
        <div className={styles.cardsSection}>
          <AddDocsCard />

          {filteredBatches.map((batch, index) => (
            <Card
              key={index}
              title={batch.id}
              content={` Template ID: ${batch.templateID}, Output Type: ${batch.outputType}`}
              output={`Output: ${batch.output}`}
              status={`Status: ${batch.status}`}
              footer={batch.createdAt}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;
