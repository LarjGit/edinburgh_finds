// app/category/[slug]/page.tsx
import { notFound } from 'next/navigation'
import { categories } from '../../config/categories'
import Navigation from '../../components/Navigation'
import Footer from '../../components/Footer'
import VenueCard from '../../components/VenueCard'
import { prisma } from '../../../lib/prisma'

export default async function CategoryPage({ 
  params 
}: { 
  params: Promise<{ slug: string }> 
}) {
  const { slug } = await params
  
  const categoryConfig = categories[slug]
  if (!categoryConfig || !categoryConfig.isLive) {
    notFound()
  }

  const listings = await prisma.listings.findMany({
    where: {
      canonical_categories: {
        has: slug
      }
    },
    include: {
      venues: true
    },
    orderBy: {
      entity_name: 'asc'
    }
  })

  if (listings.length === 0) {
    notFound()
  }

  return (
    <>
      <Navigation />
      
      <section 
        className="bg-linear-to-br from-primary to-primary/70 text-primary-foreground py-10">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            {categoryConfig.name} in Edinburgh
          </h1>
          <p className="text-xl text-opacity/90">
            {listings.length} {listings.length === 1 ? 'place' : 'places'}
          </p>
        </div>
      </section>

      <section className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {listings.map((listing) => {
            switch(listing.entity_type) {
              case 'venue':
                if (!categoryConfig.venue) return null
                return (
                  <VenueCard
                    key={listing.listing_id}
                    listing={listing}
                    entityConfig={categoryConfig.venue}
                  />
                )
              
              // Future entity types
              case 'retailer':
              case 'coach':
              case 'club':
              case 'event':
                return null
              
              default:
                return null
            }
          })}
        </div>
      </section>
      
      <Footer />
    </>
  )
}