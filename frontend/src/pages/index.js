import Head from 'next/head';
import HomePage from '@/pages/homepage';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Doc Generator</title>
      </Head>
      <main>
        <HomePage />
      </main>
    </div>
  );
}
