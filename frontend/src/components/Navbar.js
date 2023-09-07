// components/Navbar.js
import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import styles from '../styles/navbar.module.css';
import logo from '../../public/images/logo.png';

const Navbar = () => {
  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        <Link href="/">
          <Image src={logo} alt="Doc Generator" />
        </Link>
      </div>
      <div className={styles.buttons}>
        <Link href="/generator">
          <button className={styles.buttonTransparent}>Generate</button>
        </Link>
        <Link href="/dashboard">
          <button className={styles.buttonTransparent}>Dashboard</button>
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
