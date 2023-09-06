import Head from 'next/head';
import Hero from '@/components/Hero';
import Navbar from '@/components/Navbar';
import Information from '@/components/Information';
export default function Home() {
  return (
    <div>
      <Head>
        <title>Doc Generator</title>
      </Head>
      <main>
        <Navbar />
        <Hero />
        <Information />
      </main>
    </div>
  );
}
