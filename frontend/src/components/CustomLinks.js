// components/CustomLink.js
import React from 'react';
import Link from 'next/link';

const CustomLink = ({ href, children }) => {
  return (
    <Link href={href}>
      <a>{children}</a>
    </Link>
  );
};

export default CustomLink;
