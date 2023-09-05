// components/Hero.js
import React from 'react';
import { useRouter } from 'next/router';
import styles from '../styles/hero.module.css';

const Hero = () => {
  const router = useRouter();

  const handleButtonClick = () => {
    router.push('/generator');
  };

  return (
    <section className={styles['hero-section']}>
      <div className={styles['hero-content']}>
        <h1 className={styles['hero-title']}>Hello,</h1>
        <h3 className={styles['hero-subtitle']}>
          Here&apos;s a super cool way of doc-generation!
        </h3>
        <p className={styles['hero-paragraph']}>
          The Doc-Generator is an easily integrable and reusable tool built on
          open-source software (OSS). It provides seamless generation of single
          and bulk documents in various available formats, ensuring
          interoperability.
        </p>
        <button className={styles['hero-button']} onClick={handleButtonClick}>
          GET STARTED
        </button>
      </div>
    </section>
  );
};

export default Hero;
