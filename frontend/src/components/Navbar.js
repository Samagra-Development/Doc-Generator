// components/Navbar.js
import React from 'react';
import styles from '../styles/navbar.module.css';

const Navbar = () => {
  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        <img src="/images/logo.png" alt="Logo" />
      </div>
      <div className={styles.buttons}>
        <button className={styles.buttonTransparent}>Login</button>
        <button className={styles.buttonGradient}>Signup</button>
      </div>
    </nav>
  );
};

export default Navbar;
