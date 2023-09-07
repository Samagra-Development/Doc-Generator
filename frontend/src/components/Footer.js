// components/Footer.js
import { FaGithub } from 'react-icons/fa';
import styles from '../styles/footer.module.css';
const Footer = () => {
  return (
    <footer className={styles.footer}>
      <div className={styles.footerLeft}>Doc-generator</div>
      <div className={styles.footerRight}>
        <a
          href="https://github.com/Samagra-Development/Doc-Generator"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaGithub />
        </a>
      </div>
    </footer>
  );
};

export default Footer;
