import Navigation from './components/Navigation'
import Footer from './components/Footer'
import CategoryTile from './components/CategoryTile'
import { categories } from './config/categories'
import Image from 'next/image'

export default function Home() {
  return (
    <>
      <Navigation />
      
      {/* Hero Section with Edinburgh Castle Background */}
      <section className="relative h-[450px] flex items-center justify-center">
        {/* Background Image */}
        <Image
          src="/images/edinburgh-castle.jpg"
          alt="Edinburgh Castle"
          fill
          className="object-cover object-[center_30%]"
          priority
        />
        
        {/* Dark Overlay for Text Readability */}
        <div className="absolute inset-0 bg-black/40" />
        
        {/* Content */}
        <div className="relative z-10 text-center text-white px-4">
          <div className="mb-6">
            <Image
              src="/images/branding/logo.png"
              alt="Edinburgh Finds Logo"
              width={150}
              height={150}
              className="mx-auto"
            />
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold mb-4">
            Find your thing in Edinburgh
          </h1>
          
          <p className="text-lg md:text-xl max-w-2xl mx-auto">
            Discover clubs, activities, and experiences across Edinburgh.
          </p>
          <p className="text-lg md:text-xl max-w-2xl mx-auto">
            Curated by locals.
          </p>
        </div>
      </section>

      <section className="pt-8 pb-24 bg-secondary">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-secondary-foreground">
            Browse Categories
          </h2>
          
          {/* Grid - 3 columns on desktop, 1 on mobile */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {Object.entries(categories).map(([slug, category]) => (
              <CategoryTile
                key={slug}
                slug={slug}
                name={category.name}
                image={category.image}
                isLive={category.isLive}
              />
            ))}
          </div>
        </div>
      </section>
      
      <Footer />
    </>
  )
}