import Hero from '@/components/Hero';
import Navbar from '@/components/Navbar';
import Information from '@/components/Information';

export default function HomePage() {
  return (
    <div>
      <Navbar />
      <Hero />
      <Information />
    </div>
  );
}
