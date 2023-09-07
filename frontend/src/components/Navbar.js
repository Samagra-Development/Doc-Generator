// components/Navbar.js
import React from 'react';
import Image from 'next/image';

import styles from '../styles/navbar.module.css';
import logo from '../../public/images/logo.png';

const Navbar = () => {
  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        <Image src={logo} alt="Doc Generator" />
      </div>
      <div className={styles.buttons}>
        <button className={styles.buttonTransparent}>Login</button>
        <button className={styles.buttonGradient}>Signup</button>
      </div>
    </nav>
  );
};

export default Navbar;
